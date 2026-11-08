import os
import sys
import pymysql
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

HOST = os.environ.get('MYSQL_HOST', 'localhost')
PORT = int(os.environ.get('MYSQL_PORT', 3306))
USER = os.environ.get('MYSQL_USER', 'root')
PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
DB_NAME = os.environ.get('MYSQL_DB', 'revive_db')

def test_mysql_connection():
    print("=" * 60)
    print("  ReVive MySQL Database Connection Diagnostic Tool")
    print("=" * 60)
    print(f"Target Host    : {HOST}")
    print(f"Target Port    : {PORT}")
    print(f"Target User    : {USER}")
    print(f"Target Database: {DB_NAME}")
    print("-" * 60)

    # 1. Attempt basic TCP / Socket connection to MySQL server
    try:
        conn = pymysql.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            charset='utf8mb4',
            connect_timeout=3
        )
        print("✅ [STEP 1/3] Successfully connected to MySQL server!")
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print(f"   MySQL Server Version: {version[0]}")

            # 2. Check if revive_db exists or create it
            cursor.execute("SHOW DATABASES LIKE %s;", (DB_NAME,))
            db_exists = cursor.fetchone()
            
            if not db_exists:
                print(f"⚠️  [STEP 2/3] Database '{DB_NAME}' does not exist yet. Creating it now...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                print(f"✅ [STEP 2/3] Created database '{DB_NAME}' successfully!")
            else:
                print(f"✅ [STEP 2/3] Database '{DB_NAME}' already exists.")

        conn.select_db(DB_NAME)

        # 3. Check existing tables in revive_db
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"✅ [STEP 3/3] Tables found in '{DB_NAME}': {len(tables)}")
            for t in tables:
                cursor.execute(f"SELECT COUNT(*) FROM `{t}`;")
                count = cursor.fetchone()[0]
                print(f"   • {t:<15} ({count} rows)")

        conn.close()
        print("-" * 60)
        print("🎉 SUCCESS: Your backend can talk directly to MySQL!")
        print("=" * 60)
        return True

    except pymysql.err.OperationalError as e:
        print("❌ CONNECTION FAILED:")
        error_code, error_msg = e.args[0], e.args[1]
        print(f"   Error Code   : {error_code}")
        print(f"   Error Message: {error_msg}")
        print("-" * 60)
        if error_code == 2003:
            print("👉 DIAGNOSIS: MySQL server is not running on port 3306.")
            print("   SOLUTION:")
            print("   1. Open MySQL Workbench, XAMPP, or Windows Services.")
            print("   2. Start the MySQL service (or click 'Start' next to MySQL in XAMPP).")
            print("   3. Re-run: python test_mysql.py")
        elif error_code == 1045:
            print("👉 DIAGNOSIS: Access denied / Incorrect password.")
            print("   SOLUTION:")
            print("   1. Open 'backend/.env' in VS Code or Notepad.")
            print("   2. Update 'MYSQL_PASSWORD=your_password' with your real MySQL password.")
            print("   3. Re-run: python test_mysql.py")
        print("=" * 60)
        return False

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == '__main__':
    test_mysql_connection()

