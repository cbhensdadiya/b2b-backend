-- B2B Marketplace Database Schema
-- PostgreSQL 14+
-- This is a reference schema. Use Alembic migrations for actual database setup.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Role Enum
CREATE TYPE user_role AS ENUM ('MasterAdmin', 'Buyer');

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mobile VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'Buyer',
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Indexes for Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_mobile ON users(mobile);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);

-- OTP Table
CREATE TABLE otps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mobile VARCHAR(20) NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for OTP
CREATE INDEX idx_otps_mobile ON otps(mobile);
CREATE INDEX idx_otps_created_at ON otps(created_at);

-- Categories Table
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Categories
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_is_active ON categories(is_active);

-- Subcategories Table
CREATE TABLE subcategories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Subcategories
CREATE INDEX idx_subcategories_category_id ON subcategories(category_id);
CREATE INDEX idx_subcategories_slug ON subcategories(slug);
CREATE INDEX idx_subcategories_is_active ON subcategories(is_active);

-- Audit Logs Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID,
    changes JSONB,
    ip_address VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Audit Logs
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subcategories_updated_at BEFORE UPDATE ON subcategories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert Master Admin (password: cp@512A hashed with BCrypt cost factor 12)
-- Note: Run seed_admin.py instead for proper password hashing
INSERT INTO users (name, email, mobile, password_hash, role, is_verified, is_active)
VALUES (
    'Master Admin',
    'cbhensdadiya@sofvare.com',
    '0000000000',
    '$2b$12$placeholder_hash_run_seed_admin_py',
    'MasterAdmin',
    TRUE,
    TRUE
);

-- Sample Categories
INSERT INTO categories (name, slug, description, is_active) VALUES
('Electronics', 'electronics', 'Electronic components and devices', TRUE),
('Raw Materials', 'raw-materials', 'Industrial raw materials', TRUE),
('Machinery', 'machinery', 'Industrial machinery and equipment', TRUE),
('Chemicals', 'chemicals', 'Industrial chemicals', TRUE),
('Textiles', 'textiles', 'Textile materials and fabrics', TRUE);

-- Sample Subcategories for Electronics
INSERT INTO subcategories (category_id, name, slug, description, is_active)
SELECT id, 'Semiconductors', 'semiconductors', 'Semiconductor components', TRUE
FROM categories WHERE slug = 'electronics';

INSERT INTO subcategories (category_id, name, slug, description, is_active)
SELECT id, 'Circuit Boards', 'circuit-boards', 'PCB and circuit boards', TRUE
FROM categories WHERE slug = 'electronics';

INSERT INTO subcategories (category_id, name, slug, description, is_active)
SELECT id, 'Sensors', 'sensors', 'Electronic sensors', TRUE
FROM categories WHERE slug = 'electronics';

-- Comments
COMMENT ON TABLE users IS 'User accounts for buyers and admins';
COMMENT ON TABLE otps IS 'One-time passwords for mobile verification';
COMMENT ON TABLE categories IS 'Product categories';
COMMENT ON TABLE subcategories IS 'Product subcategories';
COMMENT ON TABLE audit_logs IS 'Audit trail for user actions';

COMMENT ON COLUMN users.password_hash IS 'BCrypt hashed password with cost factor 12';
COMMENT ON COLUMN users.deleted_at IS 'Soft delete timestamp';
COMMENT ON COLUMN otps.expires_at IS 'OTP expiration timestamp';
