"""
Project Upload and GitHub Integration
Handles file uploads, GitHub repository connections, and project analysis
"""
import os
import shutil
import requests
from typing import Dict, List, Optional
from pathlib import Path
import tempfile
import zipfile
from git import Repo

class ProjectHandler:
    """Manages project uploads and GitHub integrations"""
    
    def __init__(self, storage_path: str = "projects"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.github_token = os.getenv('GITHUB_TOKEN')
    
    def upload_project_files(self, user_id: str, project_id: str, files: List) -> Dict:
        """Handle direct file uploads"""
        try:
            project_dir = self.storage_path / user_id / project_id
            project_dir.mkdir(parents=True, exist_ok=True)
            
            uploaded_files = []
            for file in files:
                file_path = project_dir / file.filename
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(file.file, f)
                uploaded_files.append(str(file_path))
            
            return {
                'success': True,
                'project_path': str(project_dir),
                'files_uploaded': len(uploaded_files),
                'files': uploaded_files
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def upload_project_zip(self, user_id: str, project_id: str, zip_file) -> Dict:
        """Handle ZIP file upload and extraction"""
        try:
            project_dir = self.storage_path / user_id / project_id
            project_dir.mkdir(parents=True, exist_ok=True)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                shutil.copyfileobj(zip_file.file, tmp_file)
                tmp_path = tmp_file.name
            
            with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                zip_ref.extractall(project_dir)
            
            os.unlink(tmp_path)
            
            file_count = sum(1 for _ in project_dir.rglob('*') if _.is_file())
            
            return {
                'success': True,
                'project_path': str(project_dir),
                'files_extracted': file_count
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def clone_github_repo(self, user_id: str, project_id: str, repo_url: str) -> Dict:
        """Clone a GitHub repository"""
        try:
            project_dir = self.storage_path / user_id / project_id
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Add authentication if token is available
            if self.github_token and 'github.com' in repo_url:
                repo_url = repo_url.replace('https://', f'https://{self.github_token}@')
            
            Repo.clone_from(repo_url, project_dir)
            
            file_count = sum(1 for _ in project_dir.rglob('*') if _.is_file())
            
            return {
                'success': True,
                'project_path': str(project_dir),
                'files_cloned': file_count,
                'repository_url': repo_url
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_github_repo_info(self, repo_url: str) -> Dict:
        """Get GitHub repository information"""
        try:
            # Extract owner and repo name from URL
            parts = repo_url.rstrip('/').split('/')
            owner, repo = parts[-2], parts[-1].replace('.git', '')
            
            api_url = f'https://api.github.com/repos/{owner}/{repo}'
            headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
            
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'success': True,
                'name': data.get('name'),
                'description': data.get('description'),
                'language': data.get('language'),
                'stars': data.get('stargazers_count'),
                'forks': data.get('forks_count'),
                'open_issues': data.get('open_issues_count'),
                'default_branch': data.get('default_branch')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_project_structure(self, project_path: str) -> Dict:
        """Analyze project structure and detect technologies"""
        path = Path(project_path)
        
        file_counts = {}
        tech_stack = []
        
        # Count files by extension
        for file in path.rglob('*'):
            if file.is_file():
                ext = file.suffix.lower()
                file_counts[ext] = file_counts.get(ext, 0) + 1
        
        # Detect technologies
        if (path / 'package.json').exists():
            tech_stack.append('Node.js/JavaScript')
        if (path / 'requirements.txt').exists():
            tech_stack.append('Python')
        if (path / 'pom.xml').exists():
            tech_stack.append('Java/Maven')
        if (path / 'Cargo.toml').exists():
            tech_stack.append('Rust')
        if (path / 'go.mod').exists():
            tech_stack.append('Go')
        if (path / 'Dockerfile').exists():
            tech_stack.append('Docker')
        
        total_files = sum(file_counts.values())
        
        return {
            'total_files': total_files,
            'file_types': file_counts,
            'technologies': tech_stack,
            'project_size_mb': sum(f.stat().st_size for f in path.rglob('*') if f.is_file()) / (1024 * 1024)
        }
    
    def cleanup_project(self, user_id: str, project_id: str) -> Dict:
        """Delete project files"""
        try:
            project_dir = self.storage_path / user_id / project_id
            if project_dir.exists():
                shutil.rmtree(project_dir)
                return {'success': True, 'message': 'Project cleaned up'}
            return {'success': False, 'error': 'Project not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}