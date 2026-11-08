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

def setup_mysql_from_schema():
    print(f"Connecting to MySQL ({USER}@{HOST}:{PORT})...")
    try:
        conn = pymysql.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            charset='utf8mb4',
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
        )
    except Exception as e:
        print(f"❌ Failed to connect to MySQL: {e}")
        print("Please ensure MySQL is running and password is correct in backend/.env")
        return False

    schema_file = os.path.join(BASE_DIR, 'schema.sql')
    if not os.path.exists(schema_file):
        print(f"❌ schema.sql not found at {schema_file}")
        return False

    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    print(f"Executing schema.sql into MySQL...")
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
        conn.commit()
        print("✅ Tables created in MySQL successfully!")
        conn.close()

        # Run seed.py using MySQL
        print("Seeding sample data into MySQL...")
        from seed import seed_database
        seed_database()
        print("🎉 All 6 tables seeded in MySQL successfully!")
        return True
    except Exception as e:
        print(f"❌ Error executing schema: {e}")
        return False

if __name__ == '__main__':
    setup_mysql_from_schema()

