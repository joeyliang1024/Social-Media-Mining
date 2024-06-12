import os
import sqlite3

def get_sqlite_files(base_dir):
    """遍歷base_dir，並返回所有名為data.sqlite的文件路徑"""
    sqlite_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "datas.sqlite":
                sqlite_files.append(os.path.join(root, file))
    return sqlite_files

def merge_sqlite_files(base_dir, output_file):
    """將多個SQLite資料庫合併到一個資料庫中"""
    sqlite_files = get_sqlite_files(base_dir)
    if not sqlite_files:
        print("未找到任何data.sqlite文件")
        return

    # 創建輸出資料庫
    output_conn = sqlite3.connect(output_file)
    output_cursor = output_conn.cursor()

    for file in sqlite_files:
        print(f"正在合併 {file}")

        input_conn = sqlite3.connect(file)
        input_cursor = input_conn.cursor()

        # 獲取所有表
        input_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = input_cursor.fetchall()

        for table_name in tables:
            table_name = table_name[0]
            print(f"正在處理表 {table_name}")
            # 獲取表結構
            input_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = input_cursor.fetchall()
            column_names = [col[1] for col in columns]

            # 創建表結構（如果表尚不存在）
            column_definitions = ", ".join([f"{col[1]} {col[2]}" for col in columns])
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
            output_cursor.execute(create_table_sql)

            # 複製數據
            input_cursor.execute(f"SELECT * FROM {table_name}")
            rows = input_cursor.fetchall()
            print(f"正在複製 {len(rows)} 行數據")
            placeholders = ", ".join(["?" for _ in column_names])
            insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
            output_cursor.executemany(insert_sql, rows)

        input_conn.close()

    output_conn.commit()
    output_conn.close()
    print(f"所有資料庫已成功合併到 {output_file}")

# 設置基本目錄和輸出文件
base_dir = "../"
output_file = "merged_data.sqlite"

merge_sqlite_files(base_dir, output_file)
