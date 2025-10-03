'use client';

import { useState, useEffect } from 'react';
import { Plus, Users, Settings, Mail, Trash2, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';

interface Organization {
  id: number;
  name: string;
  billing_email: string;
  owner_id: number;
  created_at: string;
  member_count: number;
  project_count: number;
}

interface Member {
  id: number;
  user_id: number;
  username: string;
  email: string;
  role: string;
  joined_at: string;
}

interface Invite {
  id: number;
  organization_id: number;
  email: string;
  role: string;
  token: string;
  expires_at: string;
  created_at: string;
}

export default function OrganizationsPage() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [invites, setInvites] = useState<Invite[]>([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);
  const [newOrgName, setNewOrgName] = useState('');
  const [newOrgEmail, setNewOrgEmail] = useState('');
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('developer');

  useEffect(() => {
    fetchOrganizations();
  }, []);

  useEffect(() => {
    if (selectedOrg) {
      fetchMembers(selectedOrg.id);
      fetchInvites(selectedOrg.id);
    }
  }, [selectedOrg]);

  const fetchOrganizations = async () => {
    try {
      const response = await fetch('/api/organizations', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      const data = await response.json();
      setOrganizations(data);
      if (data.length > 0 && !selectedOrg) {
        setSelectedOrg(data[0]);
      }
    } catch (error) {
      console.error('Error fetching organizations:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMembers = async (orgId: number) => {
    try {
      const response = await fetch(`/api/organizations/${orgId}/members`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      const data = await response.json();
      setMembers(data);
    } catch (error) {
      console.error('Error fetching members:', error);
    }
  };

  const fetchInvites = async (orgId: number) => {
    try {
      const response = await fetch(`/api/organizations/${orgId}/invites`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      const data = await response.json();
      setInvites(data);
    } catch (error) {
      console.error('Error fetching invites:', error);
    }
  };

  const createOrganization = async () => {
    try {
      const response = await fetch('/api/organizations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          name: newOrgName,
          billing_email: newOrgEmail,
        }),
      });

      if (response.ok) {
        setCreateDialogOpen(false);
        setNewOrgName('');
        setNewOrgEmail('');
        fetchOrganizations();
      }
    } catch (error) {
      console.error('Error creating organization:', error);
    }
  };

  const sendInvite = async () => {
    if (!selectedOrg) return;

    try {
      const response = await fetch(
        `/api/organizations/${selectedOrg.id}/invites`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            email: inviteEmail,
            role: inviteRole,
          }),
        }
      );

      if (response.ok) {
        setInviteDialogOpen(false);
        setInviteEmail('');
        setInviteRole('developer');
        fetchInvites(selectedOrg.id);
      }
    } catch (error) {
      console.error('Error sending invite:', error);
    }
  };

  const updateMemberRole = async (memberId: number, userId: number, newRole: string) => {
    if (!selectedOrg) return;

    try {
      const response = await fetch(
        `/api/organizations/${selectedOrg.id}/members/${userId}/role`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ role: newRole }),
        }
      );

      if (response.ok) {
        fetchMembers(selectedOrg.id);
      }
    } catch (error) {
      console.error('Error updating member role:', error);
    }
  };

  const removeMember = async (userId: number) => {
    if (!selectedOrg) return;

    try {
      const response = await fetch(
        `/api/organizations/${selectedOrg.id}/members/${userId}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      );

      if (response.ok) {
        fetchMembers(selectedOrg.id);
      }
    } catch (error) {
      console.error('Error removing member:', error);
    }
  };

  const revokeInvite = async (inviteId: number) => {
    if (!selectedOrg) return;

    try {
      const response = await fetch(
        `/api/organizations/${selectedOrg.id}/invites/${inviteId}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      );

      if (response.ok) {
        fetchInvites(selectedOrg.id);
      }
    } catch (error) {
      console.error('Error revoking invite:', error);
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'admin':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      case 'developer':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'viewer':
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
      default:
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Organizations</h1>
          <p className="text-muted-foreground">
            Manage your teams and collaborators
          </p>
        </div>
        <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Organization
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Organization</DialogTitle>
              <DialogDescription>
                Set up a new organization to collaborate with your team
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="org-name">Organization Name</Label>
                <Input
                  id="org-name"
                  placeholder="My Company"
                  value={newOrgName}
                  onChange={(e) => setNewOrgName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="org-email">Billing Email</Label>
                <Input
                  id="org-email"
                  type="email"
                  placeholder="billing@company.com"
                  value={newOrgEmail}
                  onChange={(e) => setNewOrgEmail(e.target.value)}
                />
              </div>
              <Button onClick={createOrganization} className="w-full">
                Create Organization
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-1 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Your Organizations</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {organizations.map((org) => (
                <button
                  key={org.id}
                  onClick={() => setSelectedOrg(org)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    selectedOrg?.id === org.id
                      ? 'bg-primary text-primary-foreground'
                      : 'hover:bg-muted'
                  }`}
                >
                  <div className="font-medium">{org.name}</div>
                  <div className="text-sm opacity-80 flex items-center gap-2 mt-1">
                    <Users className="h-3 w-3" />
                    {org.member_count} members · {org.project_count} projects
                  </div>
                </button>
              ))}
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-2 space-y-6">
          {selectedOrg && (
            <>
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>{selectedOrg.name}</CardTitle>
                      <CardDescription>
                        {selectedOrg.billing_email}
                      </CardDescription>
                    </div>
                    <Button variant="outline" size="sm">
                      <Settings className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <div className="text-2xl font-bold">
                        {selectedOrg.member_count}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Members
                      </div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold">
                        {selectedOrg.project_count}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Projects
                      </div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold">{invites.length}</div>
                      <div className="text-sm text-muted-foreground">
                        Pending Invites
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Team Members</CardTitle>
                    <Dialog
                      open={inviteDialogOpen}
                      onOpenChange={setInviteDialogOpen}
                    >
                      <DialogTrigger asChild>
                        <Button size="sm">
                          <Mail className="mr-2 h-4 w-4" />
                          Invite Member
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Invite Team Member</DialogTitle>
                          <DialogDescription>
                            Send an invitation to join your organization
                          </DialogDescription>
                        </DialogHeader>
                        <div className="space-y-4">
                          <div className="space-y-2">
                            <Label htmlFor="invite-email">Email Address</Label>
                            <Input
                              id="invite-email"
                              type="email"
                              placeholder="colleague@company.com"
                              value={inviteEmail}
                              onChange={(e) => setInviteEmail(e.target.value)}
                            />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="invite-role">Role</Label>
                            <Select
                              value={inviteRole}
                              onValueChange={setInviteRole}
                            >
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="admin">Admin</SelectItem>
                                <SelectItem value="developer">
                                  Developer
                                </SelectItem>
                                <SelectItem value="viewer">Viewer</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                          <Button onClick={sendInvite} className="w-full">
                            Send Invitation
                          </Button>
                        </div>
                      </DialogContent>
                    </Dialog>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {members.map((member) => (
                      <div
                        key={member.id}
                        className="flex items-center justify-between p-3 border rounded-lg"
                      >
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                            <Users className="h-5 w-5 text-primary" />
                          </div>
                          <div>
                            <div className="font-medium">{member.username}</div>
                            <div className="text-sm text-muted-foreground">
                              {member.email}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Select
                            value={member.role}
                            onValueChange={(value) =>
                              updateMemberRole(member.id, member.user_id, value)
                            }
                          >
                            <SelectTrigger className="w-32">
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="admin">
                                <div className="flex items-center gap-2">
                                  <Shield className="h-3 w-3" />
                                  Admin
                                </div>
                              </SelectItem>
                              <SelectItem value="developer">
                                Developer
                              </SelectItem>
                              <SelectItem value="viewer">Viewer</SelectItem>
                            </SelectContent>
                          </Select>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeMember(member.user_id)}
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {invites.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Pending Invitations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {invites.map((invite) => (
                        <div
                          key={invite.id}
                          className="flex items-center justify-between p-3 border rounded-lg"
                        >
                          <div className="flex items-center gap-3">
                            <Mail className="h-5 w-5 text-muted-foreground" />
                            <div>
                              <div className="font-medium">{invite.email}</div>
                              <div className="text-sm text-muted-foreground">
                                Invited as {invite.role} ·{' '}
                                {new Date(invite.created_at).toLocaleDateString()}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge
                              variant="outline"
                              className={getRoleBadgeColor(invite.role)}
                            >
                              {invite.role}
                            </Badge>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => revokeInvite(invite.id)}
                            >
                              <Trash2 className="h-4 w-4 text-destructive" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}