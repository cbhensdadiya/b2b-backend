# B2B Marketplace Backend API

A production-ready RESTful API built with FastAPI and PostgreSQL for the B2B Marketplace platform.

## 🚀 Features

- **FastAPI Framework**: Modern, fast, and async Python web framework
- **PostgreSQL Database**: Robust relational database with SQLAlchemy ORM
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Master Admin, Buyer roles
- **OTP Verification**: Mobile number verification with OTP
- **Password Hashing**: BCrypt with cost factor 12
- **Database Migrations**: Alembic for schema management
- **CORS Enabled**: Cross-origin resource sharing for Angular frontend
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Global exception handling
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## 📋 API Endpoints

### Authentication
- `POST /api/buyer/auth/signup` - Buyer registration
- `POST /api/buyer/auth/login` - Buyer login
- `POST /api/buyer/auth/verify-otp` - Verify mobile OTP
- `POST /api/buyer/auth/resend-otp` - Resend OTP
- `POST /api/buyer/auth/refresh` - Refresh access token
- `GET /api/buyer/auth/me` - Get current buyer info

### Master Admin - Buyers
- `GET /api/admin/buyers` - List all buyers (paginated)
- `GET /api/admin/buyers/{id}` - Get buyer details
- `PUT /api/admin/buyers/{id}` - Update buyer
- `DELETE /api/admin/buyers/{id}` - Soft delete buyer

### Master Admin - Categories
- `GET /api/admin/categories` - List all categories
- `POST /api/admin/categories` - Create category
- `PUT /api/admin/categories/{id}` - Update category
- `DELETE /api/admin/categories/{id}` - Delete category

### Master Admin - Subcategories
- `GET /api/admin/subcategories` - List all subcategories
- `POST /api/admin/subcategories` - Create subcategory
- `PUT /api/admin/subcategories/{id}` - Update subcategory
- `DELETE /api/admin/subcategories/{id}` - Delete subcategory

### Public
- `GET /api/categories` - Get all active categories
- `GET /api/categories/{id}/subcategories` - Get subcategories

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: BCrypt (passlib)
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **OTP**: PyOTP
- **SMS**: Twilio (optional)
- **ASGI Server**: Uvicorn

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 14 or higher
- pip

### Setup

1. **Clone and navigate to backend**
```bash
cd b2b-backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your settings
```

5. **Create PostgreSQL database**
```sql
CREATE DATABASE b2b_marketplace;
```

6. **Run database migrations**
```bash
alembic upgrade head
```

7. **Seed master admin**
```bash
python seed_admin.py
```

8. **Start development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure

```
b2b-backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py           # Authentication endpoints
│   │   │   │   ├── buyers.py         # Buyer management
│   │   │   │   ├── categories.py     # Category management
│   │   │   │   └── public.py         # Public endpoints
│   │   │   └── api.py                # API router
│   │   └── deps.py                   # Dependencies (auth, db)
│   ├── core/
│   │   ├── config.py                 # Configuration
│   │   ├── security.py               # JWT, password hashing
│   │   └── database.py               # Database connection
│   ├── models/
│   │   ├── user.py                   # User model
│   │   ├── category.py               # Category model
│   │   ├── otp.py                    # OTP model
│   │   └── audit.py                  # Audit log model
│   ├── schemas/
│   │   ├── auth.py                   # Auth schemas
│   │   ├── buyer.py                  # Buyer schemas
│   │   ├── category.py               # Category schemas
│   │   └── common.py                 # Common schemas
│   ├── services/
│   │   ├── auth_service.py           # Authentication logic
│   │   ├── otp_service.py            # OTP generation/verification
│   │   ├── sms_service.py            # SMS sending
│   │   └── email_service.py          # Email sending
│   ├── utils/
│   │   ├── helpers.py                # Helper functions
│   │   └── exceptions.py             # Custom exceptions
│   └── main.py                       # FastAPI application
├── alembic/
│   ├── versions/                     # Migration files
│   └── env.py                        # Alembic config
├── tests/                            # Test files
├── .env.example                      # Example environment variables
├── .gitignore                        # Git ignore file
├── alembic.ini                       # Alembic configuration
├── requirements.txt                  # Python dependencies
├── seed_admin.py                     # Seed master admin
└── README.md                         # This file
```

## 🔐 Authentication Flow

### Buyer Signup
1. Buyer submits signup form (name, email, mobile, password)
2. System validates input
3. System hashes password (BCrypt, cost factor 12)
4. System creates buyer record (isVerified=false)
5. System generates 6-digit OTP
6. System sends OTP via SMS
7. System returns success message

### OTP Verification
1. Buyer submits mobile and OTP
2. System validates OTP (not expired, matches)
3. System marks buyer as verified
4. System returns success message

### Buyer Login
1. Buyer submits email and password
2. System validates credentials
3. System checks if verified
4. System generates JWT token
5. System returns token and buyer data

## 🗄️ Database Schema

### Users Table
- id (UUID, PK)
- name (VARCHAR)
- email (VARCHAR, UNIQUE)
- mobile (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- role (ENUM: 'MasterAdmin', 'Buyer')
- is_verified (BOOLEAN)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- deleted_at (TIMESTAMP, nullable)

### OTP Table
- id (UUID, PK)
- mobile (VARCHAR)
- otp_code (VARCHAR)
- expires_at (TIMESTAMP)
- is_used (BOOLEAN)
- created_at (TIMESTAMP)

### Categories Table
- id (UUID, PK)
- name (VARCHAR, UNIQUE)
- slug (VARCHAR, UNIQUE)
- description (TEXT)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Subcategories Table
- id (UUID, PK)
- category_id (UUID, FK)
- name (VARCHAR)
- slug (VARCHAR)
- description (TEXT)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Audit Logs Table
- id (UUID, PK)
- user_id (UUID, FK)
- action (VARCHAR)
- entity_type (VARCHAR)
- entity_id (UUID)
- changes (JSONB)
- ip_address (VARCHAR)
- created_at (TIMESTAMP)

## 🧪 Testing

### Run tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=app tests/
```

## 📚 API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Configuration

### Environment Variables

Key configurations in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/b2b_marketplace

# JWT
SECRET_KEY=your-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:4200

# Master Admin
MASTER_ADMIN_EMAIL=cbhensdadiya@sofvare.com
MASTER_ADMIN_PASSWORD=cp@512A
```

## 🚀 Deployment

### Using Docker

```bash
# Build image
docker build -t b2b-backend .

# Run container
docker run -p 8000:8000 --env-file .env b2b-backend
```

### Using Docker Compose

```bash
docker-compose up -d
```

### Manual Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Run migrations: `alembic upgrade head`
4. Seed admin: `python seed_admin.py`
5. Start server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## 🔒 Security Features

- Password hashing with BCrypt (cost factor 12)
- JWT token-based authentication
- Token expiration and refresh
- Role-based access control
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Rate limiting (optional)
- Request logging

## 📊 Master Admin Credentials

**Email**: cbhensdadiya@sofvare.com  
**Password**: cp@512A

⚠️ **Important**: Change these credentials in production!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Built with ❤️ using FastAPI and PostgreSQL**
