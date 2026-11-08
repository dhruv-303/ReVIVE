import os
import sys
import uuid
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from models import db, User, Category, Product, Subscription, Offer, Order, Review, DeviceDiagnostic

def seed_database():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding ReVive refurbished marketplace database with comprehensive, classy tech catalog...")
        db.drop_all()
        db.create_all()

        # ---------------------------------------------------------------------
        # 1. CATEGORIES (6 Comprehensive Refurbished Electronics Segments)
        # ---------------------------------------------------------------------
        categories_data = [
            {
                'name': 'Laptops & MacBooks',
                'slug': 'laptops',
                'description': 'Student-certified refurbished MacBooks, ThinkPads, and Dell XPS ultrabooks benchmarked for campus computing.',
                'icon': 'laptop'
            },
            {
                'name': 'Smartphones',
                'slug': 'smartphones',
                'description': 'Factory-unlocked iPhones, Samsung Galaxy, and Google Pixel devices with verified 90%+ battery health and pristine OLED displays.',
                'icon': 'smartphone'
            },
            {
                'name': 'Audio & Headphones',
                'slug': 'audio',
                'description': 'Active noise-canceling headphones, AirPods, and studio monitors ultrasonically sanitized with replacement hygiene cushions.',
                'icon': 'headphones'
            },
            {
                'name': 'Tablets & iPads',
                'slug': 'tablets',
                'description': 'Certified iPads and Galaxy Tabs with stylus support and flawless touch digitizers for lecture notes & digital sketching.',
                'icon': 'tablet'
            },
            {
                'name': 'Wearables & Smartwatches',
                'slug': 'wearables',
                'description': 'Apple Watches, Galaxy Watches, and Garmin fitness trackers with calibrated heart rate sensors and new antimicrobial bands.',
                'icon': 'watch'
            },
            {
                'name': 'PC Components & Gaming',
                'slug': 'gaming',
                'description': 'Stress-tested GPUs with fresh thermal paste, mechanical keyboards, gaming consoles, and high-refresh monitors.',
                'icon': 'gamepad'
            }
        ]

        cat_objs = {}
        for cat in categories_data:
            c = Category(**cat)
            db.session.add(c)
            cat_objs[cat['slug']] = c
        db.session.commit()
        print(f"  ✅ Seeded {len(categories_data)} Categories")

        # ---------------------------------------------------------------------
        # 2. USERS (Sellers & Buyers from Top Universities)
        # ---------------------------------------------------------------------
        users_data = [
            {
                'username': 'aryan_refurbs',
                'email': 'seller@revive.edu',
                'full_name': 'Aryan Sharma',
                'phone': '+91 98765 43210',
                'role': 'seller',
                'subscription_plan': 'Campus Pro',
                'subscription_status': 'active',
                'college_name': 'Delhi Technological University (DTU)',
                'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop&q=80'
            },
            {
                'username': 'priya_tech',
                'email': 'priya@revive.edu',
                'full_name': 'Priya Patel',
                'phone': '+91 98234 56789',
                'role': 'seller',
                'subscription_plan': 'Student Starter',
                'subscription_status': 'active',
                'college_name': 'National Institute of Technology (NIT Trichy)',
                'avatar_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&auto=format&fit=crop&q=80'
            },
            {
                'username': 'vikram_hardware',
                'email': 'vikram@revive.edu',
                'full_name': 'Vikram Malhotra',
                'phone': '+91 97123 45678',
                'role': 'seller',
                'subscription_plan': 'Master Refurbisher',
                'subscription_status': 'active',
                'college_name': 'Indian Institute of Technology (IIT Bombay)',
                'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80'
            },
            {
                'username': 'ananya_gadgets',
                'email': 'ananya@revive.edu',
                'full_name': 'Ananya Sen',
                'phone': '+91 99345 67890',
                'role': 'seller',
                'subscription_plan': 'Campus Pro',
                'subscription_status': 'active',
                'college_name': 'BITS Pilani (Goa Campus)',
                'avatar_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&auto=format&fit=crop&q=80'
            },
            {
                'username': 'rohit_student',
                'email': 'buyer@revive.edu',
                'full_name': 'Rohit Verma',
                'phone': '+91 91234 56780',
                'role': 'buyer',
                'subscription_plan': 'Student Starter',
                'subscription_status': 'active',
                'college_name': 'Birla Institute of Technology (BITS Pilani)',
                'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&auto=format&fit=crop&q=80'
            },
            {
                'username': 'neha_cs',
                'email': 'neha@revive.edu',
                'full_name': 'Neha Gupta',
                'phone': '+91 98451 23456',
                'role': 'buyer',
                'subscription_plan': 'Student Starter',
                'subscription_status': 'active',
                'college_name': 'Delhi Technological University (DTU)',
                'avatar_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&auto=format&fit=crop&q=80'
            }
        ]

        user_objs = {}
        for u_data in users_data:
            user = User(
                username=u_data['username'],
                email=u_data['email'],
                full_name=u_data['full_name'],
                phone=u_data['phone'],
                role=u_data['role'],
                subscription_plan=u_data['subscription_plan'],
                subscription_status=u_data['subscription_status'],
                college_name=u_data['college_name'],
                avatar_url=u_data['avatar_url']
            )
            user.set_password('password123')
            db.session.add(user)
            user_objs[u_data['username']] = user
        db.session.commit()
        print(f"  ✅ Seeded {len(users_data)} Verified Campus Users")

        # ---------------------------------------------------------------------
        # 3. SUBSCRIPTIONS (Seller Plans)
        # ---------------------------------------------------------------------
        subs = [
            Subscription(
                user_id=user_objs['aryan_refurbs'].id,
                plan_name='Campus Pro',
                price_monthly=799.00,
                billing_cycle='monthly',
                max_listings=25,
                commission_rate=4.00,
                status='active',
                features='25 active listings; Featured marketplace placements; 4% platform fee; Fast 12h campus payout; Free ReVive diagnostic seals'
            ),
            Subscription(
                user_id=user_objs['priya_tech'].id,
                plan_name='Student Starter',
                price_monthly=0.00,
                billing_cycle='free',
                max_listings=5,
                commission_rate=8.00,
                status='active',
                features='5 active listings; Verified Student Refurbisher badge; Make an Offer support; 8% platform fee'
            ),
            Subscription(
                user_id=user_objs['vikram_hardware'].id,
                plan_name='Master Refurbisher',
                price_monthly=1999.00,
                billing_cycle='monthly',
                max_listings=100,
                commission_rate=2.00,
                status='active',
                features='Unlimited listings; Top homepage spotlight; 2% fee; Direct campus kiosk pickup partner; 12-Month warranty backing'
            ),
            Subscription(
                user_id=user_objs['ananya_gadgets'].id,
                plan_name='Campus Pro',
                price_monthly=799.00,
                billing_cycle='monthly',
                max_listings=25,
                commission_rate=4.00,
                status='active',
                features='25 active listings; Priority campus search; 4% fee; Rapid student escrow payouts'
            )
        ]
        db.session.add_all(subs)
        db.session.commit()
        print("  ✅ Seeded Seller Subscriptions")

        # ---------------------------------------------------------------------
        # 4. PRODUCTS (24+ High-End, Classy Refurbished Tech Items)
        # ---------------------------------------------------------------------
        seller_aryan = user_objs['aryan_refurbs'].id
        seller_priya = user_objs['priya_tech'].id
        seller_vikram = user_objs['vikram_hardware'].id
        seller_ananya = user_objs['ananya_gadgets'].id

        cat_lap = cat_objs['laptops'].id
        cat_phone = cat_objs['smartphones'].id
        cat_aud = cat_objs['audio'].id
        cat_tab = cat_objs['tablets'].id
        cat_wear = cat_objs['wearables'].id
        cat_gam = cat_objs['gaming'].id

        products_list = [
            # --- LAPTOPS & MACBOOKS ---
            {
                'title': 'Apple MacBook Air 13" (M1 Chip, 8GB RAM, 256GB SSD) - Space Gray',
                'slug': 'apple-macbook-air-m1-256gb-space-gray',
                'description': 'Student-certified refurbished MacBook Air M1. Pristine anodized aluminum body with zero cosmetic dents. Keyboard and Force Touch trackpad re-certified. Battery at 96% original capacity with only 82 cycles. Includes original 30W USB-C adapter and braided power cable.',
                'category_id': cat_lap,
                'seller_id': seller_aryan,
                'original_price': 84900.00,
                'refurbished_price': 48990.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 96,
                'tested_points': 34,
                'carbon_saved_kg': 52.4,
                'specifications': 'Apple M1 Chip (8-Core CPU / 7-Core GPU); 8GB Unified Memory; 256GB PCIe SSD; 13.3" Retina TrueTone Display; 82 Battery Cycles; macOS Sequoia fresh installation; MagSafe 3 compatible USB-C.',
                'image_url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Apple MacBook Pro 14" (M2 Pro 10-Core, 16GB RAM, 512GB SSD) - Space Black',
                'slug': 'apple-macbook-pro-14-m2-pro-space-black',
                'description': 'Powerhouse workstation for CS, video editing, and software engineers. Liquid Retina XDR 120Hz ProMotion display tested for 100% color gamut uniformity. Studio-quality 3-mic array and 6-speaker spatial audio system inspected.',
                'category_id': cat_lap,
                'seller_id': seller_vikram,
                'original_price': 199900.00,
                'refurbished_price': 134900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 98,
                'tested_points': 38,
                'carbon_saved_kg': 68.0,
                'specifications': 'Apple M2 Pro (10-Core CPU / 16-Core GPU); 16GB Unified RAM (200GB/s bandwidth); 512GB NVMe SSD (up to 7.4GB/s); 14.2" Liquid Retina XDR Mini-LED (1600 nits peak); HDMI 2.1 & SDXC slot; 98% Battery health.',
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Lenovo ThinkPad X1 Carbon Gen 9 (Intel i7 11th Gen, 16GB, 512GB SSD)',
                'slug': 'lenovo-thinkpad-x1-carbon-gen9-i7',
                'description': 'Ultralight carbon-fiber business laptop. Thermals repasted with Arctic MX-6 compound. Legendary ThinkPad tactile keyboard with trackpoint. Windows 11 Pro activated clean license. Ideal for coding and research.',
                'category_id': cat_lap,
                'seller_id': seller_priya,
                'original_price': 129900.00,
                'refurbished_price': 44500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 92,
                'tested_points': 32,
                'carbon_saved_kg': 46.5,
                'specifications': 'Intel Core i7-1165G7 Quad-Core up to 4.7GHz; 16GB LPDDR4x RAM; 512GB PCIe NVMe SSD; 14.0" FHD+ 16:10 Anti-glare Display (400 nits); Dual Thunderbolt 4; Fingerprint power button; 57Wh Battery.',
                'image_url': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Dell XPS 15 9520 (Intel i7 12th Gen, 32GB RAM, 1TB SSD, RTX 3050 Ti) - Platinum Silver',
                'slug': 'dell-xps-15-9520-i7-32gb-rtx',
                'description': 'CNC machined aluminum chassis with carbon fiber composite palm rest. 3.5K OLED InfinityEdge touch display with deep blacks. Dual fan cooling system ultrasonic deep-cleaned.',
                'category_id': cat_lap,
                'seller_id': seller_ananya,
                'original_price': 185000.00,
                'refurbished_price': 89500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 94,
                'tested_points': 36,
                'carbon_saved_kg': 58.2,
                'specifications': 'Intel Core i7-12700H (14-Core up to 4.7GHz); 32GB DDR5 4800MHz Dual-Channel; 1TB PCIe 4.0 NVMe SSD; NVIDIA GeForce RTX 3050 Ti 4GB; 15.6" 3.5K (3456x2160) OLED Touch; 86Wh Battery.',
                'image_url': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'ASUS ROG Zephyrus G14 (AMD Ryzen 9 7940HS, 16GB DDR5, RTX 4060, 165Hz) - Moonlight White',
                'slug': 'asus-rog-zephyrus-g14-ryzen9-rtx4060',
                'description': 'Portable 14-inch gaming and ML powerhouse. Liquid metal CPU thermal interface verified. ROG Nebula 165Hz Display with 100% DCI-P3 color gamut. MUX Switch with NVIDIA Advanced Optimus.',
                'category_id': cat_lap,
                'seller_id': seller_vikram,
                'original_price': 159990.00,
                'refurbished_price': 98900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 95,
                'tested_points': 36,
                'carbon_saved_kg': 54.0,
                'specifications': 'AMD Ryzen 9 7940HS (8-Core / 16-Thread up to 5.2GHz); 16GB DDR5 4800MHz; 1TB PCIe Gen4 SSD; NVIDIA GeForce RTX 4060 8GB GDDR6 (125W TGP); 14" QHD+ 165Hz 3ms ROG Nebula Display; 76Wh Battery.',
                'image_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Apple MacBook Air 15" (M2 Chip, 16GB RAM, 512GB SSD) - Midnight Blue',
                'slug': 'apple-macbook-air-15-m2-midnight',
                'description': 'Spacious 15.3-inch Liquid Retina display in a razor-thin 11.5mm unibody design. Silent fanless architecture. 66W MagSafe charger included with braided color-matched cable.',
                'category_id': cat_lap,
                'seller_id': seller_aryan,
                'original_price': 154900.00,
                'refurbished_price': 102900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 97,
                'tested_points': 34,
                'carbon_saved_kg': 56.1,
                'specifications': 'Apple M2 (8-Core CPU / 10-Core GPU); 16GB Unified RAM; 512GB SSD; 15.3" Liquid Retina Display (500 nits); Six-speaker sound system with force-cancelling woofers; 1080p FaceTime HD camera.',
                'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },

            # --- SMARTPHONES ---
            {
                'title': 'Apple iPhone 14 Pro 128GB - Deep Purple (Factory Unlocked)',
                'slug': 'iphone-14-pro-128gb-deep-purple',
                'description': 'Factory refurbished iPhone 14 Pro with ProMotion 120Hz Ceramic Shield display. Dynamic Island fully tested. 48MP triple camera array calibrated for 4K ProRES video. Carrier unlocked for all Indian and international eSIMs.',
                'category_id': cat_phone,
                'seller_id': seller_aryan,
                'original_price': 119900.00,
                'refurbished_price': 62990.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 3,
                'status': 'available',
                'battery_health': 94,
                'tested_points': 36,
                'carbon_saved_kg': 38.0,
                'specifications': 'Apple A16 Bionic 4nm Chip; 128GB Storage; 6.1" Super Retina XDR OLED (1-120Hz ProMotion, 2000 nits outdoor peak); 48MP Main + 12MP Telephoto + 12MP Ultrawide; Face ID; Battery Health 94%.',
                'image_url': 'https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Apple iPhone 15 Pro 256GB - Natural Titanium (Ceramic Shield)',
                'slug': 'iphone-15-pro-256gb-natural-titanium',
                'description': 'Aerospace-grade titanium unibody with contoured edges. Customizable Action button. USB-C port with USB 3 speeds (10Gbps). Ray-tracing capable A17 Pro chip. Zero scratches, pristine condition.',
                'category_id': cat_phone,
                'seller_id': seller_vikram,
                'original_price': 134900.00,
                'refurbished_price': 89900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 99,
                'tested_points': 38,
                'carbon_saved_kg': 41.5,
                'specifications': 'Apple A17 Pro (3nm architecture, 6-core GPU); 256GB Storage; 6.1" Super Retina XDR Always-On OLED (120Hz ProMotion); Action Button; 48MP Next-gen portrait sensor; USB-C 3.0 (10Gbps).',
                'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Samsung Galaxy S23 Ultra 256GB - Phantom Black (200MP + S-Pen)',
                'slug': 'samsung-galaxy-s23-ultra-256gb-phantom-black',
                'description': 'Ultimate Android flagship with integrated S-Pen stylus. 200MP main camera with 100x Space Zoom. Corning Gorilla Glass Victus 2 front & back with zero micro-scratches. Certified battery tested at 93%.',
                'category_id': cat_phone,
                'seller_id': seller_ananya,
                'original_price': 124999.00,
                'refurbished_price': 66900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 93,
                'tested_points': 36,
                'carbon_saved_kg': 39.8,
                'specifications': 'Snapdragon 8 Gen 2 for Galaxy; 12GB LPDDR5X RAM; 256GB UFS 4.0; 6.8" Edge QHD+ Dynamic AMOLED 2X (1-120Hz, 1750 nits); Built-in Bluetooth S-Pen; 200MP Quad Camera; 5000mAh Battery (45W fast charge).',
                'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Google Pixel 8 Pro 128GB - Bay Blue (Tensor G3, Super Actua OLED)',
                'slug': 'google-pixel-8-pro-128gb-bay-blue',
                'description': 'Google AI flagship with Best Take, Audio Magic Eraser, and 7 years of official Android OS updates. Matte glass finish with polished aluminum camera visor. Thermometer sensor calibrated.',
                'category_id': cat_phone,
                'seller_id': seller_priya,
                'original_price': 106999.00,
                'refurbished_price': 58500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 95,
                'tested_points': 34,
                'carbon_saved_kg': 36.2,
                'specifications': 'Google Tensor G3 & Titan M2 Security; 12GB LPDDR5X RAM; 128GB UFS 3.1; 6.7" Super Actua OLED (1-120Hz, 2400 nits); 50MP Main + 48MP 5x Telephoto + 48MP Ultrawide; 5050mAh Battery.',
                'image_url': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'OnePlus 12 512GB - Emerald Green (Snapdragon 8 Gen 3, 100W SuperVOOC)',
                'slug': 'oneplus-12-512gb-emerald-green',
                'description': 'Speed powerhouse with 16GB RAM and 512GB storage. 4th Gen Hasselblad Camera system. Includes original 100W fast charger capable of 1-100% top-up in 26 minutes.',
                'category_id': cat_phone,
                'seller_id': seller_aryan,
                'original_price': 69999.00,
                'refurbished_price': 47500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 96,
                'tested_points': 32,
                'carbon_saved_kg': 35.0,
                'specifications': 'Snapdragon 8 Gen 3 (4nm); 16GB LPDDR5X RAM; 512GB UFS 4.0; 6.82" 2K 120Hz ProXDR Display (4500 nits peak); Hasselblad 50MP LYT-808 sensor; 5400mAh Dual-Cell Battery; 100W SuperVOOC Charger.',
                'image_url': 'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Apple iPhone 13 128GB - Starlight (Ceramic Shield & Cinematic Mode)',
                'slug': 'apple-iphone-13-128gb-starlight',
                'description': 'Budget champion refurbished iPhone with phenomenal dual camera performance, battery life, and iOS 18 support. Minor hairline micro-scratch on back edge (Grade B), 100% verified functional.',
                'category_id': cat_phone,
                'seller_id': seller_priya,
                'original_price': 59900.00,
                'refurbished_price': 33900.00,
                'condition_grade': 'Grade B - Very Good',
                'warranty_months': 6,
                'stock_quantity': 3,
                'status': 'available',
                'battery_health': 90,
                'tested_points': 30,
                'carbon_saved_kg': 32.5,
                'specifications': 'Apple A15 Bionic; 128GB Storage; 6.1" Super Retina XDR OLED; 12MP Wide with Sensor-Shift OIS + 12MP Ultrawide; Cinematic Mode in 1080p 30fps; Ceramic Shield Front; 90% Battery capacity.',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },

            # --- AUDIO & HEADPHONES ---
            {
                'title': 'Sony WH-1000XM4 Wireless Noise-Canceling Headphones - Black',
                'slug': 'sony-wh-1000xm4-anc-headphones',
                'description': 'Gold-standard noise-canceling headphones for university libraries. Sanitized with medical-grade isopropyl, fitted with fresh brand-new memory foam ear cushions. Multipoint Bluetooth tested.',
                'category_id': cat_aud,
                'seller_id': seller_priya,
                'original_price': 29990.00,
                'refurbished_price': 14990.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 98,
                'tested_points': 28,
                'carbon_saved_kg': 18.0,
                'specifications': 'Dual Noise Sensor technology; 30-hour battery life with quick charging (10 min = 5 hours); Touch sensor controls; Speak-to-chat; Multipoint connection for 2 simultaneous devices.',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Apple AirPods Pro 2nd Gen with USB-C MagSafe Case (Active Noise Cancellation)',
                'slug': 'apple-airpods-pro-2-usbc',
                'description': 'H2-chip powered AirPods Pro with 2x stronger Active Noise Cancellation, Adaptive Audio, and Transparency mode. Thoroughly sanitized with new hygienic silicone ear tips (XS, S, M, L included).',
                'category_id': cat_aud,
                'seller_id': seller_aryan,
                'original_price': 24900.00,
                'refurbished_price': 14490.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 3,
                'status': 'available',
                'battery_health': 98,
                'tested_points': 30,
                'carbon_saved_kg': 12.0,
                'specifications': 'Apple H2 chip & U1 MagSafe Case; USB-C Charging Port; Up to 6 hours listening time with ANC (30 hours with case); Precision Finding with built-in case speaker; IP54 dust, sweat, and water resistance.',
                'image_url': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Bose QuietComfort 45 Active Noise-Cancelling Headphones - Triple Black',
                'slug': 'bose-quietcomfort-45-triple-black',
                'description': 'Renowned Bose acoustic noise cancelling and lightweight comfort architecture. Plush synthetic leather earcups replaced with new OEM cushions. 24-hour battery playback verified.',
                'category_id': cat_aud,
                'seller_id': seller_ananya,
                'original_price': 29900.00,
                'refurbished_price': 16500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 96,
                'tested_points': 28,
                'carbon_saved_kg': 16.5,
                'specifications': 'TriPort acoustic architecture; Quiet and Aware modes; 24-hour battery life on a single charge; USB-C quick charge (15 min = 3 hours); Adjustable EQ via Bose Music app; Glass-filled nylon headband.',
                'image_url': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Marshall Stanmore III Wireless Bluetooth Speaker - Vintage Black & Brass',
                'slug': 'marshall-stanmore-iii-vintage-black',
                'description': 'Room-filling stereo soundstage with outward-angled tweeters and updated waveguides. Iconic vintage Marshall vinyl finish and brass script logo. Perfect for hostel rooms and student hangouts.',
                'category_id': cat_aud,
                'seller_id': seller_vikram,
                'original_price': 37999.00,
                'refurbished_price': 22900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 100,
                'tested_points': 26,
                'carbon_saved_kg': 24.0,
                'specifications': '80W Class D amplification; 1x 50W woofer + 2x 15W tweeters; Bluetooth 5.2 with LE Audio readiness; 3.5mm Aux & RCA inputs; Dynamic Loudness tonal balance; PVC-free vegan leather housing.',
                'image_url': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },

            # --- TABLETS & IPADS ---
            {
                'title': 'Apple iPad Air 5th Gen 64GB Wi-Fi - Starlight (Apple Pencil 2 Ready)',
                'slug': 'apple-ipad-air-m1-64gb-starlight',
                'description': 'M1-powered iPad Air. Liquid Retina anti-reflective display inspected under magnification with zero dead pixels. Magnetic induction charger for Apple Pencil 2 fully tested. Ideal for lecture notes and sketching.',
                'category_id': cat_tab,
                'seller_id': seller_aryan,
                'original_price': 54900.00,
                'refurbished_price': 34500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 95,
                'tested_points': 30,
                'carbon_saved_kg': 29.0,
                'specifications': 'Apple M1 chip (8-Core CPU / 8-Core GPU); 64GB Storage; 10.9" Liquid Retina TrueTone display; Touch ID in power button; USB-C port; 12MP Ultra-Wide front camera with Center Stage.',
                'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Apple iPad Pro 12.9" 6th Gen (M2, 128GB, Liquid Retina XDR Mini-LED) - Space Gray',
                'slug': 'apple-ipad-pro-12-9-m2-128gb',
                'description': 'Top-of-the-line iPad Pro featuring the 10,000 Mini-LED Liquid Retina XDR display with 1,000,000:1 contrast ratio. Apple Pencil hover functionality verified. Perfect for architecture, design, and UI prototyping.',
                'category_id': cat_tab,
                'seller_id': seller_vikram,
                'original_price': 112900.00,
                'refurbished_price': 76500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 96,
                'tested_points': 36,
                'carbon_saved_kg': 38.0,
                'specifications': 'Apple M2 (8-Core CPU / 10-Core GPU / 16-Core Neural Engine); 128GB Storage; 12.9" Mini-LED Liquid Retina XDR (120Hz ProMotion, 1600 nits HDR peak); Face ID; Thunderbolt / USB 4 port; 4-speaker audio.',
                'image_url': 'https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Samsung Galaxy Tab S9 128GB Wi-Fi with S-Pen Included - Graphite',
                'slug': 'samsung-galaxy-tab-s9-128gb-graphite',
                'description': 'Premium Android tablet with 11-inch Dynamic AMOLED 2X 120Hz display and IP68 water & dust resistance. Includes original low-latency magnetic S-Pen stylus. Samsung DeX desktop mode tested on external monitors.',
                'category_id': cat_tab,
                'seller_id': seller_ananya,
                'original_price': 72999.00,
                'refurbished_price': 44900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 97,
                'tested_points': 32,
                'carbon_saved_kg': 31.5,
                'specifications': 'Snapdragon 8 Gen 2 for Galaxy; 8GB RAM; 128GB Storage (MicroSD expandable up to 1TB); 11.0" Dynamic AMOLED 2X 120Hz; IP68 Water/Dust resistant; Quad speakers tuned by AKG with Dolby Atmos; 8400mAh battery.',
                'image_url': 'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Apple iPad Mini 6th Gen 64GB Wi-Fi - Purple (Ultra-portable Companion)',
                'slug': 'apple-ipad-mini-6-64gb-purple',
                'description': 'Pocket-sized powerhouse with 8.3-inch Liquid Retina display and A15 Bionic chip. Lightweight 293g body makes it ideal for textbook reading, quick note taking, and campus commuting.',
                'category_id': cat_tab,
                'seller_id': seller_priya,
                'original_price': 49900.00,
                'refurbished_price': 31900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 93,
                'tested_points': 30,
                'carbon_saved_kg': 22.0,
                'specifications': 'Apple A15 Bionic; 64GB Storage; 8.3" Liquid Retina TrueTone Display (500 nits); Touch ID in top button; Apple Pencil 2 support; USB-C fast charging; Landscape stereo speakers.',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },

            # --- WEARABLES & SMARTWATCHES ---
            {
                'title': 'Apple Watch Series 8 (GPS, 45mm) - Midnight Aluminum Case',
                'slug': 'apple-watch-series-8-45mm-midnight',
                'description': 'Certified refurbished smartwatch with Always-On Retina display. ECG, Blood Oxygen, and Wrist Temperature sensing sensors calibrated. Includes sanitized original sport band plus extra braided loop.',
                'category_id': cat_wear,
                'seller_id': seller_aryan,
                'original_price': 41900.00,
                'refurbished_price': 21990.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 93,
                'tested_points': 26,
                'carbon_saved_kg': 14.5,
                'specifications': '45mm Case Size; Apple S8 SiP dual-core; Always-On LTPO OLED display (1000 nits); ECG app, Blood Oxygen, and Temperature sensor; Crash Detection & Fall Detection; 50m water resistance (WR50).',
                'image_url': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Apple Watch Ultra (GPS + Cellular, 49mm) Titanium Case with Orange Alpine Loop',
                'slug': 'apple-watch-ultra-49mm-titanium',
                'description': 'Rugged aerospace-grade titanium smartwatch with flat sapphire front crystal. Precision dual-frequency GPS (L1 and L5) and 86-decibel emergency siren verified. 36 hours normal battery life.',
                'category_id': cat_wear,
                'seller_id': seller_vikram,
                'original_price': 89900.00,
                'refurbished_price': 52900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 98,
                'tested_points': 34,
                'carbon_saved_kg': 21.0,
                'specifications': '49mm Aerospace Titanium Case; Up to 2000 nits Always-On Retina display; Dual-frequency GPS; Water resistant 100m & EN13319 dive certified; Depth gauge with water temperature sensor; 86dB siren.',
                'image_url': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Samsung Galaxy Watch 6 Classic 47mm Bluetooth - Silver (Physical Rotating Bezel)',
                'slug': 'samsung-galaxy-watch-6-classic-47mm-silver',
                'description': 'Refurbished Galaxy Watch 6 Classic with tactile rotating bezel and Sapphire Crystal glass. Advanced sleep coaching, body composition BIA sensor, and blood pressure monitoring calibrated.',
                'category_id': cat_wear,
                'seller_id': seller_ananya,
                'original_price': 36999.00,
                'refurbished_price': 19900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 95,
                'tested_points': 28,
                'carbon_saved_kg': 13.0,
                'specifications': '47mm Stainless Steel Case with Physical Rotating Bezel; 1.5" Super AMOLED Sapphire Crystal (2000 nits); Exynos W930 Dual-Core 1.4GHz; 2GB RAM + 16GB Storage; BioActive Sensor (ECG, BIA, HR); IP68 / 5ATM.',
                'image_url': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Garmin Forerunner 265 GPS Running & Fitness Smartwatch - Aqua & Black',
                'slug': 'garmin-forerunner-265-aqua',
                'description': 'Dedicated athletic training smartwatch with bright 1.3" AMOLED touchscreen and morning report training readiness metrics. Up to 13 days of battery life in smartwatch mode.',
                'category_id': cat_wear,
                'seller_id': seller_priya,
                'original_price': 50490.00,
                'refurbished_price': 28900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 99,
                'tested_points': 28,
                'carbon_saved_kg': 15.0,
                'specifications': '1.3" AMOLED Touchscreen + 5-button interface; Multi-band GNSS with SatIQ technology; Wrist-based running dynamics and power; Up to 13 days battery life (20 hours in GPS mode); Music storage (Spotify/Amazon Music).',
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },

            # --- PC COMPONENTS & GAMING ---
            {
                'title': 'NVIDIA GeForce RTX 3070 8GB GDDR6 (Founders Edition - Thermal Repasted)',
                'slug': 'nvidia-rtx-3070-8gb-founders-edition',
                'description': 'Refurbished graphics card cleaned of dust and repasted with Arctic MX-6 high-performance thermal compound. FurMark 1-hour stress test stabilized under 67°C. Excellent for deep learning, AI vision, and 1440p gaming.',
                'category_id': cat_gam,
                'seller_id': seller_vikram,
                'original_price': 54000.00,
                'refurbished_price': 26500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 100,
                'tested_points': 26,
                'carbon_saved_kg': 42.0,
                'specifications': 'Ampere Architecture (5888 CUDA Cores); 8GB GDDR6 256-bit VRAM; Boost Clock 1725 MHz; HDMI 2.1 & 3x DisplayPort 1.4a; 220W TDP (650W PSU recommended); Founders Edition dual-axial flow cooler.',
                'image_url': 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Sony PlayStation 5 Digital Edition Refurbished with DualSense Controller & 825GB SSD',
                'slug': 'sony-ps5-digital-edition-refurbished',
                'description': 'Factory refurbished PS5 console with sanitized white faceplates and calibrated DualSense wireless controller with adaptive triggers and haptic feedback. Clean HDMI 2.1 port capable of 4K 120Hz output.',
                'category_id': cat_gam,
                'seller_id': seller_aryan,
                'original_price': 44990.00,
                'refurbished_price': 29900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 100,
                'tested_points': 30,
                'carbon_saved_kg': 48.0,
                'specifications': 'Custom AMD Zen 2 (8-Core 3.5GHz) & RDNA 2 GPU (10.28 TFLOPs); 16GB GDDR6; 825GB High-Speed SSD (5.5GB/s raw); Tempest 3D AudioTech; 4K 120Hz & 8K HDR support; 1x DualSense controller included.',
                'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&auto=format&fit=crop&q=80',
                'is_featured': True
            },
            {
                'title': 'Steam Deck OLED 512GB Handheld Gaming Console with Anti-Glare Glass',
                'slug': 'steam-deck-oled-512gb-handheld',
                'description': 'Valve Steam Deck OLED with vibrant 7.4-inch 90Hz HDR OLED screen and upgraded 50Wh battery. Thumbsticks tested for zero drift. Comes with official Valve hardshell carrying case and 45W USB-C charger.',
                'category_id': cat_gam,
                'seller_id': seller_vikram,
                'original_price': 58000.00,
                'refurbished_price': 38900.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 1,
                'status': 'available',
                'battery_health': 98,
                'tested_points': 32,
                'carbon_saved_kg': 26.0,
                'specifications': 'AMD 6nm APU (Zen 2 4c/8t + 8 RDNA 2 CUs); 16GB LPDDR5 RAM; 512GB NVMe SSD; 7.4" 1280x800 HDR OLED 90Hz (1000 nits peak); Wi-Fi 6E; 50Wh battery (3-12 hours gameplay); Official Case & 45W Charger.',
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            },
            {
                'title': 'Keychron Q1 Pro Wireless Custom Mechanical Keyboard (Full Aluminum CNC, Gateron Red)',
                'slug': 'keychron-q1-pro-wireless-custom-keyboard',
                'description': 'Full CNC anodized aluminum 75% mechanical keyboard with double-gasket acoustic mounting. Hot-swappable switches lubricated with Krytox 205g0. Programmable via QMK/VIA on Mac & Windows.',
                'category_id': cat_gam,
                'seller_id': seller_priya,
                'original_price': 19999.00,
                'refurbished_price': 10500.00,
                'condition_grade': 'Grade A - Pristine',
                'warranty_months': 6,
                'stock_quantity': 2,
                'status': 'available',
                'battery_health': 100,
                'tested_points': 24,
                'carbon_saved_kg': 15.0,
                'specifications': '75% Layout (81 Keys); 6063 CNC Machined Aluminum Body; Double-Gasket Sound Dampening; Hot-Swappable Gateron Jupiter Red linear switches; Bluetooth 5.1 & Type-C Wired; 4000mAh Battery (300 hours typing); QMK/VIA support.',
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
                'is_featured': False
            }
        ]

        saved_products = []
        for p_data in products_list:
            prod = Product(**p_data)
            db.session.add(prod)
            saved_products.append(prod)
        db.session.commit()
        print(f"  ✅ Seeded {len(saved_products)} Classy Refurbished Products across 6 categories")

        # ---------------------------------------------------------------------
        # 5. DEVICE DIAGNOSTIC CHECKPOINTS (32-Point Testing Standard)
        # ---------------------------------------------------------------------
        print("  🔬 Seeding certified 32-point diagnostic checkpoints for all devices...")
        diagnostic_templates = [
            ('Display & Panel', 'Pixel Uniformity & Sub-Pixel Integrity', 'Passed', 'Zero dead/stuck pixels under microscopic inspection'),
            ('Display & Panel', 'True Tone & OLED Luminance Calibration', 'Passed', 'Delta-E < 1.4 across 100% color gamut'),
            ('Battery & Power', 'Charge Retention & Internal Resistance', 'Passed', 'Cycle degradation curve within OEM nominal limit'),
            ('Battery & Power', 'Power IC & Surge Protection Test', 'Passed', 'Verified 0.00V leakage on standby'),
            ('Thermal & CPU', '15-Minute Full Load Stress Benchmark', 'Passed', 'Thermal dissipation stable below 68°C with zero throttling'),
            ('Ports & Connectivity', 'Thunderbolt / USB-C Pin Continuity', 'Passed', 'Full 40Gbps bidirectional transfer tested'),
            ('Audio & Mic', 'Harmonic Acoustic Distortion (THD)', 'Passed', 'THD < 0.2% across 20Hz - 20,000Hz sweep'),
            ('Security & Biometrics', 'Face ID / Touch ID Enclave Test', 'Passed', 'Hardware cryptographic handshake verified')
        ]

        for p in saved_products:
            # Seed 4-6 diagnostics for each product
            for cat, test_name, res, notes in diagnostic_templates[:5]:
                diag = DeviceDiagnostic(
                    product_id=p.id,
                    category=cat,
                    test_name=test_name,
                    result=res,
                    notes=notes
                )
                db.session.add(diag)
        db.session.commit()
        print("  ✅ Seeded 120+ Diagnostic Lab Test Checkpoints")

        # ---------------------------------------------------------------------
        # 6. VERIFIED STUDENT REVIEWS
        # ---------------------------------------------------------------------
        reviews_data = [
            (saved_products[0].id, user_objs['rohit_student'].id, 5, 'Indistinguishable from brand new!', 'Picked this MacBook Air M1 up at the DTU campus library. Battery capacity is 96%, zero dents or scratches, and the seller Aryan handed over the certified warranty slip on the spot. Great initiative for student budgets!'),
            (saved_products[0].id, user_objs['neha_cs'].id, 5, 'Flawless for Computer Science lab work', 'Compiled our React Native & Python machine learning assignments smoothly. Screen TrueTone is gorgeous and battery lasts easily 14 hours.'),
            (saved_products[1].id, user_objs['rohit_student'].id, 5, 'Pro workstation at 35% off retail', 'The Liquid Retina XDR screen is unbelievable. Inspected thermals before making payment at the quad. Aryan is a certified refurbisher, completely legit.'),
            (saved_products[2].id, user_objs['neha_cs'].id, 5, 'Best keyboard for coding ever made', 'The ThinkPad X1 keyboard is unmatched for typing code late at night. Clean Windows 11 installation with zero bloatware.'),
            (saved_products[6].id, user_objs['rohit_student'].id, 5, 'Dynamic Island and cameras are mint', 'iPhone 14 Pro in Deep Purple with battery at 94%. Saved almost ₹57,000 compared to new. 6-Month ReVive replacement warranty gives total peace of mind.'),
            (saved_products[7].id, user_objs['neha_cs'].id, 5, 'Titanium finish feels ultra premium', 'Natural Titanium is so light in hand. USB-C transfer to my laptop is lightning fast. Best deal on campus.'),
            (saved_products[8].id, user_objs['rohit_student'].id, 5, 'S-Pen makes digital notes effortless', 'Galaxy S23 Ultra camera zoom is insane for taking photos of blackboard slides from the back row in large lecture halls!'),
            (saved_products[12].id, user_objs['neha_cs'].id, 5, 'Library study sessions are silent now', 'Sony XM4 noise cancellation is pure magic. Earcups were completely sanitized and fresh with replacement memory foam.'),
            (saved_products[13].id, user_objs['rohit_student'].id, 5, 'Original Apple audio quality guaranteed', 'AirPods Pro 2 with USB-C case. Seller tested Bluetooth sync with me before accepting payment.')
        ]

        for pid, uid, rating, title, comment in reviews_data:
            rev = Review(
                product_id=pid,
                user_id=uid,
                rating=rating,
                title=title,
                comment=comment,
                verified_purchase=True
            )
            db.session.add(rev)
        db.session.commit()
        print(f"  ✅ Seeded {len(reviews_data)} Verified Student Reviews with 5-Star Ratings")

        # ---------------------------------------------------------------------
        # 7. ORDERS & WARRANTY CERTIFICATES
        # ---------------------------------------------------------------------
        orders_data = [
            {
                'order_number': 'RV-A891F2C4',
                'buyer_id': user_objs['rohit_student'].id,
                'product_id': saved_products[0].id,
                'seller_id': saved_products[0].seller_id,
                'total_amount': 48990.00,
                'status': 'delivered',
                'shipping_name': 'Rohit Verma',
                'shipping_address': 'Hostel Block B, Room 304, Campus Quad',
                'shipping_city': 'New Delhi',
                'shipping_phone': '+91 91234 56780',
                'payment_method': 'UPI / Card on Campus Handover',
                'delivery_timeslot': 'Central Library Quad (1:00 PM - 2:00 PM)',
                'warranty_code': 'WAR-RV-A891F2C4-2026'
            },
            {
                'order_number': 'RV-E47209B1',
                'buyer_id': user_objs['neha_cs'].id,
                'product_id': saved_products[12].id,
                'seller_id': saved_products[12].seller_id,
                'total_amount': 14990.00,
                'status': 'confirmed',
                'shipping_name': 'Neha Gupta',
                'shipping_address': 'Girls Hostel 2, Tech Campus Quad',
                'shipping_city': 'New Delhi',
                'shipping_phone': '+91 98451 23456',
                'payment_method': 'UPI / Card on Campus Handover',
                'delivery_timeslot': 'Tech Block Cafeteria (4:30 PM - 5:30 PM)',
                'warranty_code': 'WAR-RV-E47209B1-2026'
            }
        ]

        for o in orders_data:
            order_obj = Order(**o)
            db.session.add(order_obj)
        db.session.commit()
        print(f"  ✅ Seeded {len(orders_data)} Campus Orders with Digital Warranty Certificates")

        # ---------------------------------------------------------------------
        # 8. MAKE AN OFFER NEGOTIATIONS
        # ---------------------------------------------------------------------
        offers_data = [
            {
                'product_id': saved_products[0].id,
                'buyer_id': user_objs['rohit_student'].id,
                'seller_id': saved_products[0].seller_id,
                'offer_amount': 46500.00,
                'original_price': float(saved_products[0].refurbished_price),
                'message': 'Hey Aryan, 2nd year CS student here! Would you accept ₹46,500? I can meet at the library quad for inspection today itself.',
                'status': 'accepted'
            },
            {
                'product_id': saved_products[6].id,
                'buyer_id': user_objs['neha_cs'].id,
                'seller_id': saved_products[6].seller_id,
                'offer_amount': 59000.00,
                'original_price': float(saved_products[6].refurbished_price),
                'message': 'Hi! I am interested in the iPhone 14 Pro Deep Purple. Would you be willing to do ₹59,000 with campus handover?',
                'status': 'pending'
            }
        ]

        for off in offers_data:
            offer_obj = Offer(**off)
            db.session.add(offer_obj)
        db.session.commit()
        print(f"  ✅ Seeded {len(offers_data)} Student Offers")

        print("✨ Database successfully seeded with rich, classy certified refurbished tech catalog!")

if __name__ == '__main__':
    seed_database()
