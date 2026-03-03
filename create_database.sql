-- B2B Marketplace - Database Creation Script
-- Run this script to create the database

-- Connect to PostgreSQL as postgres user:
-- psql -U postgres -f create_database.sql

-- Check if database exists and drop if needed (optional)
-- DROP DATABASE IF EXISTS b2b_marketplace;

-- Create database
CREATE DATABASE b2b_marketplace
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Connect to the new database
\c b2b_marketplace

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Display success message
\echo ''
\echo '============================================================'
\echo 'Database "b2b_marketplace" created successfully!'
\echo '============================================================'
\echo ''
\echo 'Next steps:'
\echo '1. Update .env file with database credentials'
\echo '2. Run: alembic upgrade head'
\echo '3. Run: python seed_admin.py'
\echo ''
