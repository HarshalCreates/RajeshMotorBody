# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import urllib.parse
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # needed for flash messages
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Email configuration
ADMIN_EMAIL = 'rajeshmoterbody@gmail.com'  # Replace with your email
ADMIN_PHONE = '+919824020762'  # Replace with your WhatsApp number (with country code)

# For simpler email sending without SMTP setup, we'll use Formspree
FORMSPREE_ID = 'mdkgnnae'  # Replace with your Formspree form ID after signing up at formspree.io

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if required static image files exist
required_images = [
    'static/images/Pickupp.png',
    'static/images/Eicherr.png',
    'static/images/TataAce.png',
    'static/images/Dumper.png'
]

for img_path in required_images:
    if not os.path.exists(img_path):
        print(f"WARNING: Required image file {img_path} not found!")

# Function to send email
def send_order_email(order_info):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"New Truck Order: {order_info['model']}"
        
        # Create email body with order details
        body = f"""
        <html>
        <body>
            <h2>New Truck Order Received</h2>
            <p><strong>Order Date:</strong> {order_info['order_date']}</p>
            <p><strong>Truck Type:</strong> {order_info['model']}</p>
            <p><strong>Specifications:</strong> {order_info['specs']}</p>
            <p><strong>Delivery Location:</strong> {order_info['location']}</p>
            <p><strong>Expected Timeline:</strong> {order_info['timeline']}</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to server and send email
        print(f"Attempting to send email to {ADMIN_EMAIL}...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        
        try:
            server.login(ADMIN_EMAIL, 'Sanvi@123')
            text = msg.as_string()
            server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, text)
            print("Email sent successfully!")
            return True
        except Exception as login_error:
            print(f"SMTP Authentication Error: {login_error}")
            
            # If you want a more reliable alternative without SMTP setup:
            # Consider using a service like Resend.com (they have a free tier)
            # 1. Sign up at https://resend.com
            # 2. Get your API key
            # 3. Install the resend library: pip install resend
            # 4. Uncomment and modify the code below:
            
            """
            import resend
            resend.api_key = "re_123YourResendAPIKey"
            
            try:
                r = resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": ADMIN_EMAIL,
                    "subject": f"New Truck Order: {order_info['model']}",
                    "html": body
                })
                print("Email sent using Resend!")
                return True
            except Exception as resend_error:
                print(f"Resend API Error: {resend_error}")
                return False
            """
            
            return False
        finally:
            server.quit()
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Function to generate WhatsApp link with order details
def get_whatsapp_link(order_info):
    # Create message text
    message = f"""New Truck Order:
Order Date: {order_info['order_date']}
Truck Type: {order_info['model']}
Specifications: {order_info['specs']}
Location: {order_info['location']}
Timeline: {order_info['timeline']}"""
    
    # URL encode the message
    encoded_message = urllib.parse.quote(message)
    
    # Create WhatsApp API link
    whatsapp_link = f"https://api.whatsapp.com/send?phone={ADMIN_PHONE}&text={encoded_message}"
    
    return whatsapp_link

# Store truck data
truck_data = []

# Sample truck models data
truck_models = {
    "eicher-curtain": {
        "name": "Eicher Sliding Curtain",
        "brand": "Eicher",
        "category": "Specialized",
        "rating": 4.7,
        "reviews": 15,
        "warranty": "2 Years",
        "material": "Aluminum frame with reinforced PVC curtain sides",
        "dimensions": "22ft x 7.5ft x 8ft (LxWxH)",
        "capacity": "Up to 12 tons",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Eicher Pro 3015, 3019, 4019, 5025 series",
        "main_image": "/static/images/SlidingCurtain.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/1/XR/ZU/PN/108537223/eicher-pro-3015-truck-1000x1000.png",
                "caption": "Eicher Sliding Curtain Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/10/OO/ME/DD/36130494/eicher-pro-3015-truck-1000x1000.jpg",
                "caption": "Eicher Sliding Curtain Side View"
            },
            {
                "url": "https://5.imimg.com/data5/ANDROID/Default/2021/11/KK/MM/GJ/46481591/product-jpeg-1000x1000.jpg",
                "caption": "Eicher Sliding Curtain with Open Side"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/7/332186088/QR/XL/JQ/182158761/eicher-3015-truck-1000x1000.jpg",
                "caption": "Eicher Pro Full Vehicle"
            }
        ],
        "features": [
            {
                "icon": "fas fa-door-open",
                "title": "Easy Side Access",
                "description": "Sliding curtain sides allow for full-length access to the cargo area from both sides"
            },
            {
                "icon": "fas fa-shield-alt",
                "title": "Weather Protection",
                "description": "High-quality PVC curtains provide protection from weather while maintaining easy access"
            },
            {
                "icon": "fas fa-dolly",
                "title": "Efficient Loading",
                "description": "Side access enables forklift loading from any angle, drastically reducing loading times"
            }
        ],
        "custom_options": [
            {
                "title": "Standard Curtain",
                "description": "Basic sliding curtain setup with manual operation and secure locking",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/10/OO/ME/DD/36130494/eicher-pro-3015-truck-1000x1000.jpg"
            },
            {
                "title": "Premium Curtain",
                "description": "Enhanced curtain material with better tear resistance and UV protection",
                "image": "https://5.imimg.com/data5/ANDROID/Default/2021/11/KK/MM/GJ/46481591/product-jpeg-1000x1000.jpg"
            },
            {
                "title": "Dual-height System",
                "description": "Adjustable roof height to accommodate taller cargo when needed",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/1/XR/ZU/PN/108537223/eicher-pro-3015-truck-1000x1000.png"
            },
            {
                "title": "Combo Access",
                "description": "Combined sliding curtain sides with rear door access for maximum loading flexibility",
                "image": "https://5.imimg.com/data5/SELLER/Default/2023/7/332186088/QR/XL/JQ/182158761/eicher-3015-truck-1000x1000.jpg"
            }
        ]
    },
    "tata-lpt": {
        "name": "Tata LPT 1613",
        "brand": "Tata",
        "category": "Premium",
        "rating": 4.5,
        "reviews": 28,
        "warranty": "2 Years",
        "material": "High-strength steel cargo body",
        "dimensions": "24ft x 8ft x 7ft (LxWxH)",
        "capacity": "Up to 15 tons",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Tata LPT 1613, 1615, 1618 series",
        "main_image": "static/images/truck-removebg-preview.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/4/SU/QD/WZ/80849576/tata-3618-tip-trailer-1000x1000.jpg",
                "caption": "Tata LPT 1613 Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/2/LH/SD/DZ/122276492/tata-1613-truck-1000x1000.jpg",
                "caption": "Tata LPT 1613 Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/10/XU/AF/TL/2498777/tata-1613-flat-truck-1000x1000.jpg",
                "caption": "Tata LPT 1613 Flatbed"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/12/UA/EH/QR/14444723/tata-1612-high-deck-truck-1000x1000.jpg",
                "caption": "Tata LPT High Deck Configuration"
            }
        ],
        "features": [
            {
                "icon": "fas fa-shield-alt",
                "title": "Reinforced Structure",
                "description": "Steel frame with additional reinforcement at stress points for maximum durability"
            },
            {
                "icon": "fas fa-tint-slash",
                "title": "Anti-Corrosive Coating",
                "description": "Multi-layer anti-rust treatment and weather-resistant paint finish"
            },
            {
                "icon": "fas fa-weight-hanging",
                "title": "Optimized Weight",
                "description": "Lightweight yet strong construction to maximize payload capacity"
            }
        ],
        "custom_options": [
            {
                "title": "Container Body",
                "description": "Fully enclosed storage with secure locking system and waterproof sealing",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/3/DL/CH/KA/41051223/tata-1613-container-body-1000x1000.jpg"
            },
            {
                "title": "Flatbed Design",
                "description": "Open flatbed with removable side panels for versatile loading options",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/10/XU/AF/TL/2498777/tata-1613-flat-truck-1000x1000.jpg"
            },
            {
                "title": "High Deck Option",
                "description": "Increased cargo volume with extended side panels and reinforced floor",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/12/UA/EH/QR/14444723/tata-1612-high-deck-truck-1000x1000.jpg"
            },
            {
                "title": "Tarpaulin Cover",
                "description": "Heavy-duty tarpaulin with frame supports for weather protection",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/12/UR/NQ/UZ/134083312/tata-signa-4825-tk-tractor-1000x1000.jpg"
            }
        ]
    },
    "container": {
        "name": "Multi-Brand Container Body",
        "brand": "Multi-brand",
        "category": "Specialized",
        "rating": 4.8,
        "reviews": 32,
        "warranty": "3 Years",
        "material": "Industrial-grade steel with anti-corrosion treatment",
        "dimensions": "20ft/24ft/32ft x 8ft x 8.5ft (LxWxH)",
        "capacity": "Up to 30 tons depending on configuration",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Tata, Ashok Leyland, BharatBenz, Eicher, and more",
        "main_image": "static/images/container-removebg-preview.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/3/DL/CH/KA/41051223/tata-1613-container-body-1000x1000.jpg",
                "caption": "Standard Container Body - Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/2/GB/WV/LI/24055954/eicher-box-truck-1000x1000.jpg",
                "caption": "Eicher Pro Container Configuration"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/6/WN/XH/ZC/112442360/tata-container-body-1000x1000.png",
                "caption": "Tata Container Body - Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/11/KS/LJ/UG/99306635/ashok-leyland-1616-container-body-1000x1000.jpeg",
                "caption": "Ashok Leyland Container Body"
            }
        ],
        "features": [
            {
                "icon": "fas fa-lock",
                "title": "Advanced Security",
                "description": "Multi-point locking system with tamper-proof design for maximum cargo security"
            },
            {
                "icon": "fas fa-cloud-rain",
                "title": "Weather Protection",
                "description": "Fully sealed design with waterproof construction for all-weather transport"
            },
            {
                "icon": "fas fa-exchange-alt",
                "title": "Versatile Access",
                "description": "Available with rear door, side door, or roll-up door configurations for flexible loading"
            }
        ],
        "custom_options": [
            {
                "title": "Standard Container",
                "description": "Fully enclosed cargo space with rear-door access and secure locking system",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/3/DL/CH/KA/41051223/tata-1613-container-body-1000x1000.jpg"
            },
            {
                "title": "High-Cube Container",
                "description": "Extended height container for increased volume capacity and bulky items",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/6/WN/XH/ZC/112442360/tata-container-body-1000x1000.png"
            },
            {
                "title": "Side-Access Container",
                "description": "Container with additional side door access for convenient loading and unloading",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/11/KS/LJ/UG/99306635/ashok-leyland-1616-container-body-1000x1000.jpeg"
            },
            {
                "title": "Insulated Container",
                "description": "Temperature-stable container with specialized insulation for sensitive cargo",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/7/BF/GC/LM/152879492/refrigerated-truck-body-1000x1000.jpg"
            }
        ]
    },
    "ashok-leyland": {
        "name": "Ashok Leyland Ecomet",
        "brand": "Ashok Leyland",
        "category": "Commercial",
        "rating": 4.0,
        "reviews": 22,
        "warranty": "3 Years",
        "material": "Galvanized steel construction",
        "dimensions": "22ft x 7.5ft x 7ft (LxWxH)",
        "capacity": "Up to 25 tons",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Ashok Leyland Ecomet 1115, 1215, 1415 series",
        "main_image": "static/images/Ashok.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/ANDROID/Default/2022/2/CS/VI/GZ/41617752/product-jpeg-1000x1000.jpg",
                "caption": "Ashok Leyland Ecomet Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/6/322415501/VB/HI/NQ/179693100/al-ecomet-1215-he-cabin-and-chassis-1000x1000.jpg",
                "caption": "Ashok Leyland Ecomet Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/3/QC/XP/JZ/18742983/ecomet-1215-truck-body-1000x1000.jpg",
                "caption": "Ashok Leyland Ecomet Cargo Body"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/12/NY/TS/DO/49274419/ashok-leyland-ecomet-series-truck-1000x1000.jpg",
                "caption": "Ashok Leyland Full Vehicle View"
            }
        ],
        "features": [
            {
                "icon": "fas fa-lock",
                "title": "Secure Locking System",
                "description": "Multi-point locking mechanism for enhanced security during transit"
            },
            {
                "icon": "fas fa-snowflake",
                "title": "Weather Resistant",
                "description": "Special treatment to withstand extreme weather conditions"
            },
            {
                "icon": "fas fa-tools",
                "title": "Easy Maintenance",
                "description": "Modular design for simple repairs and parts replacement"
            }
        ],
        "custom_options": [
            {
                "title": "Heavy-duty Container",
                "description": "Reinforced container body for transporting valuable goods securely",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/3/QC/XP/JZ/18742983/ecomet-1215-truck-body-1000x1000.jpg"
            },
            {
                "title": "Refrigerated Body",
                "description": "Insulated container with cooling unit for temperature-controlled transport",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/5/QT/DA/AB/40732087/14-feet-refrigerated-truck-body-1000x1000.jpeg"
            },
            {
                "title": "Dropside Body",
                "description": "Side panels that can be lowered for easy loading and unloading",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/11/BN/WS/AQ/76818982/ashok-leyland-1616il-truck-1000x1000.png"
            },
            {
                "title": "Water Tanker",
                "description": "Specialized tank body for water transportation with anti-corrosion lining",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/7/WK/ZB/VH/8635450/ashok-ley-1000x1000.JPG"
            }
        ]
    },
    "mahindra-bolero": {
        "name": "Mahindra Bolero Pickup",
        "brand": "Mahindra",
        "category": "Light Commercial",
        "rating": 5.0,
        "reviews": 35,
        "warranty": "2 Years",
        "material": "Aluminum composite panels",
        "dimensions": "9ft x 5.5ft x 5ft (LxWxH)",
        "capacity": "Up to 1.5 tons",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Mahindra Bolero Pickup, Bolero Maxi Truck, Bolero Pik-Up FB",
        "main_image": "/static/images/Pickupp.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/12/YY/OA/LR/143542281/mahindra-bolero-pikup-fb-bs6-cbc-1000x1000.jpg",
                "caption": "Mahindra Bolero Pickup Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/8/KG/QM/ZF/113074393/mahindra-bolero-pick-up-fb-1-7t-bsvi-1000x1000.jpg",
                "caption": "Mahindra Bolero Pickup Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/5/ZI/IK/OU/146131321/mahindra-pickup-1000x1000.jpeg",
                "caption": "Mahindra Bolero Pickup Cargo Area"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/8/OV/VV/EQ/129974989/mahindra-bolero-pickup-1000x1000.jpg",
                "caption": "Mahindra Bolero Full Vehicle"
            }
        ],
        "features": [
            {
                "icon": "fas fa-weight",
                "title": "Lightweight Design",
                "description": "Aluminum construction reduces vehicle weight for improved fuel efficiency"
            },
            {
                "icon": "fas fa-expand-arrows-alt",
                "title": "Customizable Size",
                "description": "Multiple size options to fit different Bolero chassis configurations"
            },
            {
                "icon": "fas fa-ban",
                "title": "Dent Resistant",
                "description": "Composite panels resist minor impacts and maintain appearance"
            }
        ],
        "custom_options": [
            {
                "title": "Closed Container",
                "description": "Fully enclosed cargo area with rear door for secure transport",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/8/OV/VV/EQ/129974989/mahindra-bolero-pickup-1000x1000.jpg"
            },
            {
                "title": "Canopy Cover",
                "description": "Semi-enclosed design with removable canopy for versatile usage",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/5/ZI/IK/OU/146131321/mahindra-pickup-1000x1000.jpeg"
            },
            {
                "title": "Flatbed Deck",
                "description": "Open deck with low side panels for easy loading of bulky items",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/8/KG/QM/ZF/113074393/mahindra-bolero-pick-up-fb-1-7t-bsvi-1000x1000.jpg"
            },
            {
                "title": "Delivery Van",
                "description": "Custom delivery body with side door for courier and delivery services",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/4/CZ/RS/VF/151417903/mahindra-delivery-van-1000x1000.png"
            }
        ]
    },
    "eicher": {
        "name": "Eicher Pro 3015",
        "brand": "Eicher",
        "category": "Medium Duty",
        "rating": 4.0,
        "reviews": 18,
        "warranty": "2 Years",
        "material": "Mild steel with reinforced frame",
        "dimensions": "19ft x 7ft x 7ft (LxWxH)",
        "capacity": "Up to 10 tons",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Eicher Pro 3015, 3014, 3016 series",
        "main_image": "/static/images/Eicherr.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/11/IE/WN/UQ/29442415/eicher-pro-3015-truck-1000x1000.jpg",
                "caption": "Eicher Pro 3015 Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/3/GH/SP/LZ/131351989/eicher-pro-3015-cbc-truck-1000x1000.jpeg",
                "caption": "Eicher Pro 3015 Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/2/GB/WV/LI/24055954/eicher-box-truck-1000x1000.jpg",
                "caption": "Eicher Pro Box Container"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/7/332186088/QR/XL/JQ/182158761/eicher-3015-truck-1000x1000.jpg",
                "caption": "Eicher Pro Full Vehicle"
            }
        ],
        "features": [
            {
                "icon": "fas fa-wind",
                "title": "Aerodynamic Design",
                "description": "Shaped for reduced air resistance to improve fuel efficiency"
            },
            {
                "icon": "fas fa-ruler-combined",
                "title": "Extended Length",
                "description": "Available in multiple length options for increased cargo capacity"
            },
            {
                "icon": "fas fa-layer-group",
                "title": "Multi-tier Loading",
                "description": "Internal racking system allows for stacked cargo arrangement"
            }
        ],
        "custom_options": [
            {
                "title": "Box Container",
                "description": "Fully enclosed cargo area with rear and side access doors",
                "image": "https://5.imimg.com/data5/SELLER/Default/2023/2/GB/WV/LI/24055954/eicher-box-truck-1000x1000.jpg"
            },
            {
                "title": "High-side Open Body",
                "description": "Open top design with tall side panels for bulky items",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/3/GH/SP/LZ/131351989/eicher-pro-3015-cbc-truck-1000x1000.jpeg"
            },
            {
                "title": "Platform Body",
                "description": "Flat platform with minimal sides for machinery transport",
                "image": "https://5.imimg.com/data5/SELLER/Default/2023/7/332186088/QR/XL/JQ/182158761/eicher-3015-truck-1000x1000.jpg"
            },
            {
                "title": "Curtain-side Body",
                "description": "Side curtains that can be opened for full access to cargo area",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/10/OO/ME/DD/36130494/eicher-pro-3015-truck-1000x1000.jpg"
            }
        ]
    },
    "tata-ace": {
        "name": "Tata Ace",
        "brand": "Tata",
        "category": "Bestseller",
        "rating": 4.5,
        "reviews": 42,
        "warranty": "2 Years",
        "material": "Lightweight steel with rust-resistant coating",
        "dimensions": "8.2ft x 5.3ft x 5.5ft (LxWxH)",
        "capacity": "Up to 1 ton",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Tata Ace, Ace Zip, Ace Mega, Super Ace",
        "main_image": "/static/images/TataAce.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2023/2/RK/AJ/KP/171334372/tata-ace-gold-chhota-hathi-1000x1000.jpg",
                "caption": "Tata Ace Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/5/LA/XO/UI/28246811/tata-ace-mini-truck-1000x1000.jpg",
                "caption": "Tata Ace Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/3/PM/YA/QZ/118075812/1000x1000.jpg",
                "caption": "Tata Ace Cargo Area"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/10/NI/CS/DO/44048467/ace-gold-1000x1000.jpg",
                "caption": "Tata Ace Full Vehicle"
            }
        ],
        "features": [
            {
                "icon": "fas fa-balance-scale",
                "title": "Balanced Design",
                "description": "Optimized weight distribution for stability with full loads"
            },
            {
                "icon": "fas fa-battery-full",
                "title": "Low Maintenance",
                "description": "Simplified components requiring minimal servicing"
            },
            {
                "icon": "fas fa-door-open",
                "title": "Easy Access",
                "description": "Multiple access points for convenient loading and unloading"
            }
        ],
        "custom_options": [
            {
                "title": "Delivery Van Body",
                "description": "Enclosed cargo area with rear door for parcel delivery",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/10/NI/CS/DO/44048467/ace-gold-1000x1000.jpg"
            },
            {
                "title": "High-side Open Deck",
                "description": "Open top cargo area with tall side panels",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/5/LA/XO/UI/28246811/tata-ace-mini-truck-1000x1000.jpg"
            },
            {
                "title": "Food Truck Conversion",
                "description": "Custom food service body with serving window and interior fixtures",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/2/QN/CE/SK/126728923/tata-ace-food-truck-1000x1000.jpg"
            },
            {
                "title": "Refrigerated Box",
                "description": "Insulated container with cooling system for perishable goods",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/9/NN/LA/KX/115075618/tata-ace-refrigerated-van-1000x1000.jpg"
            }
        ]
    },
    "dumper": {
        "name": "Tipper/Dumper Body",
        "brand": "Multi-brand",
        "category": "Heavy Duty",
        "rating": 5.0,
        "reviews": 30,
        "warranty": "3 Years",
        "material": "Heavy-duty steel with abrasion-resistant lining",
        "dimensions": "Customizable to chassis",
        "capacity": "10-30 tons depending on configuration",
        "location": "Dabhan, Gujarat",
        "compatible_chassis": "Tata, Ashok Leyland, Eicher, BharatBenz, and more",
        "main_image": "/static/images/Dumper.png",
        "gallery_images": [
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2021/6/BU/QV/ON/40732087/tipper-body-1000x1000.jpg",
                "caption": "Tipper Body Front View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/9/EO/HE/CS/10972520/tipper-body-fabrication-1000x1000.jpeg",
                "caption": "Tipper Body Side View"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2022/12/OQ/PC/AJ/161911773/tata-2518-tipper-body-1000x1000.jpg",
                "caption": "Tipper in Action"
            },
            {
                "url": "https://5.imimg.com/data5/SELLER/Default/2020/10/LX/TY/UJ/14444723/9014-hydraulic-tipper-1000x1000.jpg",
                "caption": "Hydraulic System View"
            }
        ],
        "features": [
            {
                "icon": "fas fa-cog",
                "title": "Hydraulic System",
                "description": "Powerful hydraulic lifting mechanism for smooth and reliable operation"
            },
            {
                "icon": "fas fa-hammer",
                "title": "Impact Resistant",
                "description": "Reinforced design to withstand heavy impacts from loaded materials"
            },
            {
                "icon": "fas fa-sync-alt",
                "title": "Multi-way Tipping",
                "description": "Options for rear-only or three-way tipping functionality"
            }
        ],
        "custom_options": [
            {
                "title": "Rock Body",
                "description": "Extra reinforced body designed for quarry and mining applications",
                "image": "https://5.imimg.com/data5/SELLER/Default/2021/6/BU/QV/ON/40732087/tipper-body-1000x1000.jpg"
            },
            {
                "title": "Construction Tipper",
                "description": "Standard configuration for construction site material transport",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/9/EO/HE/CS/10972520/tipper-body-fabrication-1000x1000.jpeg"
            },
            {
                "title": "Coal Carrier",
                "description": "Specialized design with higher sides for coal transportation",
                "image": "https://5.imimg.com/data5/SELLER/Default/2022/12/OQ/PC/AJ/161911773/tata-2518-tipper-body-1000x1000.jpg"
            },
            {
                "title": "Agricultural Tipper",
                "description": "Lighter design with grain-proof sealing for agricultural products",
                "image": "https://5.imimg.com/data5/SELLER/Default/2020/10/LX/TY/UJ/14444723/9014-hydraulic-tipper-1000x1000.jpg"
            }
        ]
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/models')
def models():
    return render_template('models.html', truck_models=truck_models)

@app.route('/models/<model_id>')
def model_detail(model_id):
    # Get the model data from our dictionary
    model = truck_models.get(model_id)
    
    # If model not found, redirect to models page
    if not model:
        return redirect('/models')
    
    # Add analytics tracking (optional)
    # Log the model view if needed
    
    # Render the template with the model data and model_id
    return render_template('model_detail.html', model=model, model_id=model_id, truck_models=truck_models)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/setup-formspree')
def setup_formspree():
    """Helper route to set up Formspree for the first time"""
    return render_template('setup_formspree.html', admin_email=ADMIN_EMAIL, FORMSPREE_ID=FORMSPREE_ID)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')
        
        # Create formatted message for WhatsApp
        whatsapp_message = f"""Contact Form Submission:
Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}
Message: {message}
        """
        
        # Create WhatsApp link with the contact info
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_link = f"https://api.whatsapp.com/send?phone={ADMIN_PHONE}&text={encoded_message}"
        
        # Store email data for Formspree
        form_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message
        }
        
        # Formspree URL for the backup/alternative email method
        formspree_url = f"https://formspree.io/f/{FORMSPREE_ID}"
        
        # Show confirmation page with WhatsApp link and form data for email
        flash('Your message has been sent successfully!', 'success')
        return render_template('contact_success.html', 
                              whatsapp_link=whatsapp_link,
                              formspree_url=formspree_url,
                              form_data=form_data)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        model = request.form['model']
        specs = request.form['specs']
        location = request.form['location']
        timeline = request.form.get('timeline', 'Not specified')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        image = request.files['image']
        
        # Create a unique filename for the image to prevent overwriting
        if image and image.filename:
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}")
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            full_image_url = request.url_root.rstrip('/') + '/' + image_path
            relative_image_url = '/' + image_path
        else:
            full_image_url = None
            relative_image_url = None

        # Save order details
        truck_info = {
            'model': model,
            'specs': specs,
            'location': location,
            'timeline': timeline,
            'email': email,
            'phone': phone,
            'image_url': relative_image_url,
            'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to in-memory list
        truck_data.append(truck_info)
        
        # Generate WhatsApp link for the order
        whatsapp_message = f"""New Truck Order:
Model: {model}
Specifications: {specs}
Location: {location}
Timeline: {timeline}
Email: {email}
Phone: {phone}
Order Date: {truck_info['order_date']}"""
        
        if full_image_url:
            whatsapp_message += f"\nImage: {full_image_url}"
        
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_link = f"https://api.whatsapp.com/send?phone={ADMIN_PHONE}&text={encoded_message}"
        
        # Prepare data for Formspree
        email_message = f"""
Model: {model}
Specifications: {specs}
Location: {location}
Timeline: {timeline}
Order Date: {truck_info['order_date']}

Customer Contact:
Email: {email}
Phone: {phone}
"""
        if full_image_url:
            email_message += f"\nImage URL: {full_image_url}"
        
        # For emails, use Formspree
        formspree_url = f"https://formspree.io/f/{FORMSPREE_ID}"
        
        # Try to directly send to Formspree via API if possible
        try:
            # Formspree API endpoint
            formspree_endpoint = f"https://formspree.io/f/{FORMSPREE_ID}"
            
            # Data to send
            form_data = {
                'name': f"Order: {model}",
                'email': email,
                'phone': phone,
                'subject': f"New Truck Order: {model}",
                'message': email_message,
            }
            
            if full_image_url:
                form_data['image_url'] = full_image_url
                
            # Send data to Formspree
            response = requests.post(
                formspree_endpoint,
                data=form_data,
                headers={
                    'Accept': 'application/json',
                    'Referer': request.base_url
                }
            )
            
            if response.status_code == 200:
                print("Email sent directly to Formspree API!")
            else:
                print(f"Formspree API error: {response.status_code}")
                
        except Exception as e:
            print(f"Error sending to Formspree: {e}")
        
        # Show confirmation page with WhatsApp link
        flash('Your order has been successfully submitted! Our team will contact you soon.', 'success')
            
        return render_template(
            'order_confirmation.html', 
            truck_info=truck_info,
            whatsapp_link=whatsapp_link,
            formspree_url=formspree_url,
            form_data={
                'name': f"Order: {model}",
                'email': email,
                'phone': phone,
                'subject': f"New Truck Order: {model}",
                'message': email_message,
                'image_url': full_image_url
            }
        )
    
    # For GET requests, just render the form
    # If model is provided in URL parameters, it will be handled by the template
    selected_model = request.args.get('model', '')
    return render_template('order.html', selected_model=selected_model)

@app.route('/order-thank-you')
def order_thank_you():
    """
    Handle redirect from Formspree after form submission.
    This shows the confirmation page after Formspree processes the form.
    """
    # Get form data from query parameters (Formspree includes them in the redirect)
    model = request.args.get('model', 'Not specified')
    specs = request.args.get('specs', 'Not specified')
    location = request.args.get('location', 'Not specified')
    timeline = request.args.get('timeline', 'Not specified')
    email = request.args.get('email', 'Not provided')
    phone = request.args.get('phone', 'Not provided')
    
    # Create truck info object
    truck_info = {
        'model': model,
        'specs': specs,
        'location': location,
        'timeline': timeline,
        'email': email,
        'phone': phone,
        'image_url': None,  # Images don't get redirected from Formspree
        'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Generate WhatsApp link
    whatsapp_message = f"""New Truck Order:
Model: {model}
Specifications: {specs}
Location: {location}
Timeline: {timeline}
Email: {email}
Phone: {phone}
Order Date: {truck_info['order_date']}"""
    
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_link = f"https://api.whatsapp.com/send?phone={ADMIN_PHONE}&text={encoded_message}"
    
    # Formspree URL for reference
    formspree_url = f"https://formspree.io/f/{FORMSPREE_ID}"
    
    # Show success message
    flash('Your order has been successfully submitted! Our team will contact you soon.', 'success')
    
    # Return confirmation template
    return render_template(
        'order_confirmation.html',
        truck_info=truck_info,
        whatsapp_link=whatsapp_link,
        formspree_url=formspree_url,
        form_data={
            'name': f"Order: {model}",
            'email': email,
            'phone': phone,
            'subject': f"New Truck Order: {model}",
            'message': "Order submitted via Formspree"
        }
    )

if __name__ == '__main__':
    # Load existing images
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            truck_data.append({
                'model': 'Previously Uploaded',
                'specs': 'N/A',
                'location': 'N/A',
                'image_url': '/' + os.path.join(UPLOAD_FOLDER, filename)
            })
    # Use environment variables for host and port if available (for production)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
