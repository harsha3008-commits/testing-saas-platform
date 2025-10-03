"""
Test Report Generator
Creates comprehensive PDF reports with charts and visualizations
"""
from typing import Dict, List
from datetime import datetime
import json
from pathlib import Path

class ReportGenerator:
    """Generates comprehensive test reports"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_markdown_report(self, test_run: Dict) -> str:
        """Generate markdown format report"""
        report = f"""# Test Report - {test_run.get('project_name')}

## Executive Summary
- **Test Run ID:** {test_run.get('id')}
- **Status:** {test_run.get('status')}
- **Overall Score:** {test_run.get('overall_score')}/100
- **Production Ready:** {'✅ Yes' if test_run.get('production_ready') else '❌ No'}
- **Started:** {test_run.get('started_at')}
- **Completed:** {test_run.get('completed_at')}
- **Duration:** {test_run.get('duration_seconds')}s

## Test Categories

"""
        
        for category in test_run.get('categories', []):
            report += f"""### {category.get('name')}
- **Score:** {category.get('score')}/100
- **Status:** {category.get('status')}
- **Tests Passed:** {category.get('tests_passed')}
- **Tests Failed:** {category.get('tests_failed')}

"""
            
            if category.get('issues'):
                report += "#### Issues Found\n"
                for issue in category.get('issues')[:5]:
                    report += f"- **{issue.get('severity').upper()}:** {issue.get('message')}\n"
                    report += f"  - File: `{issue.get('file_path')}:{issue.get('line_number')}`\n"
                report += "\n"
        
        report += """## Recommendations

"""
        
        recommendations = self._generate_recommendations(test_run)
        for rec in recommendations:
            report += f"- {rec}\n"
        
        return report
    
    def generate_html_report(self, test_run: Dict) -> str:
        """Generate HTML format report with styling"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report - {test_run.get('project_name')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1E2A38; color: white; padding: 20px; border-radius: 8px; }}
        .score {{ font-size: 48px; font-weight: bold; color: #2F80ED; }}
        .category {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 8px; }}
        .issue {{ border-left: 4px solid #EB5757; padding: 10px; margin: 5px 0; }}
        .critical {{ border-color: #EB5757; }}
        .high {{ border-color: #F2C94C; }}
        .medium {{ border-color: #2F80ED; }}
        .low {{ border-color: #27AE60; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Test Report: {test_run.get('project_name')}</h1>
        <div class="score">{test_run.get('overall_score')}/100</div>
        <p>Production Ready: {'✅ Yes' if test_run.get('production_ready') else '❌ No'}</p>
    </div>
    
    <h2>Test Categories</h2>
"""
        
        for category in test_run.get('categories', []):
            html += f"""
    <div class="category">
        <h3>{category.get('name')} - {category.get('score')}/100</h3>
        <p>Passed: {category.get('tests_passed')} | Failed: {category.get('tests_failed')}</p>
"""
            
            for issue in category.get('issues', [])[:5]:
                severity_class = issue.get('severity', 'low').lower()
                html += f"""
        <div class="issue {severity_class}">
            <strong>{issue.get('severity').upper()}:</strong> {issue.get('message')}<br>
            <small>File: {issue.get('file_path')}:{issue.get('line_number')}</small>
        </div>
"""
            
            html += "    </div>\n"
        
        html += """
</body>
</html>
"""
        return html
    
    def generate_json_report(self, test_run: Dict) -> str:
        """Generate JSON format report"""
        return json.dumps(test_run, indent=2)
    
    def save_report(self, test_run: Dict, format: str = 'markdown') -> str:
        """Save report to file"""
        report_id = test_run.get('id')
        
        if format == 'markdown':
            content = self.generate_markdown_report(test_run)
            filename = f"{report_id}.md"
        elif format == 'html':
            content = self.generate_html_report(test_run)
            filename = f"{report_id}.html"
        elif format == 'json':
            content = self.generate_json_report(test_run)
            filename = f"{report_id}.json"
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        filepath = self.output_dir / filename
        filepath.write_text(content, encoding='utf-8')
        
        return str(filepath)
    
    def _generate_recommendations(self, test_run: Dict) -> List[str]:
        """Generate actionable recommendations based on test results"""
        recommendations = []
        
        overall_score = test_run.get('overall_score', 0)
        
        if overall_score < 70:
            recommendations.append("Overall score is below 70. Address critical issues before production deployment.")
        
        for category in test_run.get('categories', []):
            if category.get('score', 0) < 60:
                recommendations.append(f"Improve {category.get('name')} - current score is {category.get('score')}/100")
        
        if not test_run.get('production_ready'):
            recommendations.append("Project is not production-ready. Review and fix all critical issues.")
        
        return recommendations or ["Great job! All tests passed successfully."]
    
    def create_summary_dashboard(self, test_runs: List[Dict]) -> Dict:
        """Create dashboard summary from multiple test runs"""
        total_runs = len(test_runs)
        passed_runs = sum(1 for r in test_runs if r.get('status') == 'passed')
        failed_runs = sum(1 for r in test_runs if r.get('status') == 'failed')
        avg_score = sum(r.get('overall_score', 0) for r in test_runs) / total_runs if total_runs > 0 else 0
        
        return {
            'total_runs': total_runs,
            'passed_runs': passed_runs,
            'failed_runs': failed_runs,
            'pass_rate': (passed_runs / total_runs * 100) if total_runs > 0 else 0,
            'average_score': round(avg_score, 2)
        }