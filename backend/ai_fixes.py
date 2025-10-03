"""
AI-Powered Fix Suggestions
Uses OpenAI to generate context-aware code fixes
"""
import os
from typing import Dict, List, Optional
from openai import OpenAI

class AIFixGenerator:
    """Generates intelligent fix suggestions using AI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
        self.model = "gpt-4"
    
    def generate_fix_suggestion(self, issue: Dict) -> Dict:
        """
        Generate AI-powered fix suggestion for a code issue
        
        Args:
            issue: Dict containing severity, message, file_path, line_number, code_context
        
        Returns:
            Dict with fix_description, code_snippet, confidence_score
        """
        prompt = self._build_fix_prompt(issue)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert software engineer helping fix code issues. Provide clear, concise fixes with code examples."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            fix_text = response.choices[0].message.content
            
            return {
                'success': True,
                'fix_description': self._extract_description(fix_text),
                'code_snippet': self._extract_code(fix_text),
                'confidence_score': 0.85,
                'explanation': fix_text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_batch_fixes(self, issues: List[Dict]) -> List[Dict]:
        """Generate fixes for multiple issues"""
        fixes = []
        for issue in issues[:10]:  # Limit to 10 issues to manage API costs
            fix = self.generate_fix_suggestion(issue)
            fixes.append({
                'issue_id': issue.get('id'),
                'fix': fix
            })
        return fixes
    
    def _build_fix_prompt(self, issue: Dict) -> str:
        """Build prompt for AI fix generation"""
        return f"""
Issue Details:
- Severity: {issue.get('severity')}
- Message: {issue.get('message')}
- File: {issue.get('file_path')}
- Line: {issue.get('line_number')}

Code Context:
{issue.get('code_context', 'Not available')}

Please provide:
1. A clear explanation of the issue
2. A specific fix recommendation
3. A code snippet showing the corrected code

Format your response with sections:
EXPLANATION: ...
FIX: ...
CODE:
```
... corrected code here ...
```
"""
    
    def _extract_description(self, text: str) -> str:
        """Extract fix description from AI response"""
        if 'FIX:' in text:
            parts = text.split('FIX:')
            if len(parts) > 1:
                desc = parts[1].split('CODE:')[0].strip()
                return desc
        return text[:200]
    
    def _extract_code(self, text: str) -> str:
        """Extract code snippet from AI response"""
        if '```' in text:
            code_blocks = text.split('```')
            if len(code_blocks) > 1:
                code = code_blocks[1]
                # Remove language identifier if present
                lines = code.split('\n')
                if lines[0].strip() in ['python', 'javascript', 'java', 'typescript']:
                    code = '\n'.join(lines[1:])
                return code.strip()
        return ""
    
    def analyze_code_quality(self, code: str, language: str) -> Dict:
        """Analyze overall code quality and provide recommendations"""
        prompt = f"""
Analyze this {language} code and provide:
1. Overall quality score (0-100)
2. Top 3 improvement recommendations
3. Security concerns if any

Code:
```{language}
{code}
```
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a code quality expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'success': True,
                'analysis': analysis,
                'timestamp': str(os.times())
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }