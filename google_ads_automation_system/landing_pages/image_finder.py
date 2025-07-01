"""
Image Finder for Landing Pages
Searches for relevant images using Pexels API
"""
import logging
import requests
from typing import List, Dict, Any
from config.config import SystemConfig

logger = logging.getLogger(__name__)

class ImageFinder:
    """Finds relevant images for landing pages"""
    
    def __init__(self, openai_api_key: str, pexels_api_key: str):
        self.openai_api_key = openai_api_key
        self.pexels_api_key = pexels_api_key
        self.pexels_base_url = "https://api.pexels.com/v1"
    
    def get_images_for_service(self, service_type: str, count: int = 2) -> List[str]:
        """Get relevant images for service type"""
        try:
            search_terms = self._generate_search_terms(service_type)
            
            images = []
            for term in search_terms[:3]:  # Try up to 3 search terms
                found_images = self._search_pexels(term, count - len(images))
                images.extend(found_images)
                
                if len(images) >= count:
                    break
            
            if len(images) < count:
                fallback_images = self._get_fallback_images(service_type)
                images.extend(fallback_images[:count - len(images)])
            
            logger.info(f"Found {len(images)} images for {service_type}")
            return images[:count]
            
        except Exception as e:
            logger.error(f"Image search failed: {str(e)}")
            return self._get_fallback_images(service_type)[:count]
    
    def _generate_search_terms(self, service_type: str) -> List[str]:
        """Generate search terms using GPT-4"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""
            Generate 5 specific search terms for finding professional stock photos for a {service_type} business.
            
            Requirements:
            - Terms should find professional, high-quality images
            - Focus on the actual work/equipment/results
            - Avoid generic business photos
            - Each term should be 2-4 words maximum
            
            Return only the search terms, one per line, no numbering or formatting.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.5
            )
            
            terms = [term.strip() for term in response.choices[0].message.content.split('\n') if term.strip()]
            return terms[:5]
            
        except Exception as e:
            logger.error(f"Search term generation failed: {str(e)}")
            return self._get_fallback_search_terms(service_type)
    
    def _search_pexels(self, query: str, count: int) -> List[str]:
        """Search Pexels for images"""
        try:
            headers = {
                'Authorization': self.pexels_api_key
            }
            
            params = {
                'query': query,
                'per_page': count,
                'orientation': 'landscape'
            }
            
            response = requests.get(
                f"{self.pexels_base_url}/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for photo in data.get('photos', []):
                    image_url = photo['src']['large']
                    images.append(image_url)
                
                return images
            else:
                logger.warning(f"Pexels API returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Pexels search failed: {str(e)}")
            return []
    
    def _get_fallback_search_terms(self, service_type: str) -> List[str]:
        """Fallback search terms if GPT fails"""
        service_lower = service_type.lower()
        
        if "air duct" in service_lower:
            return ["air duct cleaning", "hvac maintenance", "duct work", "air conditioning", "ventilation system"]
        elif "hvac" in service_lower:
            return ["hvac repair", "air conditioning", "heating system", "hvac technician", "ac unit"]
        elif "chimney" in service_lower:
            return ["chimney cleaning", "fireplace maintenance", "chimney sweep", "brick chimney", "fireplace"]
        elif "carpet" in service_lower:
            return ["carpet cleaning", "steam cleaning", "rug cleaning", "carpet care", "floor cleaning"]
        elif "pressure washing" in service_lower:
            return ["pressure washing", "power washing", "house cleaning", "driveway cleaning", "exterior cleaning"]
        else:
            return [service_type.lower(), "professional service", "home maintenance", "cleaning service", "repair work"]
    
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
        elif "carpet" in service_lower:
            return [
                "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80"
            ]
        else:
            return [
                "https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80"
            ]
