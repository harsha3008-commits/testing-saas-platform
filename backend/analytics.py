from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from auth import get_current_user
from database import get_db

router = APIRouter()

# Pydantic Models
class TrendDataPoint(BaseModel):
    date: str
    passed: int
    failed: int
    total: int
    pass_rate: float

class TestTrends(BaseModel):
    period: str
    data: List[TrendDataPoint]
    overall_pass_rate: float
    total_runs: int

class CoverageStats(BaseModel):
    project_id: int
    project_name: str
    average_coverage: float
    latest_coverage: Optional[float]
    trend: str  # increasing, decreasing, stable

class FailurePattern(BaseModel):
    test_name: str
    failure_count: int
    first_failure: str
    last_failure: str
    error_message: Optional[str]

class ProjectAnalytics(BaseModel):
    project_id: int
    project_name: str
    total_runs: int
    passed_runs: int
    failed_runs: int
    pass_rate: float
    average_duration: float
    average_coverage: Optional[float]
    most_common_failures: List[str]

# Analytics Endpoints
@router.get("/analytics/trends", response_model=TestTrends)
async def get_test_trends(
    period: str = Query("7d", regex="^(7d|30d|90d)$"),
    project_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get test run trends over time"""
    # Calculate date range
    days = int(period[:-1])
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Build query based on project filter
    if project_id:
        # Verify user has access to project
        project = db.execute(
            "SELECT id FROM projects WHERE id = %s AND user_id = %s",
            (project_id, current_user["id"])
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_filter = "AND p.id = %s"
        params = (current_user["id"], start_date, project_id)
    else:
        project_filter = ""
        params = (current_user["id"], start_date)
    
    # Fetch daily aggregated data
    cursor = db.execute(
        f"""
        SELECT 
            DATE(tr.created_at) as date,
            COUNT(*) as total,
            COUNT(CASE WHEN tr.status = 'passed' THEN 1 END) as passed,
            COUNT(CASE WHEN tr.status = 'failed' THEN 1 END) as failed
        FROM test_runs tr
        JOIN projects p ON tr.project_id = p.id
        WHERE p.user_id = %s AND tr.created_at >= %s {project_filter}
        GROUP BY DATE(tr.created_at)
        ORDER BY date ASC
        """,
        params
    )
    
    data_points = []
    total_passed = 0
    total_failed = 0
    
    for row in cursor.fetchall():
        date = row[0]
        total = row[1]
        passed = row[2]
        failed = row[3]
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        data_points.append(TrendDataPoint(
            date=date.isoformat() if isinstance(date, datetime) else str(date),
            passed=passed,
            failed=failed,
            total=total,
            pass_rate=round(pass_rate, 2)
        ))
        
        total_passed += passed
        total_failed += failed
    
    total_runs = total_passed + total_failed
    overall_pass_rate = (total_passed / total_runs * 100) if total_runs > 0 else 0
    
    return TestTrends(
        period=period,
        data=data_points,
        overall_pass_rate=round(overall_pass_rate, 2),
        total_runs=total_runs
    )

@router.get("/analytics/coverage", response_model=List[CoverageStats])
async def get_coverage_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get code coverage statistics for all projects"""
    cursor = db.execute(
        """
        WITH coverage_data AS (
            SELECT 
                p.id as project_id,
                p.name as project_name,
                tr.coverage,
                tr.created_at,
                ROW_NUMBER() OVER (PARTITION BY p.id ORDER BY tr.created_at DESC) as rn
            FROM projects p
            LEFT JOIN test_runs tr ON p.id = tr.project_id AND tr.coverage IS NOT NULL
            WHERE p.user_id = %s
        ),
        latest_coverage AS (
            SELECT project_id, coverage as latest_coverage
            FROM coverage_data
            WHERE rn = 1
        ),
        previous_coverage AS (
            SELECT project_id, coverage as prev_coverage
            FROM coverage_data
            WHERE rn = 2
        )
        SELECT 
            cd.project_id,
            cd.project_name,
            AVG(cd.coverage) as avg_coverage,
            lc.latest_coverage,
            pc.prev_coverage
        FROM coverage_data cd
        LEFT JOIN latest_coverage lc ON cd.project_id = lc.project_id
        LEFT JOIN previous_coverage pc ON cd.project_id = pc.project_id
        GROUP BY cd.project_id, cd.project_name, lc.latest_coverage, pc.prev_coverage
        """,
        (current_user["id"],)
    )
    
    stats = []
    for row in cursor.fetchall():
        project_id = row[0]
        project_name = row[1]
        avg_coverage = row[2]
        latest_coverage = row[3]
        prev_coverage = row[4]
        
        # Determine trend
        if latest_coverage and prev_coverage:
            if latest_coverage > prev_coverage + 1:
                trend = "increasing"
            elif latest_coverage < prev_coverage - 1:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        stats.append(CoverageStats(
            project_id=project_id,
            project_name=project_name,
            average_coverage=round(avg_coverage, 2) if avg_coverage else 0,
            latest_coverage=round(latest_coverage, 2) if latest_coverage else None,
            trend=trend
        ))
    
    return stats

@router.get("/analytics/failure-patterns", response_model=List[FailurePattern])
async def get_failure_patterns(
    project_id: int,
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get most common test failure patterns for a project"""
    # Verify user has access to project
    project = db.execute(
        "SELECT id FROM projects WHERE id = %s AND user_id = %s",
        (project_id, current_user["id"])
    ).fetchone()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    cursor = db.execute(
        """
        SELECT 
            test_name,
            COUNT(*) as failure_count,
            MIN(created_at) as first_failure,
            MAX(created_at) as last_failure,
            error_message
        FROM test_results
        WHERE project_id = %s AND status = 'failed'
        GROUP BY test_name, error_message
        ORDER BY failure_count DESC
        LIMIT %s
        """,
        (project_id, limit)
    )
    
    patterns = []
    for row in cursor.fetchall():
        patterns.append(FailurePattern(
            test_name=row[0],
            failure_count=row[1],
            first_failure=row[2].isoformat() if row[2] else "",
            last_failure=row[3].isoformat() if row[3] else "",
            error_message=row[4]
        ))
    
    return patterns

@router.get("/analytics/projects", response_model=List[ProjectAnalytics])
async def get_project_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for all user projects"""
    cursor = db.execute(
        """
        SELECT 
            p.id as project_id,
            p.name as project_name,
            COUNT(tr.id) as total_runs,
            COUNT(CASE WHEN tr.status = 'passed' THEN 1 END) as passed_runs,
            COUNT(CASE WHEN tr.status = 'failed' THEN 1 END) as failed_runs,
            AVG(tr.duration) as avg_duration,
            AVG(tr.coverage) as avg_coverage
        FROM projects p
        LEFT JOIN test_runs tr ON p.id = tr.project_id
        WHERE p.user_id = %s
        GROUP BY p.id, p.name
        ORDER BY total_runs DESC
        """,
        (current_user["id"],)
    )
    
    analytics = []
    for row in cursor.fetchall():
        project_id = row[0]
        total_runs = row[2]
        passed_runs = row[3]
        pass_rate = (passed_runs / total_runs * 100) if total_runs > 0 else 0
        
        # Get most common failures for this project
        failures_cursor = db.execute(
            """
            SELECT test_name, COUNT(*) as count
            FROM test_results
            WHERE project_id = %s AND status = 'failed'
            GROUP BY test_name
            ORDER BY count DESC
            LIMIT 5
            """,
            (project_id,)
        )
        
        common_failures = [f[0] for f in failures_cursor.fetchall()]
        
        analytics.append(ProjectAnalytics(
            project_id=project_id,
            project_name=row[1],
            total_runs=total_runs,
            passed_runs=passed_runs,
            failed_runs=row[4],
            pass_rate=round(pass_rate, 2),
            average_duration=round(row[5], 2) if row[5] else 0,
            average_coverage=round(row[6], 2) if row[6] else None,
            most_common_failures=common_failures
        ))
    
    return analytics

@router.get("/analytics/summary")
async def get_analytics_summary(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall analytics summary"""
    cursor = db.execute(
        """
        SELECT 
            COUNT(DISTINCT p.id) as total_projects,
            COUNT(tr.id) as total_runs,
            COUNT(CASE WHEN tr.status = 'passed' THEN 1 END) as passed_runs,
            COUNT(CASE WHEN tr.status = 'failed' THEN 1 END) as failed_runs,
            AVG(tr.duration) as avg_duration,
            AVG(tr.coverage) as avg_coverage
        FROM projects p
        LEFT JOIN test_runs tr ON p.id = tr.project_id
        WHERE p.user_id = %s
        """,
        (current_user["id"],)
    )
    
    row = cursor.fetchone()
    total_runs = row[1] or 0
    passed_runs = row[2] or 0
    
    return {
        "total_projects": row[0] or 0,
        "total_runs": total_runs,
        "passed_runs": passed_runs,
        "failed_runs": row[3] or 0,
        "pass_rate": round((passed_runs / total_runs * 100) if total_runs > 0 else 0, 2),
        "average_duration": round(row[4], 2) if row[4] else 0,
        "average_coverage": round(row[5], 2) if row[5] else None
    }