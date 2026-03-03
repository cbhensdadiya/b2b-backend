"""
Check if firebase_uid column exists in users table
"""
from sqlalchemy import inspect
from app.core.database import engine

def check_firebase_uid_column():
    """Check if firebase_uid column exists"""
    inspector = inspect(engine)
    columns = inspector.get_columns('users')
    
    column_names = [col['name'] for col in columns]
    
    print("\n" + "="*60)
    print("USERS TABLE COLUMNS")
    print("="*60)
    
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
    
    print("="*60)
    
    if 'firebase_uid' in column_names:
        print("✅ firebase_uid column EXISTS")
        print("="*60)
        return True
    else:
        print("❌ firebase_uid column MISSING")
        print("\nYou need to run the migration:")
        print("  alembic upgrade head")
        print("="*60)
        return False

if __name__ == "__main__":
    try:
        exists = check_firebase_uid_column()
        exit(0 if exists else 1)
    except Exception as e:
        print(f"\n❌ Error checking database: {e}")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. Database exists")
        print("  3. .env file has correct DATABASE_URL")
        exit(1)
