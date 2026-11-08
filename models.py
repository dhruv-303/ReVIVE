from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# -----------------------------------------------------------------------------
# 1. USER MODEL
# -----------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    role = db.Column(db.String(20), default='buyer')  # 'buyer', 'seller', 'admin'
    subscription_plan = db.Column(db.String(50), default='Student Starter')
    subscription_status = db.Column(db.String(30), default='active')
    avatar_url = db.Column(db.String(255), nullable=True)
    college_name = db.Column(db.String(150), default='Campus University')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    products_listed = db.relationship('Product', backref='seller', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='Product.seller_id')
    orders_placed = db.relationship('Order', backref='buyer', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='Order.buyer_id')
    orders_sold = db.relationship('Order', backref='seller', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='Order.seller_id')
    offers_made = db.relationship('Offer', backref='buyer', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='Offer.buyer_id')
    offers_received = db.relationship('Offer', backref='seller', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='Offer.seller_id')
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone or '',
            'role': self.role,
            'subscription_plan': self.subscription_plan,
            'subscription_status': self.subscription_status,
            'avatar_url': self.avatar_url or f"https://api.dicebear.com/7.x/identicon/svg?seed={self.username}",
            'college_name': self.college_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# -----------------------------------------------------------------------------
# 2. CATEGORY MODEL
# -----------------------------------------------------------------------------
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(50), default='laptop')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description or '',
            'icon': self.icon,
            'products_count': self.products.count()
        }


# -----------------------------------------------------------------------------
# 3. PRODUCT MODEL
# -----------------------------------------------------------------------------
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    original_price = db.Column(db.Numeric(10, 2), nullable=False)
    refurbished_price = db.Column(db.Numeric(10, 2), nullable=False)
    condition_grade = db.Column(db.String(50), nullable=False, default='Grade A - Pristine')
    warranty_months = db.Column(db.Integer, default=6)
    stock_quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(30), default='available', index=True)  # 'available', 'reserved', 'sold'
    battery_health = db.Column(db.Integer, default=92)
    tested_points = db.Column(db.Integer, default=32)
    carbon_saved_kg = db.Column(db.Numeric(6, 2), default=45.5)  # E-waste sustainability metric
    specifications = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    offers = db.relationship('Offer', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    diagnostics = db.relationship('DeviceDiagnostic', backref='product', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_details=True):
        discount_percent = 0
        if self.original_price and self.original_price > 0:
            discount_percent = round(((float(self.original_price) - float(self.refurbished_price)) / float(self.original_price)) * 100)

        # Average rating
        reviews_list = self.reviews.all()
        avg_rating = round(sum(r.rating for r in reviews_list) / len(reviews_list), 1) if reviews_list else 4.9

        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else '',
            'seller_id': self.seller_id,
            'seller_name': self.seller.full_name if self.seller else 'Verified Student Refurbisher',
            'seller_college': self.seller.college_name if self.seller else 'Campus',
            'original_price': float(self.original_price),
            'refurbished_price': float(self.refurbished_price),
            'discount_percent': max(0, discount_percent),
            'condition_grade': self.condition_grade,
            'warranty_months': self.warranty_months,
            'stock_quantity': self.stock_quantity,
            'status': self.status,
            'battery_health': self.battery_health,
            'tested_points': self.tested_points,
            'carbon_saved_kg': float(self.carbon_saved_kg) if self.carbon_saved_kg else 45.0,
            'specifications': self.specifications or '',
            'image_url': self.image_url,
            'is_featured': self.is_featured,
            'avg_rating': avg_rating,
            'reviews_count': len(reviews_list),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_details:
            data['reviews'] = [r.to_dict() for r in reviews_list]
            data['diagnostics'] = [d.to_dict() for d in self.diagnostics.all()]

        return data


# -----------------------------------------------------------------------------
# 4. ORDER MODEL
# -----------------------------------------------------------------------------
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(30), default='confirmed', index=True)  # 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'
    shipping_name = db.Column(db.String(120), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(80), nullable=False)
    shipping_phone = db.Column(db.String(30), nullable=False)
    payment_method = db.Column(db.String(50), default='UPI / Card on Campus Handover')
    delivery_timeslot = db.Column(db.String(100), default='Library Quad (12 PM - 2 PM)')
    warranty_code = db.Column(db.String(60), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.full_name if self.buyer else '',
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else 'Refurbished Device',
            'product_image': self.product.image_url if self.product else '',
            'condition_grade': self.product.condition_grade if self.product else 'Grade A',
            'warranty_months': self.product.warranty_months if self.product else 6,
            'seller_id': self.seller_id,
            'seller_name': self.seller.full_name if self.seller else '',
            'seller_college': self.seller.college_name if self.seller else 'Campus',
            'total_amount': float(self.total_amount),
            'status': self.status,
            'shipping_name': self.shipping_name,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_phone': self.shipping_phone,
            'payment_method': self.payment_method,
            'delivery_timeslot': self.delivery_timeslot or 'Standard Campus Handover',
            'warranty_code': self.warranty_code or f"WAR-{self.order_number}",
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# -----------------------------------------------------------------------------
# 5. OFFER MODEL ("Make an Offer" Feature)
# -----------------------------------------------------------------------------
class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    offer_amount = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='pending', index=True)  # 'pending', 'accepted', 'rejected', 'countered'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else 'Product',
            'product_image': self.product.image_url if self.product else '',
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.full_name if self.buyer else 'Buyer',
            'seller_id': self.seller_id,
            'seller_name': self.seller.full_name if self.seller else 'Seller',
            'offer_amount': float(self.offer_amount),
            'original_price': float(self.original_price),
            'message': self.message or '',
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# -----------------------------------------------------------------------------
# 6. SUBSCRIPTION MODEL (Seller Subscription Plans)
# -----------------------------------------------------------------------------
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    plan_name = db.Column(db.String(60), nullable=False)  # 'Student Starter', 'Campus Pro', 'Master Refurbisher'
    price_monthly = db.Column(db.Numeric(8, 2), nullable=False)
    billing_cycle = db.Column(db.String(20), default='monthly')
    max_listings = db.Column(db.Integer, default=5)
    commission_rate = db.Column(db.Numeric(4, 2), default=8.00)
    status = db.Column(db.String(30), default='active', index=True)
    features = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'price_monthly': float(self.price_monthly),
            'billing_cycle': self.billing_cycle,
            'max_listings': self.max_listings,
            'commission_rate': float(self.commission_rate),
            'status': self.status,
            'features': self.features or '',
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }


# -----------------------------------------------------------------------------
# 7. PRODUCT REVIEWS TABLE (Campus Verified Feedback)
# -----------------------------------------------------------------------------
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False, default=5)
    title = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    verified_purchase = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'author_name': self.author.full_name if self.author else 'Campus Student',
            'author_college': self.author.college_name if self.author else 'University',
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'verified_purchase': self.verified_purchase,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# -----------------------------------------------------------------------------
# 8. DEVICE DIAGNOSTICS TABLE (32-Point Certified Testing Checkpoints)
# -----------------------------------------------------------------------------
class DeviceDiagnostic(db.Model):
    __tablename__ = 'device_diagnostics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)  # 'Display', 'Battery', 'Thermal & CPU', 'Ports', 'Audio'
    test_name = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(30), default='Passed')
    notes = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'category': self.category,
            'test_name': self.test_name,
            'result': self.result,
            'notes': self.notes or 'Within OEM nominal tolerances'
        }
