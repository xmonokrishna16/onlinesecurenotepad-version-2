import mysql.connector

try:
    db = mysql.connector.connect(
        host="mysql-23f354fd-onlinesecurenotepad.c.aivencloud.com",
        user="avnadmin",
        password="AVNS_yQOc54viMK_trd4vLEz",
        database="defaultdb",
        port=21951
    )
    cursor = db.cursor()
    
    # Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password TEXT
        )
    """)
    
    # Create Notes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            content TEXT
        )
    """)
    
    db.commit()
    print("Success! Tables created in Aiven.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'db' in locals(): db.close()