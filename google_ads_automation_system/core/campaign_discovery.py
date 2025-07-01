"""
Campaign Discovery Module for Google Ads Automation
Discovers existing campaigns and their performance data
"""
import logging
from typing import Dict, Any, List
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class CampaignDiscovery:
    """Discovers and analyzes existing Google Ads campaigns"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> GoogleAdsClient:
        """Initialize Google Ads client"""
        try:
            credentials = {
                "developer_token": self.config.google_ads.developer_token,
                "client_id": self.config.google_ads.client_id,
                "client_secret": self.config.google_ads.client_secret,
                "refresh_token": self.config.google_ads.refresh_token,
                "use_proto_plus": self.config.google_ads.use_proto_plus,
            }
            
            if self.config.google_ads.login_customer_id:
                credentials["login_customer_id"] = self.config.google_ads.login_customer_id
            
            return GoogleAdsClient.load_from_dict(credentials)
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Ads client: {str(e)}")
            raise
    
    def discover_campaigns(self) -> List[Dict[str, Any]]:
        """Discover all campaigns in the account"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = """
                SELECT 
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign.advertising_channel_type,
                    campaign.campaign_budget,
                    campaign.start_date,
                    campaign.end_date,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.conversions,
                    metrics.ctr,
                    metrics.average_cpc
                FROM campaign 
                WHERE segments.date DURING LAST_30_DAYS
                ORDER BY metrics.cost_micros DESC
            """
            
            response = ga_service.search(
                customer_id=self.config.google_ads.customer_id,
                query=query
            )
            
            campaigns = []
            for row in response:
                campaign_data = {
                    'campaign': {
                        'campaign_id': row.campaign.id,
                        'name': row.campaign.name,
                        'status': row.campaign.status.name,
                        'type': row.campaign.advertising_channel_type.name,
                        'budget': row.campaign.campaign_budget,
                        'start_date': row.campaign.start_date,
                        'end_date': row.campaign.end_date
                    },
                    'metrics': {
                        'impressions': row.metrics.impressions,
                        'clicks': row.metrics.clicks,
                        'cost_micros': row.metrics.cost_micros,
                        'cost_dollars': row.metrics.cost_micros / 1_000_000,
                        'conversions': row.metrics.conversions,
                        'ctr': row.metrics.ctr,
                        'average_cpc': row.metrics.average_cpc
                    }
                }
                campaigns.append(campaign_data)
            
            logger.info(f"Discovered {len(campaigns)} campaigns")
            return campaigns
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            return []
        except Exception as e:
            logger.error(f"Campaign discovery failed: {str(e)}")
            return []
    
    def get_campaign_details(self, campaign_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific campaign"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = f"""
                SELECT 
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign.advertising_channel_type,
                    campaign.bidding_strategy_type,
                    campaign.target_cpa.target_cpa_micros,
                    campaign.target_roas.target_roas,
                    campaign.maximize_conversions.target_cpa_micros,
                    campaign_budget.amount_micros,
                    campaign_budget.delivery_method,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.conversions,
                    metrics.conversions_value,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.cost_per_conversion
                FROM campaign 
                WHERE campaign.id = {campaign_id}
                AND segments.date DURING LAST_30_DAYS
            """
            
            response = ga_service.search(
                customer_id=self.config.google_ads.customer_id,
                query=query
            )
            
            for row in response:
                return {
                    'campaign_id': row.campaign.id,
                    'name': row.campaign.name,
                    'status': row.campaign.status.name,
                    'type': row.campaign.advertising_channel_type.name,
                    'bidding_strategy': row.campaign.bidding_strategy_type.name,
                    'budget_micros': row.campaign_budget.amount_micros,
                    'budget_dollars': row.campaign_budget.amount_micros / 1_000_000,
                    'delivery_method': row.campaign_budget.delivery_method.name,
                    'performance': {
                        'impressions': row.metrics.impressions,
                        'clicks': row.metrics.clicks,
                        'cost_micros': row.metrics.cost_micros,
                        'cost_dollars': row.metrics.cost_micros / 1_000_000,
                        'conversions': row.metrics.conversions,
                        'conversion_value': row.metrics.conversions_value,
                        'ctr': row.metrics.ctr,
                        'avg_cpc': row.metrics.average_cpc,
                        'cost_per_conversion': row.metrics.cost_per_conversion
                    }
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Failed to get campaign details: {str(e)}")
            return {}
