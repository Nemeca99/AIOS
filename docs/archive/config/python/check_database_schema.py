"""
Check database schema to fix column names
"""
import sqlite3

def check_database_schema():
    db_path = "F:/AI_Datasets/AIOS_Database/database/conversations.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("📊 DATABASE TABLES:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check messages table structure
        if any('messages' in str(table) for table in tables):
            cursor.execute("PRAGMA table_info(messages)")
            columns = cursor.fetchall()
            print(f"\n📋 MESSAGES TABLE COLUMNS:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        # Sample some data
        try:
            cursor.execute("SELECT * FROM messages LIMIT 3")
            rows = cursor.fetchall()
            print(f"\n📝 SAMPLE DATA ({len(rows)} rows):")
            for i, row in enumerate(rows):
                print(f"  Row {i+1}: {row}")
        except Exception as e:
            print(f"❌ Sample data error: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database_schema()
