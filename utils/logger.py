import os
from datetime import datetime


class Logger:
    def __init__(self):
        self.log_dir = "outputs/logs"
        os.makedirs(self.log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"log_{timestamp}.txt")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"

        print(log_msg)

        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")