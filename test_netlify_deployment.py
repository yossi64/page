#!/usr/bin/env python3
"""
Test Netlify deployment functionality
"""
import sys
import os
sys.path.insert(0, '/home/ubuntu/google_ads_system_final/Landing Page Builder')

def test_netlify_deployment():
    print('🔧 Testing Netlify deployment...')
    
    try:
        from netlify_deployment import NetlifyDeployment
        from config import SystemConfig
        
        config = SystemConfig()
        netlify = NetlifyDeployment(config)
        print('✅ Netlify deployment initialized successfully')
        
        thank_you = netlify.create_thank_you_page('Air Duct Cleaning')
        print(f'✅ Thank you page created: {len(thank_you)} characters')
        
        if 'gtag' in thank_you and 'AW-8246122588' in thank_you:
            print('✅ Google Ads conversion tracking code found')
        else:
            print('❌ Google Ads conversion tracking code missing')
            return False
        
        if 'תודה רבה' in thank_you and 'dir="rtl"' in thank_you:
            print('✅ Hebrew content and RTL direction found')
        else:
            print('❌ Hebrew content or RTL direction missing')
            return False
        
        test_html = '<form action="#" method="post">'
        updated_html = netlify._update_form_action(test_html)
        if 'action="thank-you.html"' in updated_html:
            print('✅ Form action update working correctly')
        else:
            print('❌ Form action update failed')
            return False
        
        print('\n🎉 Netlify deployment test completed successfully!')
        return True
        
    except Exception as e:
        print(f'❌ Netlify deployment test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_landing_page_integration():
    print('\n🔧 Testing landing page manager integration...')
    
    try:
        from config import SystemConfig
        from landing_page_manager import LandingPageManager
        
        config = SystemConfig()
        manager = LandingPageManager(config)
        print('✅ Landing page manager with Netlify initialized')
        
        if hasattr(manager, 'netlify_deployment'):
            print('✅ Netlify deployment integrated successfully')
        else:
            print('❌ Netlify deployment not integrated')
            return False
        
        test_path = '/path/to/air_duct_cleaning.html'
        service_type = manager._extract_service_type_from_path(test_path)
        if service_type == 'Air Duct Cleaning':
            print('✅ Service type extraction working correctly')
        else:
            print(f'❌ Service type extraction failed: {service_type}')
            return False
        
        print('\n🎉 Landing page integration test completed successfully!')
        return True
        
    except Exception as e:
        print(f'❌ Landing page integration test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print('🚀 Testing Netlify deployment functionality...\n')
    
    success1 = test_netlify_deployment()
    success2 = test_landing_page_integration()
    
    if success1 and success2:
        print('\n✅ All Netlify deployment tests passed!')
        sys.exit(0)
    else:
        print('\n❌ Some Netlify deployment tests failed!')
        sys.exit(1)
