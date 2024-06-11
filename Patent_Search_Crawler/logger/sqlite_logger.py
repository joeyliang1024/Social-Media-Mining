import sqlite3
import os
from logger.base import BaseLogger

row_name = [
        "公告號",
        "公告日",
        "公報卷期",
        "證書號",
        "申請號",
        "申請日",
        "公報IPC",
        "當前IPC",
        "申請人",
        "當前專利權人",
        "發明人",
        "代理人",
        "當前代理人",
        "摘要",
    ]

class SQLiteLogger(BaseLogger):
    def __init__(self, log_dir):
        super().__init__(log_dir)
        self.log_file = os.path.join(log_dir, "datas.sqlite")
        self.conn = None
        self.cursor = None

    def init_logger(self, header_list):
        if self.conn is None:
            self.conn = sqlite3.connect(self.log_file)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS log ({', '.join(header_list)})"
            )
            self.conn.commit()

    def log(self, log_dict):
        for key in row_name:
            if key not in log_dict:
                log_dict[key] = ""
                
        self.cursor.execute(
            f"INSERT INTO log VALUES ({', '.join(['?']*len(log_dict))})",
            list(log_dict.values()),
        )
        self.conn.commit()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __exit__(self, *args):
        self.close()
