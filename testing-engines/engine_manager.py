"""
Testing Engine Manager
Integrates multiple testing tools: ESLint, Pylint, PyTest, Jest, Snyk, Bandit, JMeter
"""
import subprocess
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class TestEngineManager:
    """Manages integration with various testing engines"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        
    def detect_project_type(self) -> str:
        """Detect project type based on files present"""
        if (self.project_path / "package.json").exists():
            return "javascript"
        elif (self.project_path / "requirements.txt").exists():
            return "python"
        elif (self.project_path / "pom.xml").exists():
            return "java"
        return "unknown"
    
    def run_eslint(self, file_paths: List[str]) -> Dict:
        """Run ESLint for JavaScript/TypeScript code quality"""
        try:
            result = subprocess.run(
                ["npx", "eslint", "--format", "json"] + file_paths,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            issues = json.loads(result.stdout) if result.stdout else []
            
            return {
                "engine": "eslint",
                "status": "completed",
                "issues_count": len(issues),
                "issues": self._format_eslint_issues(issues)
            }
        except Exception as e:
            return {"engine": "eslint", "status": "error", "message": str(e)}
    
    def run_pylint(self, file_paths: List[str]) -> Dict:
        """Run Pylint for Python code quality"""
        try:
            result = subprocess.run(
                ["pylint", "--output-format=json"] + file_paths,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            issues = json.loads(result.stdout) if result.stdout else []
            
            return {
                "engine": "pylint",
                "status": "completed",
                "issues_count": len(issues),
                "issues": self._format_pylint_issues(issues)
            }
        except Exception as e:
            return {"engine": "pylint", "status": "error", "message": str(e)}
    
    def run_pytest(self, test_path: str = "tests") -> Dict:
        """Run PyTest for Python unit tests"""
        try:
            result = subprocess.run(
                ["pytest", test_path, "--json-report", "--json-report-file=report.json"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            report_path = self.project_path / "report.json"
            if report_path.exists():
                with open(report_path, 'r') as f:
                    report = json.load(f)
                
                return {
                    "engine": "pytest",
                    "status": "completed",
                    "tests_passed": report.get("summary", {}).get("passed", 0),
                    "tests_failed": report.get("summary", {}).get("failed", 0),
                    "coverage": report.get("coverage", 0)
                }
            
            return {"engine": "pytest", "status": "no_report"}
        except Exception as e:
            return {"engine": "pytest", "status": "error", "message": str(e)}
    
    def run_jest(self) -> Dict:
        """Run Jest for JavaScript unit tests"""
        try:
            result = subprocess.run(
                ["npx", "jest", "--json", "--coverage"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            report = json.loads(result.stdout) if result.stdout else {}
            
            return {
                "engine": "jest",
                "status": "completed",
                "tests_passed": report.get("numPassedTests", 0),
                "tests_failed": report.get("numFailedTests", 0),
                "coverage": report.get("coverageMap", {})
            }
        except Exception as e:
            return {"engine": "jest", "status": "error", "message": str(e)}
    
    def run_snyk(self) -> Dict:
        """Run Snyk security vulnerability scan"""
        try:
            result = subprocess.run(
                ["snyk", "test", "--json"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            report = json.loads(result.stdout) if result.stdout else {}
            vulnerabilities = report.get("vulnerabilities", [])
            
            return {
                "engine": "snyk",
                "status": "completed",
                "vulnerabilities_count": len(vulnerabilities),
                "critical": len([v for v in vulnerabilities if v.get("severity") == "critical"]),
                "high": len([v for v in vulnerabilities if v.get("severity") == "high"]),
                "medium": len([v for v in vulnerabilities if v.get("severity") == "medium"]),
                "low": len([v for v in vulnerabilities if v.get("severity") == "low"])
            }
        except Exception as e:
            return {"engine": "snyk", "status": "error", "message": str(e)}
    
    def run_bandit(self, file_paths: List[str]) -> Dict:
        """Run Bandit security scanner for Python"""
        try:
            result = subprocess.run(
                ["bandit", "-r", "-f", "json"] + file_paths,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            report = json.loads(result.stdout) if result.stdout else {}
            issues = report.get("results", [])
            
            return {
                "engine": "bandit",
                "status": "completed",
                "issues_count": len(issues),
                "high": len([i for i in issues if i.get("issue_severity") == "HIGH"]),
                "medium": len([i for i in issues if i.get("issue_severity") == "MEDIUM"]),
                "low": len([i for i in issues if i.get("issue_severity") == "LOW"])
            }
        except Exception as e:
            return {"engine": "bandit", "status": "error", "message": str(e)}
    
    def _format_eslint_issues(self, issues: List[Dict]) -> List[Dict]:
        """Format ESLint issues to standard format"""
        formatted = []
        for file_result in issues:
            for message in file_result.get("messages", []):
                formatted.append({
                    "file": file_result.get("filePath"),
                    "line": message.get("line"),
                    "column": message.get("column"),
                    "severity": message.get("severity"),
                    "message": message.get("message"),
                    "rule": message.get("ruleId")
                })
        return formatted
    
    def _format_pylint_issues(self, issues: List[Dict]) -> List[Dict]:
        """Format Pylint issues to standard format"""
        return [{
            "file": issue.get("path"),
            "line": issue.get("line"),
            "column": issue.get("column"),
            "severity": issue.get("type"),
            "message": issue.get("message"),
            "symbol": issue.get("symbol")
        } for issue in issues]
    
    def run_all_tests(self) -> Dict:
        """Run all applicable tests based on project type"""
        project_type = self.detect_project_type()
        results = {"project_type": project_type, "tests": {}}
        
        if project_type == "javascript":
            results["tests"]["eslint"] = self.run_eslint(["."])
            results["tests"]["jest"] = self.run_jest()
            results["tests"]["snyk"] = self.run_snyk()
            
        elif project_type == "python":
            py_files = list(self.project_path.rglob("*.py"))
            results["tests"]["pylint"] = self.run_pylint([str(f) for f in py_files])
            results["tests"]["pytest"] = self.run_pytest()
            results["tests"]["bandit"] = self.run_bandit([str(f) for f in py_files])
            results["tests"]["snyk"] = self.run_snyk()
        
        return results