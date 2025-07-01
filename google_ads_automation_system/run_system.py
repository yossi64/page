"""
Main Entry Point for Google Ads Automation System
Unified system that connects campaign creation with landing page generation
"""
import logging
import sys
from datetime import datetime
from config.config import SystemConfig
from core.master_orchestrator import MasterOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the automation system"""
    print("🚀 Google Ads Automation System - Air Cleaning Tech LLC")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        config = SystemConfig()
        
        missing_config = config.validate()
        if missing_config:
            print("⚠️  Configuration Issues:")
            for item in missing_config:
                print(f"   - {item}")
            print()
        
        if not config.is_production_ready():
            print("⚠️  System running with limited functionality due to missing configuration")
            print("   Core features (campaign creation, landing pages) should still work")
            print()
        
        orchestrator = MasterOrchestrator(config)
        
        print("🎯 Available Automation Workflows:")
        print("1. Full Landing Page + Campaign Workflow (Integrated)")
        print("2. Campaign Optimization Only")
        print("3. Landing Page Creation Only")
        print("4. Performance Reporting")
        print("5. Exit")
        print()
        
        while True:
            try:
                choice = input("Select workflow (1-5): ").strip()
                
                if choice == "1":
                    print("\n🔄 Starting Integrated Landing Page + Campaign Workflow...")
                    result = orchestrator.run_full_landing_page_campaign_workflow()
                    print_workflow_results(result)
                    
                elif choice == "2":
                    print("\n🔧 Starting Campaign Optimization...")
                    from core.campaign_discovery import CampaignDiscovery
                    discovery = CampaignDiscovery(config)
                    campaigns = discovery.discover_campaigns()
                    
                    if campaigns:
                        result = orchestrator.run_campaign_optimization()
                        print_optimization_results(result)
                    else:
                        print("❌ No campaigns found to optimize")
                    
                elif choice == "3":
                    print("\n🎨 Starting Landing Page Creation...")
                    from landing_pages.landing_page_manager import LandingPageManager
                    manager = LandingPageManager(config)
                    page_path = manager.create_landing_page_interactive()
                    
                    if page_path:
                        print(f"✅ Landing page created: {page_path}")
                    else:
                        print("❌ Landing page creation failed")
                    
                elif choice == "4":
                    print("\n📊 Generating Performance Report...")
                    result = orchestrator.run_reporting_workflow()
                    print_reporting_results(result)
                    
                elif choice == "5":
                    print("\n👋 Goodbye!")
                    break
                    
                else:
                    print("❌ Invalid choice. Please select 1-5.")
                
                print("\n" + "="*60)
                
            except KeyboardInterrupt:
                print("\n\n👋 System interrupted by user. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Workflow error: {str(e)}")
                print(f"❌ Error: {str(e)}")
                print("Please try again or contact support.")
    
    except Exception as e:
        logger.error(f"System initialization failed: {str(e)}")
        print(f"❌ System startup failed: {str(e)}")
        sys.exit(1)

def print_workflow_results(result: dict):
    """Print integrated workflow results"""
    print("\n📋 Integrated Workflow Results:")
    print("-" * 40)
    
    if result.get('success'):
        print("✅ Overall Status: SUCCESS")
        
        landing_page = result.get('landing_page', {})
        if landing_page.get('success'):
            print(f"✅ Landing Page: Created successfully")
            print(f"   📄 Path: {landing_page.get('page_path', 'N/A')}")
        else:
            print(f"❌ Landing Page: {landing_page.get('error', 'Failed')}")
        
        campaign = result.get('campaign', {})
        if campaign.get('success'):
            print(f"✅ Campaign: Created successfully")
            print(f"   🎯 Campaign ID: {campaign.get('campaign_id', 'N/A')}")
            print(f"   📝 Keywords Added: {campaign.get('keywords_added', 0)}")
            print(f"   📢 Ads Created: {campaign.get('ads_created', 0)}")
        else:
            print(f"❌ Campaign: {campaign.get('error', 'Failed')}")
        
        deployment = result.get('deployment', {})
        if deployment and deployment.get('success'):
            print(f"✅ Deployment: {deployment.get('url', 'Deployed successfully')}")
        
    else:
        print("❌ Overall Status: FAILED")
        errors = result.get('errors', [])
        for error in errors:
            print(f"   ❌ {error}")

def print_optimization_results(result: dict):
    """Print optimization results"""
    print("\n📈 Optimization Results:")
    print("-" * 40)
    
    if result.get('success'):
        print("✅ Optimization completed successfully")
        
        keyword_opts = result.get('keyword_optimizations', [])
        if keyword_opts:
            print(f"🔧 Keyword Optimizations: {len(keyword_opts)}")
            for opt in keyword_opts[:3]:
                print(f"   • {opt.get('keyword', 'N/A')}: {opt.get('action', 'N/A')}")
        
        bid_adjustments = result.get('bid_adjustments', [])
        if bid_adjustments:
            print(f"💰 Bid Adjustments: {len(bid_adjustments)}")
        
        budget_recs = result.get('budget_recommendations', [])
        if budget_recs:
            print(f"💡 Budget Recommendations: {len(budget_recs)}")
    else:
        print(f"❌ Optimization failed: {result.get('error', 'Unknown error')}")

def print_reporting_results(result: dict):
    """Print reporting results"""
    print("\n📊 Reporting Results:")
    print("-" * 40)
    
    if result.get('success'):
        print("✅ Report generated successfully")
        print(f"📧 Email sent: {'Yes' if result.get('email_sent') else 'No'}")
        print(f"📈 Campaigns reported: {result.get('campaigns_reported', 0)}")
    else:
        print(f"❌ Reporting failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
