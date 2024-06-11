class BaseLogger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.writer = None

    def log(self, log_dict, step):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
