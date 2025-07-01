"""
Improved Google Ads Campaign Optimizer Module
Handles automated bid optimization and performance improvements
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class CampaignOptimizer:
    """Handles Google Ads campaign optimization"""
    
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
    
    def optimize_campaigns(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive campaign optimization"""
        logger.info("Starting campaign optimization")
        
        try:
            optimization_results = {
                'timestamp': datetime.now().isoformat(),
                'keyword_optimizations': [],
                'bid_adjustments': [],
                'ad_optimizations': [],
                'budget_recommendations': [],
                'performance_summary': {}
            }
            
            campaign_id = campaign_data.get('campaign', {}).get('campaign_id')
            if campaign_id:
                performance_data = self._get_campaign_performance(campaign_id)
                optimization_results['performance_summary'] = performance_data
                
                keyword_results = self._optimize_keywords(campaign_id, performance_data)
                optimization_results['keyword_optimizations'] = keyword_results
                
                bid_results = self._optimize_bids(campaign_id, performance_data)
                optimization_results['bid_adjustments'] = bid_results
                
                ad_results = self._optimize_ads(campaign_id, performance_data)
                optimization_results['ad_optimizations'] = ad_results
                
                budget_results = self._analyze_budget_performance(campaign_id, performance_data)
                optimization_results['budget_recommendations'] = budget_results
            
            logger.info("Campaign optimization completed")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Campaign optimization failed: {str(e)}")
            raise
    
    def _get_campaign_performance(self, campaign_id: str, days: int = 7) -> Dict[str, Any]:
        """Get campaign performance data for the last N days"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            query = f"""
                SELECT 
                    campaign.id,
                    campaign.name,
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
                AND segments.date BETWEEN '{start_date}' AND '{end_date}'
            """
            
            response = ga_service.search(
                customer_id=self.config.google_ads.customer_id,
                query=query
            )
            
            total_impressions = 0
            total_clicks = 0
            total_cost = 0
            total_conversions = 0
            total_conversion_value = 0
            
            for row in response:
                total_impressions += row.metrics.impressions
                total_clicks += row.metrics.clicks
                total_cost += row.metrics.cost_micros
                total_conversions += row.metrics.conversions
                total_conversion_value += row.metrics.conversions_value
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            avg_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
            cost_per_conversion = (total_cost / total_conversions) if total_conversions > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            
            return {
                'campaign_id': campaign_id,
                'date_range': f"{start_date} to {end_date}",
                'impressions': total_impressions,
                'clicks': total_clicks,
                'cost_micros': total_cost,
                'cost_dollars': total_cost / 1_000_000,
                'conversions': total_conversions,
                'conversion_value': total_conversion_value,
                'ctr': round(ctr, 2),
                'avg_cpc_micros': avg_cpc,
                'avg_cpc_dollars': round(avg_cpc / 1_000_000, 2),
                'cost_per_conversion_micros': cost_per_conversion,
                'cost_per_conversion_dollars': round(cost_per_conversion / 1_000_000, 2),
                'conversion_rate': round(conversion_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Failed to get campaign performance: {str(e)}")
            return {}
    
    def _optimize_keywords(self, campaign_id: str, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize keyword bids and status based on performance"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = f"""
                SELECT 
                    ad_group_criterion.criterion_id,
                    ad_group_criterion.keyword.text,
                    ad_group_criterion.keyword.match_type,
                    ad_group_criterion.cpc_bid_micros,
                    ad_group_criterion.status,
                    ad_group.id,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.conversions,
                    metrics.ctr,
                    metrics.average_cpc
                FROM keyword_view 
                WHERE campaign.id = {campaign_id}
                AND segments.date DURING LAST_7_DAYS
                AND ad_group_criterion.type = 'KEYWORD'
            """
            
            response = ga_service.search(
                customer_id=self.config.google_ads.customer_id,
                query=query
            )
            
            optimizations = []
            ad_group_criterion_service = self.client.get_service("AdGroupCriterionService")
            
            for row in response:
                keyword_data = {
                    'criterion_id': row.ad_group_criterion.criterion_id,
                    'keyword_text': row.ad_group_criterion.keyword.text,
                    'match_type': row.ad_group_criterion.keyword.match_type.name,
                    'current_bid_micros': row.ad_group_criterion.cpc_bid_micros,
                    'ad_group_id': row.ad_group.id,
                    'impressions': row.metrics.impressions,
                    'clicks': row.metrics.clicks,
                    'cost_micros': row.metrics.cost_micros,
                    'conversions': row.metrics.conversions,
                    'ctr': row.metrics.ctr,
                    'avg_cpc': row.metrics.average_cpc
                }
                
                optimization = self._determine_keyword_optimization(keyword_data)
                
                if optimization['action'] != 'no_change':
                    try:
                        self._apply_keyword_optimization(
                            ad_group_criterion_service,
                            keyword_data,
                            optimization
                        )
                        optimizations.append({
                            'keyword': keyword_data['keyword_text'],
                            'action': optimization['action'],
                            'old_bid': keyword_data['current_bid_micros'],
                            'new_bid': optimization.get('new_bid_micros'),
                            'reason': optimization['reason']
                        })
                    except Exception as e:
                        logger.error(f"Failed to optimize keyword {keyword_data['keyword_text']}: {str(e)}")
            
            return optimizations
            
        except Exception as e:
            logger.error(f"Keyword optimization failed: {str(e)}")
            return []
    
    def _determine_keyword_optimization(self, keyword_data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine what optimization to apply to a keyword"""
        impressions = keyword_data['impressions']
        clicks = keyword_data['clicks']
        conversions = keyword_data['conversions']
        ctr = keyword_data['ctr']
        current_bid = keyword_data['current_bid_micros']
        
        if conversions > 0 and ctr > 3.0:
            new_bid = min(current_bid * 1.2, 5_000_000)
            return {
                'action': 'increase_bid',
                'new_bid_micros': int(new_bid),
                'reason': 'High conversion rate and CTR'
            }
        
        elif clicks > 10 and conversions == 0 and ctr < 1.0:
            new_bid = max(current_bid * 0.8, 500_000)
            return {
                'action': 'decrease_bid',
                'new_bid_micros': int(new_bid),
                'reason': 'Low CTR and no conversions'
            }
        
        elif impressions < 10:
            new_bid = min(current_bid * 1.1, 3_000_000)
            return {
                'action': 'increase_bid',
                'new_bid_micros': int(new_bid),
                'reason': 'Low impression volume'
            }
        
        else:
            return {
                'action': 'no_change',
                'reason': 'Performance within acceptable range'
            }
    
    def _apply_keyword_optimization(self, service, keyword_data: Dict[str, Any], optimization: Dict[str, Any]):
        """Apply keyword optimization"""
        if optimization['action'] in ['increase_bid', 'decrease_bid']:
            operation = self.client.get_type("AdGroupCriterionOperation")
            operation.update.resource_name = (
                f"customers/{self.config.google_ads.customer_id}/"
                f"adGroupCriteria/{keyword_data['ad_group_id']}~{keyword_data['criterion_id']}"
            )
            operation.update.cpc_bid_micros = optimization['new_bid_micros']
            operation.update_mask.paths.append("cpc_bid_micros")
            
            service.mutate_ad_group_criteria(
                customer_id=self.config.google_ads.customer_id,
                operations=[operation]
            )
    
    def _optimize_bids(self, campaign_id: str, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize ad group bids based on performance"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = f"""
                SELECT 
                    ad_group.id,
                    ad_group.name,
                    ad_group.cpc_bid_micros,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.conversions,
                    metrics.cost_micros,
                    metrics.ctr
                FROM ad_group 
                WHERE campaign.id = {campaign_id}
                AND segments.date DURING LAST_7_DAYS
            """
            
            response = ga_service.search(
                customer_id=self.config.google_ads.customer_id,
                query=query
            )
            
            bid_adjustments = []
            ad_group_service = self.client.get_service("AdGroupService")
            
            for row in response:
                ad_group_data = {
                    'id': row.ad_group.id,
                    'name': row.ad_group.name,
                    'current_bid': row.ad_group.cpc_bid_micros,
                    'impressions': row.metrics.impressions,
                    'clicks': row.metrics.clicks,
                    'conversions': row.metrics.conversions,
                    'cost': row.metrics.cost_micros,
                    'ctr': row.metrics.ctr
                }
                
                adjustment = self._determine_bid_adjustment(ad_group_data)
                
                if adjustment['action'] != 'no_change':
                    try:
                        operation = self.client.get_type("AdGroupOperation")
                        operation.update.resource_name = (
                            f"customers/{self.config.google_ads.customer_id}/adGroups/{ad_group_data['id']}"
                        )
                        operation.update.cpc_bid_micros = adjustment['new_bid_micros']
                        operation.update_mask.paths.append("cpc_bid_micros")
                        
                        ad_group_service.mutate_ad_groups(
                            customer_id=self.config.google_ads.customer_id,
                            operations=[operation]
                        )
                        
                        bid_adjustments.append({
                            'ad_group_name': ad_group_data['name'],
                            'action': adjustment['action'],
                            'old_bid': ad_group_data['current_bid'],
                            'new_bid': adjustment['new_bid_micros'],
                            'reason': adjustment['reason']
                        })
                        
                    except Exception as e:
                        logger.error(f"Failed to adjust bid for ad group {ad_group_data['name']}: {str(e)}")
            
            return bid_adjustments
            
        except Exception as e:
            logger.error(f"Bid optimization failed: {str(e)}")
            return []
    
    def _determine_bid_adjustment(self, ad_group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine bid adjustment for an ad group"""
        conversions = ad_group_data['conversions']
        ctr = ad_group_data['ctr']
        current_bid = ad_group_data['current_bid']
        clicks = ad_group_data['clicks']
        
        if conversions > 0 and ctr > 2.5:
            new_bid = min(current_bid * 1.15, 4_000_000)
            return {
                'action': 'increase_bid',
                'new_bid_micros': int(new_bid),
                'reason': 'High conversion rate and CTR'
            }
        
        elif clicks > 20 and conversions == 0 and ctr < 1.5:
            new_bid = max(current_bid * 0.85, 750_000)
            return {
                'action': 'decrease_bid',
                'new_bid_micros': int(new_bid),
                'reason': 'Low performance metrics'
            }
        
        else:
            return {
                'action': 'no_change',
                'reason': 'Performance within target range'
            }
    
    def _optimize_ads(self, campaign_id: str, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize ad performance and status"""
        return [{
            'action': 'monitor',
            'reason': 'Ad optimization requires manual review of creative performance'
        }]
    
    def _analyze_budget_performance(self, campaign_id: str, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze budget performance and make recommendations"""
        try:
            recommendations = []
            
            daily_budget = self.config.campaign.daily_budget_micros
            avg_daily_spend = performance_data.get('cost_micros', 0) / 7
            
            budget_utilization = (avg_daily_spend / daily_budget) * 100 if daily_budget > 0 else 0
            
            if budget_utilization > 90:
                recommendations.append({
                    'type': 'budget_increase',
                    'current_budget': daily_budget / 1_000_000,
                    'recommended_budget': (daily_budget * 1.2) / 1_000_000,
                    'reason': f'High budget utilization ({budget_utilization:.1f}%)'
                })
            elif budget_utilization < 50:
                recommendations.append({
                    'type': 'budget_optimization',
                    'current_budget': daily_budget / 1_000_000,
                    'utilization': f"{budget_utilization:.1f}%",
                    'reason': 'Low budget utilization - consider bid increases or keyword expansion'
                })
            
            cost_per_conversion = performance_data.get('cost_per_conversion_dollars', 0)
            if cost_per_conversion > 100:
                recommendations.append({
                    'type': 'cost_efficiency',
                    'cost_per_conversion': cost_per_conversion,
                    'reason': 'High cost per conversion - review keyword targeting and bids'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Budget analysis failed: {str(e)}")
            return []
