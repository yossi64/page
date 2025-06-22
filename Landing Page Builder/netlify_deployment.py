#!/usr/bin/env python3
"""
Netlify deployment solution for landing pages with conversion tracking
"""
import os
import requests
import json
import base64
import tempfile
import zipfile
from typing import Optional

class NetlifyDeployment:
    """Simple Netlify deployment for landing pages with conversion tracking"""
    
    def __init__(self, config=None):
        self.config = config
        self.netlify_token = None
        
    def create_thank_you_page(self, service_type: str) -> str:
        """Create a professional thank you page with Google Ads conversion tracking"""
        thank_you_html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>תודה - {service_type}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .thank-you-container {{
            background: white;
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
            margin: 20px;
            animation: slideIn 0.8s ease-out;
        }}
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .success-icon {{
            font-size: 80px;
            color: #4CAF50;
            margin-bottom: 30px;
            animation: bounce 1s ease-in-out;
        }}
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-10px); }}
            60% {{ transform: translateY(-5px); }}
        }}
        h1 {{
            color: #333;
            font-size: 2.5em;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        .message {{
            font-size: 1.3em;
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .contact-info {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }}
        .phone {{
            font-size: 2em;
            color: #007bff;
            font-weight: bold;
            margin: 20px 0;
            text-decoration: none;
        }}
        .phone:hover {{
            color: #0056b3;
        }}
        .next-steps {{
            background: #e3f2fd;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #2196F3;
        }}
        .next-steps h3 {{
            color: #1976D2;
            margin-top: 0;
        }}
        .next-steps ul {{
            text-align: right;
            list-style: none;
            padding: 0;
        }}
        .next-steps li {{
            margin: 10px 0;
            padding: 5px 0;
        }}
        .footer {{
            margin-top: 30px;
            color: #888;
            font-size: 0.9em;
        }}
    </style>
    
    <!-- Google Ads Conversion Tracking -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-8246122588"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'AW-8246122588');
        
        // Track form submission conversion
        gtag('event', 'conversion', {{
            'send_to': 'AW-8246122588/form_submit',
            'value': 1.0,
            'currency': 'USD'
        }});
        
        // Track page view conversion
        gtag('event', 'conversion', {{
            'send_to': 'AW-8246122588/page_view'
        }});
        
        console.log('Google Ads conversion tracking loaded successfully');
    </script>
    
    <!-- Facebook Pixel (optional) -->
    <script>
        !function(f,b,e,v,n,t,s)
        {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', 'YOUR_PIXEL_ID');
        fbq('track', 'Lead');
    </script>
</head>
<body>
    <div class="thank-you-container">
        <div class="success-icon">✅</div>
        <h1>תודה רבה!</h1>
        
        <div class="message">
            הפנייה שלך התקבלה בהצלחה!<br>
            נציג שלנו יחזור אליך בהקדם האפשרי.
        </div>
        
        <div class="contact-info">
            <h3>פרטי יצירת קשר</h3>
            <a href="tel:+12108730584" class="phone">📞 (210) 873-0584</a>
            <p>זמינים 24/7 לשירותי חירום</p>
        </div>
        
        <div class="next-steps">
            <h3>מה קורה עכשיו?</h3>
            <ul>
                <li>✓ נציג יצור איתך קשר תוך 15 דקות</li>
                <li>✓ נקבע תור לבדיקה חינמית</li>
                <li>✓ תקבל הצעת מחיר מפורטת</li>
                <li>✓ שירות מקצועי ומהיר</li>
            </ul>
        </div>
        
        <div class="footer">
            <strong>Air Cleaning Tech LLC</strong><br>
            שירותי {service_type} מקצועיים בסן אנטוניו<br>
            <small>מורשה ומבוטח • אחריות מלאה על העבודה</small>
        </div>
    </div>
    
    <script>
        // Additional conversion tracking on page load
        setTimeout(function() {{
            gtag('event', 'conversion', {{
                'send_to': 'AW-8246122588/thank_you_page',
                'value': 1.0,
                'currency': 'USD'
            }});
        }}, 1000);
    </script>
</body>
</html>"""
        return thank_you_html
    
    def deploy_to_netlify(self, landing_page_path: str, service_type: str, site_name: Optional[str] = None) -> Optional[str]:
        """Deploy landing page and thank you page to Netlify"""
        if not self.netlify_token:
            print("⚠️ נדרש Netlify API token")
            token = input("הכנס Netlify API token (או Enter לדילוג): ").strip()
            if not token:
                print("🔄 משתמש בשירות הפריסה המובנה...")
                return self._deploy_using_builtin(landing_page_path, service_type)
            self.netlify_token = token
        
        try:
            print("🚀 מעלה דפים ל-Netlify...")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                with open(landing_page_path, 'r', encoding='utf-8') as f:
                    landing_content = f.read()
                
                landing_content = self._update_form_action(landing_content)
                
                with open(os.path.join(temp_dir, 'index.html'), 'w', encoding='utf-8') as f:
                    f.write(landing_content)
                
                thank_you_content = self.create_thank_you_page(service_type)
                with open(os.path.join(temp_dir, 'thank-you.html'), 'w', encoding='utf-8') as f:
                    f.write(thank_you_content)
                
                zip_path = os.path.join(temp_dir, 'site.zip')
                with zipfile.ZipFile(zip_path, 'w') as zip_file:
                    zip_file.write(os.path.join(temp_dir, 'index.html'), 'index.html')
                    zip_file.write(os.path.join(temp_dir, 'thank-you.html'), 'thank-you.html')
                
                headers = {
                    'Authorization': f'Bearer {self.netlify_token}',
                    'Content-Type': 'application/zip'
                }
                
                with open(zip_path, 'rb') as zip_data:
                    response = requests.post(
                        'https://api.netlify.com/api/v1/sites',
                        headers=headers,
                        data=zip_data
                    )
                
                if response.status_code == 201:
                    site_data = response.json()
                    site_url = site_data.get('ssl_url') or site_data.get('url')
                    print(f"✅ דפים הועלו בהצלחה ל-Netlify!")
                    print(f"🌐 דף נחיתה: {site_url}")
                    print(f"🌐 דף תודה: {site_url}/thank-you.html")
                    return site_url
                else:
                    print(f"❌ שגיאה בהעלאה ל-Netlify: {response.status_code}")
                    print(f"Response: {response.text}")
                    return self._deploy_using_builtin(landing_page_path, service_type)
                    
        except Exception as e:
            print(f"❌ שגיאה בהעלאה ל-Netlify: {e}")
            return self._deploy_using_builtin(landing_page_path, service_type)
    
    def _deploy_using_builtin(self, landing_page_path: str, service_type: str) -> Optional[str]:
        """Fallback to built-in deployment service"""
        try:
            print("🔄 משתמש בשירות הפריסה המובנה...")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                with open(landing_page_path, 'r', encoding='utf-8') as f:
                    landing_content = f.read()
                
                landing_content = self._update_form_action(landing_content)
                
                with open(os.path.join(temp_dir, 'index.html'), 'w', encoding='utf-8') as f:
                    f.write(landing_content)
                
                thank_you_content = self.create_thank_you_page(service_type)
                with open(os.path.join(temp_dir, 'thank-you.html'), 'w', encoding='utf-8') as f:
                    f.write(thank_you_content)
                
                try:
                    from deploy_frontend import deploy_frontend
                    deployed_url = deploy_frontend(temp_dir)
                    
                    if deployed_url:
                        print(f"✅ דפים הועלו בהצלחה!")
                        print(f"🌐 דף נחיתה: {deployed_url}")
                        print(f"🌐 דף תודה: {deployed_url}/thank-you.html")
                        return deployed_url
                    else:
                        print("❌ שגיאה בהעלאה")
                        return None
                        
                except ImportError:
                    print("⚠️ שירות הפריסה המובנה לא זמין")
                    return None
                    
        except Exception as e:
            print(f"❌ שגיאה בפריסה: {e}")
            return None
    
    def _update_form_action(self, html_content: str) -> str:
        """Update form action to point to thank you page"""
        html_content = html_content.replace('action="#"', 'action="thank-you.html"')
        html_content = html_content.replace("action='#'", "action='thank-you.html'")
        html_content = html_content.replace('action=""', 'action="thank-you.html"')
        html_content = html_content.replace("action=''", "action='thank-you.html'")
        
        if 'method=' not in html_content and '<form' in html_content:
            html_content = html_content.replace('<form', '<form method="GET"')
        
        return html_content
    
    def deploy_interactive(self, landing_page_path: str, service_type: str) -> Optional[str]:
        """Interactive deployment with simple options"""
        print("\n🚀 פריסה ל-Netlify:")
        print("1. פריסה אוטומטית (מומלץ)")
        print("2. ביטול")
        
        while True:
            choice = input("\nבחר אפשרות (1-2): ").strip()
            
            if choice == "1":
                return self.deploy_to_netlify(landing_page_path, service_type)
            elif choice == "2":
                print("✅ הדף נשמר מקומית בלבד")
                return None
            else:
                print("❌ בחירה לא תקינה, נסה שוב")
