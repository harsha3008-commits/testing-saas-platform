from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from auth import get_current_user
from database import get_db
import secrets

router = APIRouter()

# Pydantic Models
class OrganizationCreate(BaseModel):
    name: str
    billing_email: EmailStr

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    billing_email: Optional[EmailStr] = None

class OrganizationResponse(BaseModel):
    id: int
    name: str
    billing_email: str
    owner_id: int
    created_at: datetime
    member_count: int
    project_count: int

class InviteCreate(BaseModel):
    email: EmailStr
    role: str  # admin, developer, viewer

class InviteResponse(BaseModel):
    id: int
    organization_id: int
    email: str
    role: str
    token: str
    expires_at: datetime
    created_at: datetime

class MemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    role: str
    joined_at: datetime

class RoleUpdate(BaseModel):
    role: str  # admin, developer, viewer

# Organization Management
@router.post("/organizations", response_model=OrganizationResponse)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new organization"""
    # Check if user already owns an organization (optional limit)
    existing_org = db.execute(
        "SELECT id FROM organizations WHERE owner_id = %s",
        (current_user["id"],)
    ).fetchone()
    
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already owns an organization"
        )
    
    # Create organization
    cursor = db.execute(
        """
        INSERT INTO organizations (name, billing_email, owner_id, created_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id, name, billing_email, owner_id, created_at
        """,
        (org_data.name, org_data.billing_email, current_user["id"], datetime.utcnow())
    )
    org = cursor.fetchone()
    db.commit()
    
    # Add owner as admin member
    db.execute(
        """
        INSERT INTO organization_members (organization_id, user_id, role, joined_at)
        VALUES (%s, %s, 'admin', %s)
        """,
        (org[0], current_user["id"], datetime.utcnow())
    )
    db.commit()
    
    return {
        "id": org[0],
        "name": org[1],
        "billing_email": org[2],
        "owner_id": org[3],
        "created_at": org[4],
        "member_count": 1,
        "project_count": 0
    }

@router.get("/organizations", response_model=List[OrganizationResponse])
async def list_user_organizations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all organizations the user belongs to"""
    cursor = db.execute(
        """
        SELECT 
            o.id, o.name, o.billing_email, o.owner_id, o.created_at,
            COUNT(DISTINCT om.user_id) as member_count,
            COUNT(DISTINCT p.id) as project_count
        FROM organizations o
        INNER JOIN organization_members om ON o.id = om.organization_id
        LEFT JOIN projects p ON o.id = p.organization_id
        WHERE om.user_id = %s
        GROUP BY o.id, o.name, o.billing_email, o.owner_id, o.created_at
        ORDER BY o.created_at DESC
        """,
        (current_user["id"],)
    )
    
    organizations = []
    for row in cursor.fetchall():
        organizations.append({
            "id": row[0],
            "name": row[1],
            "billing_email": row[2],
            "owner_id": row[3],
            "created_at": row[4],
            "member_count": row[5],
            "project_count": row[6]
        })
    
    return organizations

@router.get("/organizations/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get organization details"""
    # Check if user is a member
    member = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this organization"
        )
    
    cursor = db.execute(
        """
        SELECT 
            o.id, o.name, o.billing_email, o.owner_id, o.created_at,
            COUNT(DISTINCT om.user_id) as member_count,
            COUNT(DISTINCT p.id) as project_count
        FROM organizations o
        LEFT JOIN organization_members om ON o.id = om.organization_id
        LEFT JOIN projects p ON o.id = p.organization_id
        WHERE o.id = %s
        GROUP BY o.id, o.name, o.billing_email, o.owner_id, o.created_at
        """,
        (org_id,)
    )
    
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return {
        "id": row[0],
        "name": row[1],
        "billing_email": row[2],
        "owner_id": row[3],
        "created_at": row[4],
        "member_count": row[5],
        "project_count": row[6]
    }

@router.patch("/organizations/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_data: OrganizationUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update organization details (admin only)"""
    # Check if user is admin
    member = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not member or member[0] not in ['admin', 'owner']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    update_fields = []
    update_values = []
    
    if org_data.name:
        update_fields.append("name = %s")
        update_values.append(org_data.name)
    
    if org_data.billing_email:
        update_fields.append("billing_email = %s")
        update_values.append(org_data.billing_email)
    
    if update_fields:
        update_values.append(org_id)
        db.execute(
            f"UPDATE organizations SET {', '.join(update_fields)} WHERE id = %s",
            tuple(update_values)
        )
        db.commit()
    
    return await get_organization(org_id, current_user, db)

# Team Member Management
@router.get("/organizations/{org_id}/members", response_model=List[MemberResponse])
async def list_organization_members(
    org_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all members of an organization"""
    # Check if user is a member
    member = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this organization"
        )
    
    cursor = db.execute(
        """
        SELECT om.id, om.user_id, u.username, u.email, om.role, om.joined_at
        FROM organization_members om
        INNER JOIN users u ON om.user_id = u.id
        WHERE om.organization_id = %s
        ORDER BY om.joined_at ASC
        """,
        (org_id,)
    )
    
    members = []
    for row in cursor.fetchall():
        members.append({
            "id": row[0],
            "user_id": row[1],
            "username": row[2],
            "email": row[3],
            "role": row[4],
            "joined_at": row[5]
        })
    
    return members

@router.patch("/organizations/{org_id}/members/{user_id}/role", response_model=MemberResponse)
async def update_member_role(
    org_id: int,
    user_id: int,
    role_data: RoleUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a member's role (admin only)"""
    # Check if current user is admin
    admin_check = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not admin_check or admin_check[0] not in ['admin', 'owner']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Validate role
    if role_data.role not in ['admin', 'developer', 'viewer']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    # Update role
    db.execute(
        "UPDATE organization_members SET role = %s WHERE organization_id = %s AND user_id = %s",
        (role_data.role, org_id, user_id)
    )
    db.commit()
    
    # Fetch updated member
    cursor = db.execute(
        """
        SELECT om.id, om.user_id, u.username, u.email, om.role, om.joined_at
        FROM organization_members om
        INNER JOIN users u ON om.user_id = u.id
        WHERE om.organization_id = %s AND om.user_id = %s
        """,
        (org_id, user_id)
    )
    
    row = cursor.fetchone()
    return {
        "id": row[0],
        "user_id": row[1],
        "username": row[2],
        "email": row[3],
        "role": row[4],
        "joined_at": row[5]
    }

@router.delete("/organizations/{org_id}/members/{user_id}")
async def remove_member(
    org_id: int,
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a member from organization (admin only)"""
    # Check if current user is admin
    admin_check = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not admin_check or admin_check[0] not in ['admin', 'owner']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Check if trying to remove owner
    org_owner = db.execute(
        "SELECT owner_id FROM organizations WHERE id = %s",
        (org_id,)
    ).fetchone()
    
    if org_owner and org_owner[0] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove organization owner"
        )
    
    db.execute(
        "DELETE FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, user_id)
    )
    db.commit()
    
    return {"message": "Member removed successfully"}

# Invitation Management
@router.post("/organizations/{org_id}/invites", response_model=InviteResponse)
async def create_invite(
    org_id: int,
    invite_data: InviteCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an invitation to join the organization (admin only)"""
    # Check if current user is admin
    admin_check = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not admin_check or admin_check[0] not in ['admin', 'owner']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Validate role
    if invite_data.role not in ['admin', 'developer', 'viewer']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    # Generate invite token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    cursor = db.execute(
        """
        INSERT INTO organization_invites 
        (organization_id, email, role, token, expires_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, organization_id, email, role, token, expires_at, created_at
        """,
        (org_id, invite_data.email, invite_data.role, token, expires_at, datetime.utcnow())
    )
    
    invite = cursor.fetchone()
    db.commit()
    
    # TODO: Send invitation email
    
    return {
        "id": invite[0],
        "organization_id": invite[1],
        "email": invite[2],
        "role": invite[3],
        "token": invite[4],
        "expires_at": invite[5],
        "created_at": invite[6]
    }

@router.get("/organizations/{org_id}/invites", response_model=List[InviteResponse])
async def list_invites(
    org_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all pending invitations (admin only)"""
    # Check if current user is admin
    admin_check = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not admin_check or admin_check[0] not in ['admin', 'owner']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    cursor = db.execute(
        """
        SELECT id, organization_id, email, role, token, expires_at, created_at
        FROM organization_invites
        WHERE organization_id = %s AND expires_at > %s
        ORDER BY created_at DESC
        """,
        (org_id, datetime.utcnow())
    )
    
    invites = []
    for row in cursor.fetchall():
        invites.append({
            "id": row[0],
            "organization_id": row[1],
            "email": row[2],
            "role": row[3],
            "token": row[4],
            "expires_at": row[5],
            "created_at": row[6]
        })
    
    return invites

@router.post("/invites/{token}/accept")
async def accept_invite(
    token: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept an organization invitation"""
    # Find invite
    cursor = db.execute(
        """
        SELECT id, organization_id, email, role, expires_at
        FROM organization_invites
        WHERE token = %s AND expires_at > %s
        """,
        (token, datetime.utcnow())
    )
    
    invite = cursor.fetchone()
    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired invitation"
        )
    
    # Check if email matches
    if invite[2].lower() != current_user["email"].lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation is for a different email address"
        )
    
    # Check if already a member
    existing = db.execute(
        "SELECT id FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (invite[1], current_user["id"])
    ).fetchone()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already a member of this organization"
        )
    
    # Add user to organization
    db.execute(
        """
        INSERT INTO organization_members (organization_id, user_id, role, joined_at)
        VALUES (%s, %s, %s, %s)
        """,
        (invite[1], current_user["id"], invite[3], datetime.utcnow())
    )
    
    # Delete invitation
    db.execute("DELETE FROM organization_invites WHERE id = %s", (invite[0],))
    db.commit()
    
    return {"message": "Successfully joined organization"}

@router.delete("/organizations/{org_id}/invites/{invite_id}")
async def revoke_invite(
    org_id: int,
    invite_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke an invitation (admin only)"""
    # Check if current user is admin
    admin_check = db.execute(
        "SELECT role FROM organization_members WHERE organization_id = %s AND user_id = %s",
        (org_id, current_user["id"])
    ).fetchone()
    
    if not admin_check or admin_check[0] not in ['admin', 'owner']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    db.execute(
        "DELETE FROM organization_invites WHERE id = %s AND organization_id = %s",
        (invite_id, org_id)
    )
    db.commit()
    
    return {"message": "Invitation revoked successfully"}