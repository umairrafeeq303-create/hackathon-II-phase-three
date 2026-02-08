#!/usr/bin/env python3
"""
Test database connectivity to Neon PostgreSQL
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in environment")
    sys.exit(1)

print(f"Testing connection to: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'}")
print("-" * 60)

try:
    # Attempt to connect
    print("🔄 Attempting to connect...")
    conn = psycopg2.connect(DATABASE_URL)

    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print("✅ SUCCESS: Connected to database!")
    print(f"📊 PostgreSQL version: {db_version[0][:50]}...")

    cursor.close()
    conn.close()

except psycopg2.OperationalError as e:
    print(f"❌ OPERATIONAL ERROR: {e}")
    print("\nPossible causes:")
    print("  1. Network connectivity issues")
    print("  2. Incorrect DATABASE_URL")
    print("  3. Database server is down")
    print("  4. Firewall blocking connection")
    sys.exit(1)

except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
    sys.exit(1)
