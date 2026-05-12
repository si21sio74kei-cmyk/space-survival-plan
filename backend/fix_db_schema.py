import sqlite3
import os

db_path = "survival_system.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查表结构
    cursor.execute("PRAGMA table_info(survival_status)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print("Current columns in survival_status table:")
    for col in columns:
        print(f"  - {col}")
    
    # 检查缺少的列
    required_columns = ['co2_level', 'humidity', 'pressure', 'backup_power_hours', 'crew_count', 'protein_level', 'water_reserve', 'medical_temp']
    missing_columns = [col for col in required_columns if col not in columns]
    
    if missing_columns:
        print(f"\nMissing columns: {missing_columns}")
        print("\nAdding missing columns...")
        
        # 添加缺少的列
        for col in missing_columns:
            if col == 'co2_level':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT 0.04")
            elif col == 'humidity':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT 45.0")
            elif col == 'pressure':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT 101.3")
            elif col == 'backup_power_hours':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT 48.0")
            elif col == 'crew_count':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} INTEGER DEFAULT 4")
            elif col == 'protein_level':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT 100.0")
            elif col == 'water_reserve':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT 100.0")
            elif col == 'medical_temp':
                cursor.execute(f"ALTER TABLE survival_status ADD COLUMN {col} FLOAT DEFAULT -70.0")
            print(f"  Added column: {col}")
        
        conn.commit()
        print("\nDatabase schema updated successfully!")
    else:
        print("\nAll required columns exist.")
    
    conn.close()
else:
    print(f"Database file '{db_path}' not found.")
