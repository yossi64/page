#!/usr/bin/env python3
"""
Landing Page Deployment Manager
Supports both regular server deployment and Netlify API deployment
"""
import os
import requests
import json
import base64
from typing import Optional, Dict, Any
import zipfile
import tempfile

class DeploymentManager:
    """Manages deployment of landing pages to various platforms"""
    
    def __init__(self, config=None):
        self.config = config
        self.netlify_api_token = None  # Will be set by user if needed
        self.server_endpoint = None    # Will be set by user if needed
        
    def deploy_to_netlify(self, html_file_path: str, site_name: Optional[str] = None) -> Optional[str]:
        """Deploy landing page to Netlify using their API"""
        if not self.netlify_api_token:
            print("⚠️ Netlify API token not configured")
            return None
            
        try:
            print("🚀 מעלה דף נחיתה ל-Netlify...")
            
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                with zipfile.ZipFile(temp_zip.name, 'w') as zip_file:
                    zip_file.writestr('index.html', html_content)
                
                headers = {
                    'Authorization': f'Bearer {self.netlify_api_token}',
                    'Content-Type': 'application/zip'
                }
                
                with open(temp_zip.name, 'rb') as zip_data:
                    response = requests.post(
                        'https://api.netlify.com/api/v1/sites',
                        headers=headers,
                        data=zip_data
                    )
                
                os.unlink(temp_zip.name)  # Clean up temp file
                
                if response.status_code == 201:
                    site_data = response.json()
                    site_url = site_data.get('ssl_url') or site_data.get('url')
                    print(f"✅ דף נחיתה הועלה בהצלחה ל-Netlify: {site_url}")
                    return site_url
                else:
                    print(f"❌ שגיאה בהעלאה ל-Netlify: {response.status_code}")
                    print(f"Response: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ שגיאה בהעלאה ל-Netlify: {e}")
            return None
    
    def deploy_to_server(self, html_file_path: str, endpoint_url: Optional[str] = None) -> Optional[str]:
        """Deploy landing page to a regular server endpoint"""
        if not endpoint_url and not self.server_endpoint:
            print("⚠️ Server endpoint not configured")
            return None
            
        endpoint = endpoint_url or self.server_endpoint
        
        try:
            print("🚀 מעלה דף נחיתה לשרת...")
            
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            files = {'file': ('index.html', html_content, 'text/html')}
            
            response = requests.post(endpoint, files=files)
            
            if response.status_code == 200:
                result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'url': response.text.strip()}
                deployed_url = result.get('url', endpoint)
                print(f"✅ דף נחיתה הועלה בהצלחה לשרת: {deployed_url}")
                return deployed_url
            else:
                print(f"❌ שגיאה בהעלאה לשרת: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ שגיאה בהעלאה לשרת: {e}")
            return None
    
    def deploy_using_builtin_service(self, html_file_path: str) -> Optional[str]:
        """Deploy using Devin's built-in deployment service"""
        try:
            print("🚀 מעלה דף נחיתה באמצעות שירות הפריסה המובנה...")
            
            html_dir = os.path.dirname(html_file_path)
            
            from deploy_frontend import deploy_frontend
            deployed_url = deploy_frontend(html_dir)
            
            if deployed_url:
                print(f"✅ דף נחיתה הועלה בהצלחה: {deployed_url}")
                return deployed_url
            else:
                print("❌ שגיאה בהעלאה באמצעות שירות הפריסה המובנה")
                return None
                
        except ImportError:
            print("⚠️ שירות הפריסה המובנה לא זמין")
            return None
        except Exception as e:
            print(f"❌ שגיאה בהעלאה באמצעות שירות הפריסה המובנה: {e}")
            return None
    
    def get_deployment_options(self) -> Dict[str, str]:
        """Get available deployment options"""
        options = {
            "1": "שמירה מקומית בלבד (ברירת מחדל)",
            "2": "העלאה לשרת (נדרש endpoint)",
            "3": "העלאה ל-Netlify (נדרש API token)",
            "4": "שירות פריסה מובנה (אוטומטי)"
        }
        return options
    
    def configure_netlify(self, api_token: str):
        """Configure Netlify API token"""
        self.netlify_api_token = api_token
        print("✅ Netlify API token configured")
    
    def configure_server(self, endpoint_url: str):
        """Configure server endpoint"""
        self.server_endpoint = endpoint_url
        print(f"✅ Server endpoint configured: {endpoint_url}")
    
    def deploy_interactive(self, html_file_path: str) -> Optional[str]:
        """Interactive deployment with user choice"""
        print("\n🚀 אפשרויות פריסה:")
        print("-" * 30)
        
        options = self.get_deployment_options()
        for key, value in options.items():
            print(f"{key}. {value}")
        
        while True:
            choice = input("\nבחר אפשרות פריסה (1-4): ").strip()
            
            if choice == "1":
                print("✅ הדף נשמר מקומית בלבד")
                return html_file_path
            
            elif choice == "2":
                endpoint = input("הכנס URL של השרת: ").strip()
                if endpoint:
                    self.configure_server(endpoint)
                    return self.deploy_to_server(html_file_path)
                else:
                    print("❌ חובה להכניס URL שרת")
                    continue
            
            elif choice == "3":
                token = input("הכנס Netlify API token: ").strip()
                if token:
                    self.configure_netlify(token)
                    return self.deploy_to_netlify(html_file_path)
                else:
                    print("❌ חובה להכניס Netlify API token")
                    continue
            
            elif choice == "4":
                return self.deploy_using_builtin_service(html_file_path)
            
            else:
                print("❌ בחירה לא תקינה, נסה שוב")
