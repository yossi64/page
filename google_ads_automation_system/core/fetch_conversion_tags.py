"""
Conversion Tag Fetcher for Google Ads Automation
Retrieves and manages conversion tracking tags
"""
import logging
from typing import Dict, Any, List
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class ConversionTagFetcher:
    """Fetches and manages Google Ads conversion tracking tags"""
    
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
    
    def get_conversion_actions(self) -> List[Dict[str, Any]]:
        """Retrieve all conversion actions for the account"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = """
                SELECT 
                    conversion_action.id,
                    conversion_action.name,
                    conversion_action.type,
                    conversion_action.status,
                    conversion_action.category,
                    conversion_action.tag_snippets
                FROM conversion_action
                WHERE conversion_action.status = 'ENABLED'
            """
            
            response = ga_service.search(
                customer_id=self.config.google_ads.customer_id,
                query=query
            )
            
            conversion_actions = []
            for row in response:
                action_data = {
                    'id': row.conversion_action.id,
                    'name': row.conversion_action.name,
                    'type': row.conversion_action.type.name,
                    'status': row.conversion_action.status.name,
                    'category': row.conversion_action.category.name,
                    'tag_snippets': []
                }
                
                for snippet in row.conversion_action.tag_snippets:
                    tag_data = {
                        'type': snippet.type.name,
                        'page_format': snippet.page_format.name,
                        'global_site_tag': snippet.global_site_tag,
                        'event_snippet': snippet.event_snippet
                    }
                    action_data['tag_snippets'].append(tag_data)
                
                conversion_actions.append(action_data)
            
            logger.info(f"Retrieved {len(conversion_actions)} conversion actions")
            return conversion_actions
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            return []
        except Exception as e:
            logger.error(f"Failed to get conversion actions: {str(e)}")
            return []
    
    def get_conversion_tag_for_action(self, conversion_action_id: str) -> Dict[str, Any]:
        """Get the conversion tag for a specific conversion action"""
        try:
            conversion_actions = self.get_conversion_actions()
            
            for action in conversion_actions:
                if str(action['id']) == str(conversion_action_id):
                    if action['tag_snippets']:
                        snippet = action['tag_snippets'][0]
                        return {
                            'success': True,
                            'conversion_action_id': conversion_action_id,
                            'conversion_action_name': action['name'],
                            'global_site_tag': snippet.get('global_site_tag', ''),
                            'event_snippet': snippet.get('event_snippet', ''),
                            'page_format': snippet.get('page_format', 'HTML')
                        }
            
            return {
                'success': False,
                'error': f'Conversion action {conversion_action_id} not found'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_conversion_tag_html(self, conversion_action_id: str = None) -> str:
        """Generate HTML conversion tracking code"""
        try:
            customer_id = self.config.google_ads.customer_id
            
            if conversion_action_id:
                tag_data = self.get_conversion_tag_for_action(conversion_action_id)
                if tag_data.get('success'):
                    return tag_data.get('global_site_tag', '') + '\n' + tag_data.get('event_snippet', '')
            
            default_tag = f"""
<!-- Google Ads Conversion Tracking -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-{customer_id}"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'AW-{customer_id}');
    
    // Conversion event
    gtag('event', 'conversion', {{
        'send_to': 'AW-{customer_id}/form_submit',
        'value': 1.0,
        'currency': 'USD'
    }});
</script>
"""
            return default_tag.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate conversion tag: {str(e)}")
            return ""
    
    def get_phone_call_conversion_tag(self) -> str:
        """Generate phone call conversion tracking code"""
        try:
            customer_id = self.config.google_ads.customer_id
            phone_number = self.config.landing_pages.phone_number
            
            phone_tag = f"""
<!-- Google Ads Phone Call Conversion Tracking -->
<script>
    document.addEventListener('DOMContentLoaded', function() {{
        // Track phone number clicks
        document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {{
            link.addEventListener('click', function() {{
                gtag('event', 'conversion', {{
                    'send_to': 'AW-{customer_id}/phone_call',
                    'value': 1.0,
                    'currency': 'USD'
                }});
            }});
        }});
        
        // Track phone number text clicks
        document.querySelectorAll('.phone-number').forEach(function(element) {{
            element.addEventListener('click', function() {{
                gtag('event', 'conversion', {{
                    'send_to': 'AW-{customer_id}/phone_call',
                    'value': 1.0,
                    'currency': 'USD'
                }});
                
                // Optionally open phone dialer
                window.location.href = 'tel:{phone_number}';
            }});
        }});
    }});
</script>
"""
            return phone_tag.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate phone call conversion tag: {str(e)}")
            return ""
