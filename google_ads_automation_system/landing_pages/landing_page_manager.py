"""
Landing Page Manager for Google Ads Automation
Creates professional landing pages integrated with campaigns
"""
import os
from typing import Dict, List, Optional
from config.config import SystemConfig

class LandingPageManager:
    """Manages landing page creation and deployment"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        
        self.business_types = {
            "1": "Air Duct Cleaning",
            "2": "HVAC Repair & Maintenance", 
            "3": "Chimney Cleaning & Repair",
            "4": "Dryer Vent Cleaning",
            "5": "Carpet Cleaning",
            "6": "Pressure Washing",
            "7": "Gutter Cleaning",
            "8": "Window Cleaning",
            "9": "Pest Control",
            "10": "Plumbing Services"
        }
        
        os.makedirs(config.landing_pages.output_directory, exist_ok=True)
    
    def create_landing_page_for_service(self, service_type: str) -> Optional[str]:
        """Create landing page for specific service type (non-interactive)"""
        print(f"\n🎨 Creating professional landing page for {service_type}...")
        
        try:
            print("🔧 Generating professional content with GPT-4...")
            content = self._generate_professional_content(service_type)
            
            print("🖼️ Finding relevant images...")
            images = self._get_relevant_images(service_type)
            
            print("🏗️ Building HTML page...")
            landing_page_path = self._build_html_page(service_type, content, images)
            
            if landing_page_path:
                print(f"🎉 Landing page created successfully!")
                print(f"📄 Saved at: {landing_page_path}")
                return landing_page_path
            else:
                print("❌ Error creating landing page")
                return None
                
        except Exception as e:
            print(f"❌ Landing page creation failed: {e}")
            return None
    
    def create_landing_page_interactive(self) -> Optional[str]:
        """Interactive landing page creation workflow"""
        print("\n🎨 Starting professional landing page creation...")
        print("=" * 50)
        
        service_type = self._get_service_type_interactive()
        if not service_type:
            return None
        
        return self.create_landing_page_for_service(service_type)
    
    def _get_service_type_interactive(self) -> Optional[str]:
        """Interactive service type selection"""
        print("\n🏢 Choose business type:")
        print("-" * 30)
        
        for key, value in self.business_types.items():
            print(f"{key}. {value}")
        
        while True:
            try:
                choice = input("\nEnter number (1-10): ").strip()
                if choice in self.business_types:
                    return self.business_types[choice]
                else:
                    print("❌ Invalid choice. Please choose number between 1-10")
            except KeyboardInterrupt:
                print("\n❌ Cancelled by user")
                return None
            except Exception:
                print("❌ Input error. Try again")
    
    def _generate_professional_content(self, service_type: str) -> str:
        """Generate professional content using GPT-4"""
        try:
            from landing_pages.gpt_writer import GPTContentGenerator
            generator = GPTContentGenerator(self.config.openai.api_key)
            content = generator.generate_content(service_type)
            print("✅ Professional content generated successfully")
            return content
        except Exception as e:
            print(f"⚠️ Content generation error: {e}")
            return self._get_fallback_content(service_type)
    
    def _get_relevant_images(self, service_type: str) -> List[str]:
        """Get relevant images for the service"""
        try:
            from landing_pages.image_finder import ImageFinder
            finder = ImageFinder(self.config.openai.api_key, self.config.landing_pages.pexels_api_key)
            images = finder.get_images_for_service(service_type, count=2)
            print(f"✅ Found {len(images)} relevant images")
            return images
        except Exception as e:
            print(f"⚠️ Image search error: {e}")
            return self._get_fallback_images(service_type)
    
    def _build_html_page(self, service_type: str, content: str, images: List[str]) -> Optional[str]:
        """Build the complete HTML page"""
        try:
            from landing_pages.html_builder_complete import build_html_page
            
            hero_image = images[0] if images else "https://via.placeholder.com/1200x600"
            content_image = images[1] if len(images) > 1 else "https://via.placeholder.com/800x600"
            
            page_path = build_html_page(service_type, content, hero_image, content_image)
            
            if page_path and os.path.exists(page_path):
                print("✅ HTML page built successfully")
                return page_path
            else:
                print("❌ HTML page build error")
                return None
                
        except Exception as e:
            print(f"❌ Page building error: {e}")
            return None
    
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
    
    def _get_fallback_images(self, service_type: str) -> List[str]:
        """Fallback images if search fails"""
        service_lower = service_type.lower()
        
        if "air duct" in service_lower or "hvac" in service_lower:
            return [
                "https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80"
            ]
        elif "chimney" in service_lower:
            return [
                "https://images.unsplash.com/photo-1518780664697-55e3ad937233?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80"
            ]
        else:
            return [
                "https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80"
            ]
    
    def list_existing_landing_pages(self) -> List[str]:
        """List all existing landing pages"""
        try:
            pages_dir = self.config.landing_pages.output_directory
            if os.path.exists(pages_dir):
                html_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
                return [os.path.join(pages_dir, f) for f in html_files]
            return []
        except Exception:
            return []
