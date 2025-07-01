"""
Test script to verify the organized Google Ads automation system works properly
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_loading():
    """Test configuration loading"""
    try:
        from config.config import SystemConfig
        config = SystemConfig()
        print("✅ Config loaded successfully")
        print(f"   Customer ID: {config.google_ads.customer_id}")
        print(f"   OpenAI Key: {config.openai.api_key[:20]}...")
        print(f"   Business: {config.landing_pages.business_name}")
        print(f"   Phone: {config.landing_pages.phone_number}")
        return True
    except Exception as e:
        print(f"❌ Config loading failed: {str(e)}")
        return False

def test_core_imports():
    """Test core module imports"""
    try:
        from core.master_orchestrator import MasterOrchestrator
        from core.keyword_research import KeywordResearcher
        from core.create_campaign import CampaignCreator
        from core.google_ads_optimizer import CampaignOptimizer
        print("✅ Core modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Core imports failed: {str(e)}")
        return False

def test_landing_page_imports():
    """Test landing page module imports"""
    try:
        from landing_pages.landing_page_manager import LandingPageManager
        from landing_pages.gpt_writer import GPTContentGenerator
        from landing_pages.image_finder import ImageFinder
        from landing_pages.html_builder_complete import build_html_page
        print("✅ Landing page modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Landing page imports failed: {str(e)}")
        return False

def test_orchestrator_initialization():
    """Test master orchestrator initialization"""
    try:
        from config.config import SystemConfig
        from core.master_orchestrator import MasterOrchestrator
        
        config = SystemConfig()
        orchestrator = MasterOrchestrator(config)
        print("✅ Master orchestrator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Orchestrator initialization failed: {str(e)}")
        return False

def test_config_validation():
    """Test configuration validation"""
    try:
        from config.config import SystemConfig
        config = SystemConfig()
        missing = config.validate()
        
        print(f"✅ Config validation completed")
        if missing:
            print(f"   ⚠️  Missing items: {len(missing)}")
            for item in missing[:3]:  # Show first 3
                print(f"      - {item}")
        else:
            print("   🎉 All configuration items present")
        
        production_ready = config.is_production_ready()
        print(f"   Production ready: {'Yes' if production_ready else 'No'}")
        return True
    except Exception as e:
        print(f"❌ Config validation failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Google Ads Automation System")
    print("=" * 50)
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Core Module Imports", test_core_imports),
        ("Landing Page Imports", test_landing_page_imports),
        ("Orchestrator Initialization", test_orchestrator_initialization),
        ("Configuration Validation", test_config_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
