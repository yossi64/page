"""
Email Reporter Module for Google Ads Automation
Generates and sends performance reports via email
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, Any, List
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class EmailReporter:
    """Handles email reporting for campaign performance"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
    
    def generate_and_send_report(self) -> Dict[str, Any]:
        """Generate performance report and send via email"""
        try:
            from core.campaign_discovery import CampaignDiscovery
            
            discovery = CampaignDiscovery(self.config)
            campaigns = discovery.discover_campaigns()
            
            report_html = self._generate_html_report(campaigns)
            
            result = self._send_email_report(report_html)
            
            return {
                'success': True,
                'campaigns_reported': len(campaigns),
                'email_sent': result.get('success', False),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_html_report(self, campaigns: List[Dict[str, Any]]) -> str:
        """Generate HTML report from campaign data"""
        total_cost = sum(c['metrics']['cost_dollars'] for c in campaigns)
        total_clicks = sum(c['metrics']['clicks'] for c in campaigns)
        total_conversions = sum(c['metrics']['conversions'] for c in campaigns)
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #4285f4; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .campaign {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .metrics {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .metric {{ text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #4285f4; }}
                .metric-label {{ font-size: 12px; color: #666; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Google Ads Performance Report</h1>
                <p>Air Cleaning Tech LLC - San Antonio</p>
                <p>{datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="summary">
                <h2>30-Day Summary</h2>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">${total_cost:.2f}</div>
                        <div class="metric-label">Total Spend</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{total_clicks:,}</div>
                        <div class="metric-label">Total Clicks</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{total_conversions:.1f}</div>
                        <div class="metric-label">Total Conversions</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{len(campaigns)}</div>
                        <div class="metric-label">Active Campaigns</div>
                    </div>
                </div>
            </div>
            
            <h2>Campaign Performance</h2>
            <table>
                <tr>
                    <th>Campaign Name</th>
                    <th>Status</th>
                    <th>Impressions</th>
                    <th>Clicks</th>
                    <th>CTR</th>
                    <th>Cost</th>
                    <th>Conversions</th>
                    <th>Avg CPC</th>
                </tr>
        """
        
        for campaign in campaigns:
            metrics = campaign['metrics']
            campaign_info = campaign['campaign']
            
            html += f"""
                <tr>
                    <td>{campaign_info['name']}</td>
                    <td>{campaign_info['status']}</td>
                    <td>{metrics['impressions']:,}</td>
                    <td>{metrics['clicks']:,}</td>
                    <td>{metrics['ctr']:.2f}%</td>
                    <td>${metrics['cost_dollars']:.2f}</td>
                    <td>{metrics['conversions']:.1f}</td>
                    <td>${metrics['average_cpc'] / 1_000_000:.2f}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <div style="margin-top: 30px; padding: 20px; background-color: #e8f5e8; border-radius: 5px;">
                <h3>📞 Contact Information</h3>
                <p><strong>Phone:</strong> (210) 873-0584</p>
                <p><strong>Email:</strong> yossi@aircleaningtechllc.com</p>
                <p><strong>Service Area:</strong> San Antonio, TX</p>
            </div>
            
            <div style="margin-top: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>This report was generated automatically by the Google Ads Automation System</p>
                <p>Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _send_email_report(self, html_content: str) -> Dict[str, Any]:
        """Send HTML report via email"""
        try:
            if not self.config.email.sender_password:
                logger.warning("Email password not configured, skipping email send")
                return {'success': False, 'reason': 'No email password configured'}
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Google Ads Performance Report - {datetime.now().strftime('%B %d, %Y')}"
            msg['From'] = self.config.email.sender_email
            msg['To'] = self.config.email.recipient_email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.config.email.smtp_server, self.config.email.smtp_port)
            server.starttls()
            server.login(self.config.email.sender_email, self.config.email.sender_password)
            
            text = msg.as_string()
            server.sendmail(self.config.email.sender_email, self.config.email.recipient_email, text)
            server.quit()
            
            logger.info(f"Report sent successfully to {self.config.email.recipient_email}")
            
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Failed to send email report: {str(e)}")
            return {'success': False, 'error': str(e)}
