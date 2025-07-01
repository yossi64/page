"""
Keyword Research Module for Google Ads Automation
Handles keyword discovery and analysis using GPT-4
"""
import logging
from typing import List, Dict, Any
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class KeywordResearcher:
    """Handles keyword research and analysis"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
    
    def research_keywords(self, base_keyword: str, count: int = 20) -> List[Dict[str, Any]]:
        """Research keywords using GPT-4"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.config.openai.api_key)
            
            prompt = f"""
            Generate {count} high-converting Google Ads keywords for "{base_keyword}" business in San Antonio, Texas.
            
            Focus on:
            - Local intent keywords
            - Commercial intent keywords  
            - Service-specific keywords
            - Emergency/urgent keywords
            
            Return as a JSON list with this format:
            [
                {{"keyword": "keyword text", "match_type": "EXACT|PHRASE|BROAD", "bid_micros": 2000000}},
                ...
            ]
            
            Bid amounts should be in micros (multiply dollars by 1,000,000).
            Use realistic bids between $1-5 for this service type.
            """
            
            response = client.chat.completions.create(
                model=self.config.openai.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.openai.max_tokens
            )
            
            import json
            keywords_data = json.loads(response.choices[0].message.content)
            
            logger.info(f"Generated {len(keywords_data)} keywords for '{base_keyword}'")
            return keywords_data
            
        except Exception as e:
            logger.error(f"Keyword research failed: {str(e)}")
            return self._get_fallback_keywords(base_keyword)
    
    def _get_fallback_keywords(self, base_keyword: str) -> List[Dict[str, Any]]:
        """Fallback keywords if GPT fails"""
        fallback_keywords = [
            {"keyword": "air duct cleaning san antonio", "match_type": "EXACT", "bid_micros": 3000000},
            {"keyword": "hvac cleaning san antonio", "match_type": "PHRASE", "bid_micros": 2500000},
            {"keyword": "duct cleaning near me", "match_type": "PHRASE", "bid_micros": 2800000},
            {"keyword": "air duct cleaning service", "match_type": "PHRASE", "bid_micros": 2200000},
            {"keyword": "professional duct cleaning", "match_type": "PHRASE", "bid_micros": 2400000},
            {"keyword": "san antonio air duct cleaning", "match_type": "EXACT", "bid_micros": 3200000},
            {"keyword": "emergency duct cleaning", "match_type": "PHRASE", "bid_micros": 3500000},
            {"keyword": "residential duct cleaning", "match_type": "PHRASE", "bid_micros": 2300000},
            {"keyword": "commercial duct cleaning", "match_type": "PHRASE", "bid_micros": 2600000},
            {"keyword": "duct cleaning company", "match_type": "PHRASE", "bid_micros": 2100000}
        ]
        
        logger.info(f"Using {len(fallback_keywords)} fallback keywords")
        return fallback_keywords
    
    def analyze_keyword_performance(self, keywords: List[str]) -> Dict[str, Any]:
        """Analyze keyword performance using Google Ads API"""
        try:
            from google.ads.googleads.client import GoogleAdsClient
            
            credentials = {
                "developer_token": self.config.google_ads.developer_token,
                "client_id": self.config.google_ads.client_id,
                "client_secret": self.config.google_ads.client_secret,
                "refresh_token": self.config.google_ads.refresh_token,
                "use_proto_plus": self.config.google_ads.use_proto_plus,
            }
            
            if self.config.google_ads.login_customer_id:
                credentials["login_customer_id"] = self.config.google_ads.login_customer_id
            
            client = GoogleAdsClient.load_from_dict(credentials)
            
            keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
            
            request = client.get_type("GenerateKeywordIdeasRequest")
            request.customer_id = self.config.google_ads.customer_id
            request.language = "1000"  # English
            request.geo_target_constants.append("geoTargetConstants/1026201")  # San Antonio
            
            request.keyword_seed.keywords.extend(keywords)
            
            response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
            
            keyword_ideas = []
            for idea in response.results:
                keyword_ideas.append({
                    'keyword': idea.text,
                    'avg_monthly_searches': idea.keyword_idea_metrics.avg_monthly_searches,
                    'competition': idea.keyword_idea_metrics.competition.name,
                    'low_top_of_page_bid_micros': idea.keyword_idea_metrics.low_top_of_page_bid_micros,
                    'high_top_of_page_bid_micros': idea.keyword_idea_metrics.high_top_of_page_bid_micros
                })
            
            return {
                'success': True,
                'keyword_ideas': keyword_ideas,
                'total_ideas': len(keyword_ideas)
            }
            
        except Exception as e:
            logger.error(f"Keyword analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
