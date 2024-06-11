import os
import csv
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

class CsvLogger(BaseLogger):
    def __init__(self, log_dir):
        super().__init__(log_dir)
        self.log_file = os.path.join(log_dir, "datas.csv")
        self.writer = None

    def init_logger(self, header_list):
        if self.writer is None:
            self.writer = csv.DictWriter(
                open(self.log_file, "w", encoding="UTF-8"), fieldnames=header_list
            )
            self.writer.writeheader()

    def log(self, log_dict):
        for key in row_name:
            if key not in log_dict:
                log_dict[key] = ""
        self.writer.writerow(log_dict)

    def close(self):
        if self.writer is not None:
            self.writer = None

    def __exit__(self, *args):
        self.close()
