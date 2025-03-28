import logging
import logging.config
import logging.handlers
import queue
import socket
import sys
from .whisper_db import WhisperDB

# 创建日志队列
log_queue = queue.Queue(-1)

# 自定义 MySQL 处理器
class MySQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.server_name = socket.gethostname()

    def emit(self, record):
        try:
            log_entry = self.format(record)  # 确保格式化日志

            # 短连接模式，避免连接超时
            db = WhisperDB()
            connection = db.connection
            cursor = connection.cursor()

            sql = """INSERT INTO openai_logs 
                     (server_name, level, message, logger_name, filename, line_no) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (self.server_name, record.levelname, log_entry, record.name, record.pathname, record.lineno)
            
            cursor.execute(sql, data)
            connection.commit()
        except Exception as e:
            print(f"MySQL logging error: {e}", file=sys.stderr)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

# 定义日志配置
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s [%(name)s - %(filename)s:%(lineno)d]",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "queue": {
            "()": logging.handlers.QueueHandler,
            "queue": log_queue
        },
    },
    "loggers": {
        "whisper_ai": {
            "level": "INFO",
            "handlers": ["console", "queue"],
            "propagate": False,
        }
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

    mysql_handler = MySQLHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s [%(name)s - %(filename)s:%(lineno)d]"
    )
    mysql_handler.setFormatter(formatter)

    listener = logging.handlers.QueueListener(log_queue, mysql_handler, respect_handler_level=True)
    listener.start()

    print("Logging system initialized")  # 方便调试
