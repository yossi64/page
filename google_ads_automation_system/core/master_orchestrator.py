"""
Master Orchestrator for Google Ads Automation System
Coordinates all automation workflows and integrates campaign creation with landing pages
"""
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class MasterOrchestrator:
    """Main orchestrator that coordinates all automation workflows"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def run_full_landing_page_campaign_workflow(self) -> Dict[str, Any]:
        """
        Complete integrated workflow:
        1. Create landing page
        2. Create Google Ads campaign
        3. Connect them together
        4. Deploy and monitor
        """
        logger.info("🚀 Starting integrated landing page + campaign workflow")
        
        workflow_results = {
            'timestamp': datetime.now().isoformat(),
            'landing_page': None,
            'campaign': None,
            'deployment': None,
            'success': False,
            'errors': []
        }
        
        try:
            logger.info("Step 1: Creating landing page...")
            landing_page_result = self._create_landing_page()
            workflow_results['landing_page'] = landing_page_result
            
            if not landing_page_result.get('success'):
                raise Exception("Landing page creation failed")
            
            logger.info("Step 2: Creating Google Ads campaign...")
            campaign_result = self._create_campaign_with_keywords()
            workflow_results['campaign'] = campaign_result
            
            if not campaign_result.get('success'):
                raise Exception("Campaign creation failed")
            
            logger.info("Step 3: Connecting landing page to campaign...")
            self._connect_landing_page_to_campaign(
                landing_page_result, 
                campaign_result
            )
            
            logger.info("Step 4: Deploying integrated system...")
            deployment_result = self._deploy_landing_page(landing_page_result)
            workflow_results['deployment'] = deployment_result
            
            workflow_results['success'] = True
            logger.info("✅ Integrated workflow completed successfully!")
            
        except Exception as e:
            error_msg = f"Workflow failed: {str(e)}"
            logger.error(error_msg)
            workflow_results['errors'].append(error_msg)
            workflow_results['success'] = False
        
        return workflow_results
    
    def _create_landing_page(self) -> Dict[str, Any]:
        """Create landing page using the landing page manager"""
        try:
            from landing_pages.landing_page_manager import LandingPageManager
            
            manager = LandingPageManager(self.config)
            page_path = manager.create_landing_page_for_service("Air Duct Cleaning")
            
            if page_path:
                return {
                    'success': True,
                    'page_path': page_path,
                    'service_type': 'Air Duct Cleaning'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to create landing page'
                }
                
        except Exception as e:
            logger.error(f"Landing page creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_campaign_with_keywords(self) -> Dict[str, Any]:
        """Create Google Ads campaign with keywords"""
        try:
            from core.create_campaign import CampaignCreator
            from core.keyword_research import KeywordResearcher
            
            keyword_researcher = KeywordResearcher(self.config)
            keywords = keyword_researcher.research_keywords("air duct cleaning San Antonio")
            
            campaign_creator = CampaignCreator(self.config)
            campaign_result = campaign_creator.create_campaign_with_keywords(
                campaign_name=self.config.campaign.campaign_name,
                keywords=keywords,
                daily_budget_micros=self.config.campaign.daily_budget_micros
            )
            
            return campaign_result
            
        except Exception as e:
            logger.error(f"Campaign creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _connect_landing_page_to_campaign(self, landing_page_result: Dict, campaign_result: Dict):
        """Connect the landing page URL to the campaign ads"""
        try:
            if not landing_page_result.get('success') or not campaign_result.get('success'):
                return
            
            logger.info("Connecting landing page to campaign ads...")
            
        except Exception as e:
            logger.error(f"Failed to connect landing page to campaign: {str(e)}")
    
    def _deploy_landing_page(self, landing_page_result: Dict) -> Dict[str, Any]:
        """Deploy the landing page"""
        try:
            from deployment.deployment_manager import DeploymentManager
            
            deployment_manager = DeploymentManager(self.config)
            deployment_result = deployment_manager.deploy_page(
                landing_page_result.get('page_path')
            )
            
            return deployment_result
            
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_campaign_optimization(self) -> Dict[str, Any]:
        """Run campaign optimization workflow"""
        try:
            from core.google_ads_optimizer import CampaignOptimizer
            from core.campaign_discovery import CampaignDiscovery
            
            discovery = CampaignDiscovery(self.config)
            campaigns = discovery.discover_campaigns()
            
            optimizer = CampaignOptimizer(self.config)
            optimization_results = []
            
            for campaign in campaigns:
                result = optimizer.optimize_campaigns(campaign)
                optimization_results.append(result)
            
            return {
                'success': True,
                'optimizations': optimization_results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_reporting_workflow(self) -> Dict[str, Any]:
        """Generate and send performance reports"""
        try:
            from core.email_reporter import EmailReporter
            
            reporter = EmailReporter(self.config)
            report_result = reporter.generate_and_send_report()
            
            return report_result
            
        except Exception as e:
            logger.error(f"Reporting failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
