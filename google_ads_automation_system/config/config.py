"""
Centralized Configuration Management for Google Ads Automation System
Handles all settings, credentials, and environment variables
"""
import os
from dataclasses import dataclass
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class GoogleAdsConfig:
    """Google Ads API configuration"""
    customer_id: str
    developer_token: str
    client_id: str
    client_secret: str
    refresh_token: str
    login_customer_id: Optional[str] = None
    use_proto_plus: bool = True

@dataclass
class OpenAIConfig:
    """OpenAI API configuration"""
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 1000

@dataclass
class EmailConfig:
    """Email configuration for reporting"""
    sender_email: str
    sender_password: str
    recipient_email: str
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587

@dataclass
class CampaignConfig:
    """Campaign-specific settings"""
    campaign_name: str
    daily_budget_micros: int = 50_000_000  # $50 in micros
    target_location: str = "San Antonio, TX"
    business_type: str = "Air Duct Cleaning"
    phone_number: str = "2108730584"
    website_url: str = "https://your-domain.com"

@dataclass
class LandingPageConfig:
    """Landing page generation settings"""
    pexels_api_key: str
    output_directory: str = "landing_pages"
    phone_number: str = "2108730584"
    business_name: str = "Air Cleaning Tech LLC"
    service_area: str = "San Antonio, TX"

@dataclass
class WebhookConfig:
    """Webhook server configuration"""
    port: int = 5000
    host: str = "localhost"
    endpoint: str = "/track_call"

class SystemConfig:
    """Main system configuration with environment variable loading"""
    
    def __init__(self):
        self.google_ads = GoogleAdsConfig(
            customer_id=os.getenv("GOOGLE_ADS_CUSTOMER_ID", "8246122588"),
            developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "YOUR_DEVELOPER_TOKEN_HERE"),
            client_id=os.getenv("GOOGLE_ADS_CLIENT_ID", "YOUR_CLIENT_ID_HERE"),
            client_secret=os.getenv("GOOGLE_ADS_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE"),
            refresh_token=os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "YOUR_REFRESH_TOKEN_HERE"),
            login_customer_id=os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "8246122588"),
            use_proto_plus=True
        )
        
        self.openai = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
        )
        
        self.email = EmailConfig(
            sender_email="yossi@aircleaningtechllc.com",
            sender_password="",
            recipient_email="yossi6466@gmail.com"
        )
        
        self.campaign = CampaignConfig(
            campaign_name=f"Air Duct Cleaning San Antonio {self._get_timestamp()}",
            daily_budget_micros=50_000_000,
            target_location="San Antonio, TX",
            phone_number="2108730584"
        )
        
        self.landing_pages = LandingPageConfig(
            pexels_api_key=os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE"),
            phone_number="(210) 873-0584",
            business_name="Air Cleaning Tech LLC",
            service_area="San Antonio, TX"
        )
        
        self.webhook = WebhookConfig(
            port=int(os.getenv("WEBHOOK_PORT", "5000")),
            host=os.getenv("WEBHOOK_HOST", "localhost")
        )
    
    def _get_timestamp(self) -> str:
        """Generate timestamp for unique naming"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M")
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of missing items"""
        missing = []
        
        if not self.google_ads.customer_id:
            missing.append("GOOGLE_ADS_CUSTOMER_ID")
        if not self.openai.api_key:
            missing.append("OPENAI_API_KEY")
            
        if not self.google_ads.developer_token:
            missing.append("GOOGLE_ADS_DEVELOPER_TOKEN (needed for full API access)")
        if not self.email.sender_password:
            missing.append("SENDER_PASSWORD (needed for email reports)")
        if not self.landing_pages.pexels_api_key:
            missing.append("PEXELS_API_KEY (needed for landing page images)")
            
        return missing
    
    def is_production_ready(self) -> bool:
        """Check if configuration is ready for production use"""
        critical_missing = [item for item in self.validate() 
                          if not item.startswith("(")]
        return len(critical_missing) == 0
