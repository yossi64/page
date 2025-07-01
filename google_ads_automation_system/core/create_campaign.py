"""
Campaign Creation Module for Google Ads Automation
Handles campaign, ad group, and ad creation
"""
import logging
from typing import Dict, Any, List
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class CampaignCreator:
    """Handles Google Ads campaign creation"""
    
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
    
    def create_campaign_with_keywords(self, campaign_name: str, keywords: List[Dict[str, Any]], daily_budget_micros: int) -> Dict[str, Any]:
        """Create complete campaign with ad groups and keywords"""
        try:
            logger.info(f"Creating campaign: {campaign_name}")
            
            campaign_result = self._create_campaign(campaign_name, daily_budget_micros)
            if not campaign_result.get('success'):
                return campaign_result
            
            campaign_id = campaign_result['campaign_id']
            
            ad_group_result = self._create_ad_group(campaign_id, "Air Duct Cleaning")
            if not ad_group_result.get('success'):
                return ad_group_result
            
            ad_group_id = ad_group_result['ad_group_id']
            
            keywords_result = self._add_keywords_to_ad_group(ad_group_id, keywords)
            ads_result = self._create_ads_for_ad_group(ad_group_id)
            
            return {
                'success': True,
                'campaign_id': campaign_id,
                'ad_group_id': ad_group_id,
                'keywords_added': keywords_result.get('keywords_added', 0),
                'ads_created': ads_result.get('ads_created', 0),
                'campaign_name': campaign_name
            }
            
        except Exception as e:
            logger.error(f"Campaign creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_campaign(self, campaign_name: str, daily_budget_micros: int) -> Dict[str, Any]:
        """Create Google Ads campaign"""
        try:
            campaign_budget_service = self.client.get_service("CampaignBudgetService")
            campaign_service = self.client.get_service("CampaignService")
            
            budget_operation = self.client.get_type("CampaignBudgetOperation")
            budget = budget_operation.create
            budget.name = f"{campaign_name} Budget"
            budget.delivery_method = self.client.enums.BudgetDeliveryMethodEnum.STANDARD
            budget.amount_micros = daily_budget_micros
            
            budget_response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=self.config.google_ads.customer_id,
                operations=[budget_operation]
            )
            
            budget_resource_name = budget_response.results[0].resource_name
            
            campaign_operation = self.client.get_type("CampaignOperation")
            campaign = campaign_operation.create
            campaign.name = campaign_name
            campaign.advertising_channel_type = self.client.enums.AdvertisingChannelTypeEnum.SEARCH
            campaign.status = self.client.enums.CampaignStatusEnum.PAUSED
            campaign.campaign_budget = budget_resource_name
            campaign.network_settings.target_google_search = True
            campaign.network_settings.target_search_network = True
            
            geo_target_service = self.client.get_service("GeoTargetConstantService")
            geo_target_constant = geo_target_service.suggest_geo_target_constants(
                locale="en",
                country_code="US",
                location_names=["San Antonio, TX"]
            )
            
            if geo_target_constant.geo_target_constant_suggestions:
                geo_target = geo_target_constant.geo_target_constant_suggestions[0].geo_target_constant
                campaign.geo_target_type_setting.positive_geo_target_type = (
                    self.client.enums.PositiveGeoTargetTypeEnum.PRESENCE_OR_INTEREST
                )
                
                geo_criterion = campaign.geo_targets.add()
                geo_criterion.geo_target_constant = geo_target.resource_name
            
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=self.config.google_ads.customer_id,
                operations=[campaign_operation]
            )
            
            campaign_resource_name = campaign_response.results[0].resource_name
            campaign_id = campaign_resource_name.split('/')[-1]
            
            logger.info(f"Campaign created successfully: {campaign_id}")
            
            return {
                'success': True,
                'campaign_id': campaign_id,
                'campaign_resource_name': campaign_resource_name
            }
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            return {
                'success': False,
                'error': f"Google Ads API error: {ex}"
            }
        except Exception as e:
            logger.error(f"Campaign creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_ad_group(self, campaign_id: str, ad_group_name: str) -> Dict[str, Any]:
        """Create ad group within campaign"""
        try:
            ad_group_service = self.client.get_service("AdGroupService")
            
            ad_group_operation = self.client.get_type("AdGroupOperation")
            ad_group = ad_group_operation.create
            ad_group.name = ad_group_name
            ad_group.campaign = f"customers/{self.config.google_ads.customer_id}/campaigns/{campaign_id}"
            ad_group.type_ = self.client.enums.AdGroupTypeEnum.SEARCH_STANDARD
            ad_group.status = self.client.enums.AdGroupStatusEnum.ENABLED
            ad_group.cpc_bid_micros = 2000000  # $2.00
            
            ad_group_response = ad_group_service.mutate_ad_groups(
                customer_id=self.config.google_ads.customer_id,
                operations=[ad_group_operation]
            )
            
            ad_group_resource_name = ad_group_response.results[0].resource_name
            ad_group_id = ad_group_resource_name.split('/')[-1]
            
            logger.info(f"Ad group created successfully: {ad_group_id}")
            
            return {
                'success': True,
                'ad_group_id': ad_group_id,
                'ad_group_resource_name': ad_group_resource_name
            }
            
        except Exception as e:
            logger.error(f"Ad group creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _add_keywords_to_ad_group(self, ad_group_id: str, keywords: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add keywords to ad group"""
        try:
            ad_group_criterion_service = self.client.get_service("AdGroupCriterionService")
            
            operations = []
            for keyword_data in keywords:
                operation = self.client.get_type("AdGroupCriterionOperation")
                criterion = operation.create
                criterion.ad_group = f"customers/{self.config.google_ads.customer_id}/adGroups/{ad_group_id}"
                criterion.status = self.client.enums.AdGroupCriterionStatusEnum.ENABLED
                criterion.keyword.text = keyword_data['keyword']
                
                match_type_map = {
                    'EXACT': self.client.enums.KeywordMatchTypeEnum.EXACT,
                    'PHRASE': self.client.enums.KeywordMatchTypeEnum.PHRASE,
                    'BROAD': self.client.enums.KeywordMatchTypeEnum.BROAD_MODIFIED
                }
                
                criterion.keyword.match_type = match_type_map.get(
                    keyword_data.get('match_type', 'PHRASE'),
                    self.client.enums.KeywordMatchTypeEnum.PHRASE
                )
                
                criterion.cpc_bid_micros = keyword_data.get('bid_micros', 2000000)
                operations.append(operation)
            
            response = ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id=self.config.google_ads.customer_id,
                operations=operations
            )
            
            logger.info(f"Added {len(response.results)} keywords to ad group {ad_group_id}")
            
            return {
                'success': True,
                'keywords_added': len(response.results)
            }
            
        except Exception as e:
            logger.error(f"Keyword addition failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_ads_for_ad_group(self, ad_group_id: str) -> Dict[str, Any]:
        """Create ads for ad group"""
        try:
            ad_group_ad_service = self.client.get_service("AdGroupAdService")
            
            ads_data = [
                {
                    'headline1': 'Professional Air Duct Cleaning',
                    'headline2': 'San Antonio Experts',
                    'headline3': 'Call (210) 873-0584',
                    'description1': 'Licensed & insured air duct cleaning service. Same-day appointments available.',
                    'description2': 'Improve your air quality today. Free estimates. 100% satisfaction guaranteed.'
                },
                {
                    'headline1': 'Air Duct Cleaning Service',
                    'headline2': 'San Antonio TX',
                    'headline3': 'Free Estimates',
                    'description1': 'Expert HVAC cleaning services. Professional technicians with modern equipment.',
                    'description2': 'Call now for cleaner air and better health. Licensed and fully insured.'
                }
            ]
            
            operations = []
            for ad_data in ads_data:
                operation = self.client.get_type("AdGroupAdOperation")
                ad_group_ad = operation.create
                ad_group_ad.ad_group = f"customers/{self.config.google_ads.customer_id}/adGroups/{ad_group_id}"
                ad_group_ad.status = self.client.enums.AdGroupAdStatusEnum.ENABLED
                
                expanded_text_ad = ad_group_ad.ad.expanded_text_ad
                expanded_text_ad.headline_part1 = ad_data['headline1']
                expanded_text_ad.headline_part2 = ad_data['headline2']
                expanded_text_ad.headline_part3 = ad_data['headline3']
                expanded_text_ad.description = ad_data['description1']
                expanded_text_ad.description2 = ad_data['description2']
                expanded_text_ad.final_urls.append(self.config.campaign.website_url)
                
                operations.append(operation)
            
            response = ad_group_ad_service.mutate_ad_group_ads(
                customer_id=self.config.google_ads.customer_id,
                operations=operations
            )
            
            logger.info(f"Created {len(response.results)} ads for ad group {ad_group_id}")
            
            return {
                'success': True,
                'ads_created': len(response.results)
            }
            
        except Exception as e:
            logger.error(f"Ad creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
