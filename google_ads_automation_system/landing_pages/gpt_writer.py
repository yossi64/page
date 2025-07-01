"""
GPT Content Generator for Landing Pages
Uses OpenAI GPT-4 to generate professional marketing content
"""
import logging
from typing import Dict, Any
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class GPTContentGenerator:
    """Generates professional content using GPT-4"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def generate_content(self, service_type: str) -> str:
        """Generate professional content for service type"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""
            Create professional, compelling marketing content for a {service_type} business in San Antonio, Texas.
            
            Requirements:
            - Professional tone but approachable
            - Focus on benefits and value proposition
            - Include local San Antonio references
            - Emphasize trust, quality, and reliability
            - Include call-to-action elements
            - Use HTML formatting (h3, p, ul, li, strong tags)
            - Content should be 300-500 words
            - Include phone number: (210) 873-0584
            
            Structure:
            1. Opening paragraph about the service
            2. "Why Choose Us" section with 4-6 bullet points
            3. Service process or approach
            4. Call to action with phone number
            
            Make it sound professional and trustworthy for San Antonio customers.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info(f"Generated {len(content)} characters of content for {service_type}")
            
            return content
            
        except Exception as e:
            logger.error(f"GPT content generation failed: {str(e)}")
            return self._get_fallback_content(service_type)
    
    def _get_fallback_content(self, service_type: str) -> str:
        """Fallback content if GPT fails"""
        return f"""
        <h3>Professional {service_type} Services in San Antonio</h3>
        <p>When you need reliable {service_type.lower()} services in San Antonio, trust our experienced team to deliver exceptional results. We've been serving the San Antonio community for over 10 years with professional, licensed, and insured services.</p>
        
        <h3>Why Choose Our {service_type} Services:</h3>
        <ul>
            <li><strong>Licensed & Insured:</strong> Fully certified technicians with comprehensive insurance coverage</li>
            <li><strong>Same-Day Service:</strong> Emergency and scheduled appointments available</li>
            <li><strong>100% Satisfaction Guarantee:</strong> We stand behind our work with a complete satisfaction promise</li>
            <li><strong>Upfront Pricing:</strong> No hidden fees or surprise charges - transparent pricing always</li>
            <li><strong>Local Expertise:</strong> Deep understanding of San Antonio's unique needs</li>
            <li><strong>Modern Equipment:</strong> State-of-the-art tools and techniques for superior results</li>
        </ul>
        
        <h3>Our Service Process:</h3>
        <ol>
            <li><strong>Free Consultation:</strong> We assess your needs and provide an honest evaluation</li>
            <li><strong>Detailed Quote:</strong> Transparent pricing with no hidden fees or surprises</li>
            <li><strong>Professional Service:</strong> Expert technicians complete the work efficiently</li>
            <li><strong>Quality Guarantee:</strong> We ensure your complete satisfaction with our work</li>
        </ol>
        
        <p><strong>Ready to get started?</strong> Call us today at (210) 873-0584 for your free, no-obligation quote. Our friendly team is standing by to help!</p>
        """
