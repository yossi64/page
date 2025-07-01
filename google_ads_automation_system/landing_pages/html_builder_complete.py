"""
HTML Builder for Landing Pages
Creates complete, professional HTML pages with conversion tracking
"""
import os
from datetime import datetime
from config.config import SystemConfig

def build_html_page(service_type: str, content: str, hero_image: str, content_image: str) -> str:
    """Build complete HTML landing page"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{service_type.lower().replace(' ', '_')}_{timestamp}.html"
    filepath = os.path.join("landing_pages", filename)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{service_type} Services in San Antonio | Air Cleaning Tech LLC</title>
    <meta name="description" content="Professional {service_type.lower()} services in San Antonio. Licensed, insured, and guaranteed. Call (210) 873-0584 for free estimates.">
    
    <!-- Google Ads Conversion Tracking -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-8246122588"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'AW-8246122588');
    </script>
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .hero {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{hero_image}');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            align-items: center;
            color: white;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .hero p {{
            font-size: 1.5rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .cta-button {{
            display: inline-block;
            background: #ff6b35;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2rem;
            font-weight: bold;
            transition: background 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            background: #e55a2b;
            transform: translateY(-2px);
        }}
        
        .phone-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #ff6b35;
            margin: 1rem 0;
        }}
        
        .content-section {{
            padding: 80px 0;
            background: #f8f9fa;
        }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            align-items: center;
            margin: 40px 0;
        }}
        
        .content-text {{
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .content-image {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }}
        
        .features {{
            background: white;
            padding: 80px 0;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}
        
        .feature-card {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }}
        
        .feature-icon {{
            font-size: 3rem;
            color: #ff6b35;
            margin-bottom: 20px;
        }}
        
        .contact-section {{
            background: #2c3e50;
            color: white;
            padding: 80px 0;
            text-align: center;
        }}
        
        .contact-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}
        
        .contact-item {{
            padding: 20px;
        }}
        
        .contact-item h3 {{
            color: #ff6b35;
            margin-bottom: 10px;
        }}
        
        .form-section {{
            background: white;
            padding: 80px 0;
        }}
        
        .contact-form {{
            max-width: 600px;
            margin: 0 auto;
            background: #f8f9fa;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }}
        
        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }}
        
        .form-group textarea {{
            height: 120px;
            resize: vertical;
        }}
        
        .submit-btn {{
            background: #ff6b35;
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 5px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
            width: 100%;
        }}
        
        .submit-btn:hover {{
            background: #e55a2b;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}
            
            .hero p {{
                font-size: 1.2rem;
            }}
            
            .content-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .phone-number {{
                font-size: 1.5rem;
            }}
            
            .contact-form {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="container">
            <h1>Professional {service_type}</h1>
            <p>San Antonio's Most Trusted Service Professionals</p>
            <div class="phone-number">(210) 873-0584</div>
            <a href="#contact" class="cta-button">Get Free Estimate</a>
        </div>
    </section>
    
    <section class="content-section">
        <div class="container">
            <div class="content-grid">
                <div class="content-text">
                    {content}
                </div>
                <div>
                    <img src="{content_image}" alt="{service_type} Service" class="content-image">
                </div>
            </div>
        </div>
    </section>
    
    <section class="features">
        <div class="container">
            <h2 style="text-align: center; margin-bottom: 20px;">Why Choose Air Cleaning Tech LLC?</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🏆</div>
                    <h3>Licensed & Insured</h3>
                    <p>Fully certified professionals with comprehensive insurance coverage for your peace of mind.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Same-Day Service</h3>
                    <p>Emergency and scheduled appointments available to meet your urgent needs.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">✅</div>
                    <h3>100% Guarantee</h3>
                    <p>We stand behind our work with a complete satisfaction guarantee on all services.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💰</div>
                    <h3>Upfront Pricing</h3>
                    <p>No hidden fees or surprise charges - transparent pricing you can trust.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🏠</div>
                    <h3>Local Experts</h3>
                    <p>Deep understanding of San Antonio's unique climate and service needs.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔧</div>
                    <h3>Modern Equipment</h3>
                    <p>State-of-the-art tools and techniques for superior, lasting results.</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="form-section" id="contact">
        <div class="container">
            <h2 style="text-align: center; margin-bottom: 40px;">Get Your Free Estimate Today</h2>
            <form class="contact-form" action="thankyou.html" method="POST">
                <div class="form-group">
                    <label for="name">Full Name *</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone Number *</label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email">
                </div>
                <div class="form-group">
                    <label for="address">Service Address</label>
                    <input type="text" id="address" name="address" placeholder="San Antonio, TX">
                </div>
                <div class="form-group">
                    <label for="service">Service Needed</label>
                    <input type="text" id="service" name="service" value="{service_type}" readonly>
                </div>
                <div class="form-group">
                    <label for="message">Additional Details</label>
                    <textarea id="message" name="message" placeholder="Tell us about your specific needs..."></textarea>
                </div>
                <button type="submit" class="submit-btn">Get Free Estimate</button>
            </form>
        </div>
    </section>
    
    <section class="contact-section">
        <div class="container">
            <h2>Ready to Get Started?</h2>
            <p style="font-size: 1.2rem; margin: 20px 0;">Call us now for immediate assistance</p>
            <div class="phone-number" style="color: white;">(210) 873-0584</div>
            
            <div class="contact-info">
                <div class="contact-item">
                    <h3>📞 Phone</h3>
                    <p>(210) 873-0584</p>
                </div>
                <div class="contact-item">
                    <h3>📧 Email</h3>
                    <p>info@aircleaningtechllc.com</p>
                </div>
                <div class="contact-item">
                    <h3>📍 Service Area</h3>
                    <p>San Antonio, TX & Surrounding Areas</p>
                </div>
                <div class="contact-item">
                    <h3>🕒 Hours</h3>
                    <p>24/7 Emergency Service Available</p>
                </div>
            </div>
        </div>
    </section>
    
    <script>
        document.querySelector('.contact-form').addEventListener('submit', function(e) {{
            const name = document.getElementById('name').value;
            const phone = document.getElementById('phone').value;
            
            if (!name || !phone) {{
                e.preventDefault();
                alert('Please fill in all required fields (Name and Phone).');
                return;
            }}
            
            gtag('event', 'conversion', {{
                'send_to': 'AW-8246122588/form_submit',
                'value': 1.0,
                'currency': 'USD'
            }});
        }});
        
        document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {{
            link.addEventListener('click', function() {{
                gtag('event', 'conversion', {{
                    'send_to': 'AW-8246122588/phone_call',
                    'value': 1.0,
                    'currency': 'USD'
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath
