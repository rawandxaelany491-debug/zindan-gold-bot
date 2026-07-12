from github import Github
import base64
import json
from datetime import datetime
from typing import Dict, List

class GitHubManager:
    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
        
    def upload_image(self, image_data: bytes, filename: str, user_id: str) -> str:
        """
        بارکردنی وێنە بۆ GitHub
        
        Returns:
            URLی وێنەکە
        """
        path = f"images/{user_id}/{datetime.now().strftime('%Y%m%d')}/{filename}"
        
        try:
            # هەوڵدان بۆ دۆزینەوەی فایل
            self.repo.get_contents(path)
            # فایل هەیە - نۆکە
            path = f"images/{user_id}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        except:
            pass
        
        # بارکردنی فایل
        self.repo.create_file(
            path=path,
            message=f"Upload image {filename} by user {user_id}",
            content=base64.b64encode(image_data).decode('utf-8')
        )
        
        return f"https://raw.githubusercontent.com/{self.repo.full_name}/main/{path}"
    
    def save_analysis(self, user_id: str, analysis: Dict, image_url: str) -> None:
        """پاشکەوتکردنی شیکاری"""
        data = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "image_url": image_url,
            "analysis": analysis
        }
        
        path = f"analyses/{user_id}/{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # هەوڵدان بۆ دۆزینەوەی فایل
            file = self.repo.get_contents(path)
            current_data = json.loads(base64.b64decode(file.content).decode('utf-8'))
            if isinstance(current_data, list):
                current_data.append(data)
            else:
                current_data = [current_data, data]
            new_content = json.dumps(current_data, indent=2)
            
            self.repo.update_file(
                path=path,
                message=f"Update analysis for user {user_id}",
                content=new_content,
                sha=file.sha
            )
        except:
            # فایل نیە - دروستی بکە
            self.repo.create_file(
                path=path,
                message=f"Create analysis file for user {user_id}",
                content=json.dumps([data], indent=2)
            )
    
    def get_user_history(self, user_id: str) -> List[Dict]:
        """هێنانی مێژووی بەکارهێنەر"""
        path = f"analyses/{user_id}/"
        try:
            contents = self.repo.get_contents(path)
            all_data = []
            for content in contents:
                file_data = json.loads(base64.b64decode(content.content).decode('utf-8'))
                all_data.extend(file_data)
            return all_data
        except:
            return []