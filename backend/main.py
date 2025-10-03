from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="Testing SaaS Platform API",
    description="Universal Automated Testing & Deployment Readiness Tool",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"

class ProjectType(str, Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    BACKEND_SERVICE = "backend_service"
    CODE_REPOSITORY = "code_repository"

class TestCategory(BaseModel):
    name: str
    score: int
    status: TestStatus
    issues: List[str]
    fixes: List[str]

class TestReport(BaseModel):
    id: str
    project_name: str
    project_type: ProjectType
    status: TestStatus
    overall_score: int
    created_at: datetime
    completed_at: Optional[datetime]
    categories: List[TestCategory]
    production_ready: bool

class ProjectCreate(BaseModel):
    name: str
    type: ProjectType
    repository_url: Optional[str]
    description: Optional[str]

# In-memory storage (will be replaced with database)
projects_db = []
reports_db = []

@app.get("/")
async def root():
    return {
        "message": "Testing SaaS Platform API",
        "version": "1.0.0",
        "endpoints": {
            "projects": "/api/projects",
            "reports": "/api/reports",
            "run_test": "/api/test/run"
        }
    }

@app.get("/api/projects")
async def get_projects():
    return {"projects": projects_db}

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    new_project = {
        "id": f"proj_{len(projects_db) + 1}",
        "name": project.name,
        "type": project.type,
        "repository_url": project.repository_url,
        "description": project.description,
        "created_at": datetime.now().isoformat()
    }
    projects_db.append(new_project)
    return new_project

@app.get("/api/reports")
async def get_reports():
    return {"reports": reports_db}

@app.post("/api/test/run")
async def run_test(project_id: str):
    # Mock test execution
    mock_report = {
        "id": f"report_{len(reports_db) + 1}",
        "project_name": "Sample Project",
        "project_type": ProjectType.WEB_APP,
        "status": TestStatus.RUNNING,
        "overall_score": 0,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "categories": [
            {
                "name": "Code Quality",
                "score": 85,
                "status": TestStatus.RUNNING,
                "issues": [],
                "fixes": []
            },
            {
                "name": "Security",
                "score": 92,
                "status": TestStatus.RUNNING,
                "issues": [],
                "fixes": []
            },
            {
                "name": "Performance",
                "score": 70,
                "status": TestStatus.RUNNING,
                "issues": [],
                "fixes": []
            }
        ],
        "production_ready": False
    }
    reports_db.append(mock_report)
    return {"message": "Test started", "report_id": mock_report["id"], "status": "running"}

@app.get("/api/reports/{report_id}")
async def get_report(report_id: str):
    report = next((r for r in reports_db if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.get("/api/stats")
async def get_stats():
    return {
        "total_projects": len(projects_db),
        "tests_run_today": 47,
        "pass_rate": 94,
        "critical_issues": 3
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)