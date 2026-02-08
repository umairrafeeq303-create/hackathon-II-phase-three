"""
Database connection test script for production deployment.
Tests PostgreSQL connection before starting the application.
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError


def test_database_connection():
    """
    Test database connection and validate configuration.
    Returns True if connection successful, False otherwise.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        return False

    # Mask password in logs for security
    safe_url = database_url
    if "@" in database_url:
        parts = database_url.split("@")
        if ":" in parts[0]:
            user_pass = parts[0].split("://")[1]
            if ":" in user_pass:
                user = user_pass.split(":")[0]
                safe_url = database_url.replace(user_pass, f"{user}:****")

    print("=" * 70)
    print("🔍 DATABASE CONNECTION TEST")
    print("=" * 70)
    print(f"Database URL: {safe_url}")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'unknown')}")
    print("=" * 70)

    try:
        # Create engine with timeout
        engine = create_engine(
            database_url,
            pool_pre_ping=True,  # Test connections before using
            pool_recycle=3600,   # Recycle connections after 1 hour
            connect_args={
                "connect_timeout": 10,
                "options": "-c statement_timeout=10000"
            } if database_url.startswith("postgresql") else {}
        )

        # Test connection
        print("Attempting to connect to database...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful!")

            # Get database info
            if database_url.startswith("postgresql"):
                try:
                    version_result = connection.execute(text("SELECT version()"))
                    version = version_result.fetchone()[0]
                    print(f"📊 PostgreSQL version: {version.split(',')[0]}")
                except Exception as e:
                    print(f"⚠️  Could not get version: {e}")

            print("=" * 70)
            return True

    except OperationalError as e:
        print("=" * 70)
        print("❌ DATABASE CONNECTION FAILED")
        print("=" * 70)
        print(f"Error type: OperationalError")
        print(f"Error message: {str(e)}")
        print("=" * 70)
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("1. Check DATABASE_URL is correct in Railway environment variables")
        print("2. Ensure DATABASE_URL includes ?sslmode=require for Neon")
        print("3. Verify Neon database is active and accessible")
        print("4. Check network connectivity from Railway to Neon")
        print("5. Ensure connection string format: postgresql://user:pass@host/db")
        print("=" * 70)
        return False

    except SQLAlchemyError as e:
        print("=" * 70)
        print("❌ DATABASE ERROR")
        print("=" * 70)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("=" * 70)
        return False

    except Exception as e:
        print("=" * 70)
        print("❌ UNEXPECTED ERROR")
        print("=" * 70)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("=" * 70)
        return False

    finally:
        if 'engine' in locals():
            engine.dispose()


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
