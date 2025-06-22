#!/usr/bin/env python3
"""
Test deployment integration with real deploy_frontend command
"""
import sys
import os
import tempfile
import shutil

sys.path.insert(0, '/home/ubuntu/google_ads_system_final/Landing Page Builder')

def test_deployment_with_real_service():
    """Test deployment using the actual deploy_frontend command"""
    print('🔧 Testing deployment with real service...')
    
    try:
        from simple_deployment import SimpleDeployment
        
        with tempfile.TemporaryDirectory() as temp_dir:
            test_html = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Test Landing Page</title>
</head>
<body>
    <h1>דף נחיתה לבדיקה</h1>
    <form action="#" method="post">
        <input type="text" name="name" placeholder="שם">
        <input type="email" name="email" placeholder="אימייל">
        <button type="submit">שלח</button>
    </form>
</body>
</html>"""
            
            test_file = os.path.join(temp_dir, 'test_landing.html')
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_html)
            
            deployment = SimpleDeployment()
            deployed_url = deployment.deploy_landing_page_with_thank_you(
                test_file, 
                "Air Duct Cleaning"
            )
            
            if deployed_url:
                print(f'✅ Deployment successful: {deployed_url}')
                return True
            else:
                print('❌ Deployment failed')
                return False
                
    except Exception as e:
        print(f'❌ Deployment test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_netlify_integration():
    """Test Netlify deployment integration"""
    print('\n🔧 Testing Netlify integration...')
    
    try:
        from netlify_deployment import NetlifyDeployment
        from config import SystemConfig
        
        config = SystemConfig()
        netlify = NetlifyDeployment(config)
        
        thank_you = netlify.create_thank_you_page('Air Duct Cleaning')
        
        if 'תודה רבה' in thank_you and 'gtag' in thank_you:
            print('✅ Netlify thank you page creation working')
            return True
        else:
            print('❌ Netlify thank you page creation failed')
            return False
            
    except Exception as e:
        print(f'❌ Netlify integration test failed: {e}')
        return False

if __name__ == "__main__":
    print('🚀 Testing deployment integration...\n')
    
    success1 = test_deployment_with_real_service()
    success2 = test_netlify_integration()
    
    if success1 and success2:
        print('\n✅ All deployment integration tests passed!')
        sys.exit(0)
    else:
        print('\n❌ Some deployment integration tests failed!')
        sys.exit(1)
