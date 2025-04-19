# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Store truck data
truck_data = []

# Sample truck models data
truck_models = {
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
        "location": "Delhi",
        "compatible_chassis": "Tata LPT 1613, 1615, 1618 series",
        "main_image": "https://5.imimg.com/data5/SELLER/Default/2023/4/SU/QD/WZ/80849576/tata-3618-tip-trailer-1000x1000.jpg",
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
        "location": "Mumbai",
        "compatible_chassis": "Ashok Leyland Ecomet 1115, 1215, 1415 series",
        "main_image": "https://5.imimg.com/data5/ANDROID/Default/2022/2/CS/VI/GZ/41617752/product-jpeg-1000x1000.jpg",
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
        "location": "Gujarat",
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
        "location": "Chennai",
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
        "location": "Delhi",
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
        "location": "Pune",
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
    
    return render_template('model_detail.html', model=model)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add-truck', methods=['GET', 'POST'])
def add_truck():
    if request.method == 'POST':
        model = request.form['model']
        specs = request.form['specs']
        location = request.form['location']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            truck_data.append({
                'model': model,
                'specs': specs,
                'location': location,
                'image_url': '/' + image_path
            })
        return redirect(url_for('home'))
    return render_template('add_truck.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # Load existing images
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            truck_data.append({
                'model': 'Previously Uploaded',
                'specs': 'N/A',
                'location': 'N/A',
                'image_url': '/' + os.path.join(UPLOAD_FOLDER, filename)
            })
    app.run(debug=True)
