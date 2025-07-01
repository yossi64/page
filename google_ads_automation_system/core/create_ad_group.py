"""
Ad Group Creation Module for Google Ads Automation
Creates ad groups within campaigns with proper targeting
"""
import logging
from typing import Dict, Any, List, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class AdGroupCreator:
    """Creates and manages ad groups within Google Ads campaigns"""
    
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
    
    def create_ad_group(self, campaign_id: str, ad_group_name: str, 
                       cpc_bid_micros: int = 1000000) -> Dict[str, Any]:
        """Create a new ad group within a campaign"""
        try:
            ad_group_service = self.client.get_service("AdGroupService")
            ad_group_operation = self.client.get_type("AdGroupOperation")
            
            ad_group = ad_group_operation.create
            ad_group.name = ad_group_name
            ad_group.campaign = self.client.get_service("GoogleAdsService").campaign_path(
                self.config.google_ads.customer_id, campaign_id
            )
            ad_group.type_ = self.client.get_type("AdGroupTypeEnum").AdGroupType.SEARCH_STANDARD
            ad_group.status = self.client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED
            ad_group.cpc_bid_micros = cpc_bid_micros
            
            response = ad_group_service.mutate_ad_groups(
                customer_id=self.config.google_ads.customer_id,
                operations=[ad_group_operation]
            )
            
            ad_group_resource_name = response.results[0].resource_name
            ad_group_id = ad_group_resource_name.split("/")[-1]
            
            logger.info(f"Created ad group: {ad_group_name} (ID: {ad_group_id})")
            
            return {
                'success': True,
                'ad_group_id': ad_group_id,
                'ad_group_name': ad_group_name,
                'resource_name': ad_group_resource_name,
                'cpc_bid_micros': cpc_bid_micros
            }
            
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error creating ad group: {ex}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Failed to create ad group: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def create_multiple_ad_groups(self, campaign_id: str, 
                                 ad_groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple ad groups for a campaign"""
        results = []
        
        for ad_group_data in ad_groups:
            name = ad_group_data.get('name', 'Default Ad Group')
            cpc_bid = ad_group_data.get('cpc_bid_micros', 1000000)
            
            result = self.create_ad_group(campaign_id, name, cpc_bid)
            results.append(result)
            
            if not result.get('success'):
                logger.warning(f"Failed to create ad group: {name}")
        
        successful_groups = [r for r in results if r.get('success')]
        logger.info(f"Created {len(successful_groups)}/{len(ad_groups)} ad groups successfully")
        
        return results
    
    def update_ad_group_bid(self, ad_group_id: str, new_cpc_bid_micros: int) -> Dict[str, Any]:
        """Update the CPC bid for an ad group"""
        try:
            ad_group_service = self.client.get_service("AdGroupService")
            ad_group_operation = self.client.get_type("AdGroupOperation")
            
            ad_group = ad_group_operation.update
            ad_group.resource_name = self.client.get_service("GoogleAdsService").ad_group_path(
                self.config.google_ads.customer_id, ad_group_id
            )
            ad_group.cpc_bid_micros = new_cpc_bid_micros
            
            field_mask = self.client.get_type("FieldMask")
            field_mask.paths.append("cpc_bid_micros")
            ad_group_operation.update_mask = field_mask
            
            response = ad_group_service.mutate_ad_groups(
                customer_id=self.config.google_ads.customer_id,
                operations=[ad_group_operation]
            )
            
            logger.info(f"Updated ad group {ad_group_id} bid to {new_cpc_bid_micros} micros")
            
            return {
                'success': True,
                'ad_group_id': ad_group_id,
                'new_cpc_bid_micros': new_cpc_bid_micros
            }
            
        except Exception as e:
            error_msg = f"Failed to update ad group bid: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
