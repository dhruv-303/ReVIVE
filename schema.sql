-- ============================================================================
-- ReVive - Refurbished Marketplace Database Schema
-- Author: ReVive Team (College Startup Project)
-- Database: MySQL 8.0+
-- Compatible with: MySQL Workbench, phpMyAdmin, CLI
-- ============================================================================

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS revive_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE revive_db;

-- Disable foreign key checks during drop to allow clean re-runs
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS device_diagnostics;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------------
-- 1. USERS TABLE
-- Stores buyers, student sellers, and admins
-- ----------------------------------------------------------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(30) NULL,
    role ENUM('buyer', 'seller', 'admin') DEFAULT 'buyer',
    subscription_plan VARCHAR(50) DEFAULT 'Student Starter',
    subscription_status VARCHAR(30) DEFAULT 'active',
    avatar_url VARCHAR(255) NULL,
    college_name VARCHAR(150) DEFAULT 'Campus University',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 2. CATEGORIES TABLE
-- Electronics categories for refurbished tech
-- ----------------------------------------------------------------------------
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    slug VARCHAR(80) NOT NULL UNIQUE,
    description VARCHAR(255) NULL,
    icon VARCHAR(50) DEFAULT 'laptop',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 3. PRODUCTS TABLE
-- Refurbished device listings with condition grades, verification and warranty
-- ----------------------------------------------------------------------------
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(220) NOT NULL,
    description TEXT NOT NULL,
    category_id INT NOT NULL,
    seller_id INT NOT NULL,
    original_price DECIMAL(10, 2) NOT NULL,
    refurbished_price DECIMAL(10, 2) NOT NULL,
    condition_grade ENUM('Grade A - Pristine', 'Grade B - Very Good', 'Grade C - Good') NOT NULL DEFAULT 'Grade A - Pristine',
    warranty_months INT DEFAULT 6,
    stock_quantity INT DEFAULT 1,
    status ENUM('available', 'reserved', 'sold') DEFAULT 'available',
    battery_health INT DEFAULT 92,
    tested_points INT DEFAULT 32,
    carbon_saved_kg DECIMAL(6, 2) DEFAULT 45.00,
    specifications TEXT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
    CONSTRAINT fk_products_seller FOREIGN KEY (seller_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_products_category (category_id),
    INDEX idx_products_seller (seller_id),
    INDEX idx_products_status (status),
    INDEX idx_products_price (refurbished_price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 4. ORDERS TABLE
-- Completed purchases by buyers
-- ----------------------------------------------------------------------------
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    seller_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'confirmed',
    shipping_name VARCHAR(120) NOT NULL,
    shipping_address TEXT NOT NULL,
    shipping_city VARCHAR(80) NOT NULL,
    shipping_phone VARCHAR(30) NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'Cash / UPI on Delivery',
    delivery_timeslot VARCHAR(100) DEFAULT 'Campus Quad (12 PM - 2 PM)',
    warranty_code VARCHAR(60) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_buyer FOREIGN KEY (buyer_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_product FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_seller FOREIGN KEY (seller_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_orders_buyer (buyer_id),
    INDEX idx_orders_seller (seller_id),
    INDEX idx_orders_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 5. OFFERS TABLE
-- "Make an Offer" price negotiation between buyer and seller
-- ----------------------------------------------------------------------------
CREATE TABLE offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    offer_amount DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2) NOT NULL,
    message TEXT NULL,
    status ENUM('pending', 'accepted', 'rejected', 'countered') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_offers_product FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
    CONSTRAINT fk_offers_buyer FOREIGN KEY (buyer_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_offers_seller FOREIGN KEY (seller_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_offers_product (product_id),
    INDEX idx_offers_buyer (buyer_id),
    INDEX idx_offers_seller (seller_id),
    INDEX idx_offers_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 6. SUBSCRIPTIONS TABLE
-- Seller tiers: Student Starter, Campus Pro, Master Refurbisher
-- ----------------------------------------------------------------------------
CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_name VARCHAR(60) NOT NULL,
    price_monthly DECIMAL(8, 2) NOT NULL,
    billing_cycle VARCHAR(20) DEFAULT 'monthly',
    max_listings INT DEFAULT 5,
    commission_rate DECIMAL(4, 2) DEFAULT 8.00,
    status ENUM('active', 'cancelled', 'expired') DEFAULT 'active',
    features TEXT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NULL,
    CONSTRAINT fk_subscriptions_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_subscriptions_user (user_id),
    INDEX idx_subscriptions_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 7. REVIEWS TABLE
-- Verified campus student ratings & feedback
-- ----------------------------------------------------------------------------
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL DEFAULT 5,
    title VARCHAR(150) NOT NULL,
    comment TEXT NOT NULL,
    verified_purchase BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reviews_product FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_reviews_product (product_id),
    INDEX idx_reviews_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- 8. DEVICE DIAGNOSTICS TABLE
-- 32-point certified laboratory inspection checkpoints
-- ----------------------------------------------------------------------------
CREATE TABLE device_diagnostics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    result VARCHAR(30) DEFAULT 'Passed',
    notes VARCHAR(255) NULL,
    CONSTRAINT fk_diagnostics_product FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
    INDEX idx_diagnostics_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

