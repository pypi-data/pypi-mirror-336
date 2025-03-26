# logging_config.py
import logging
import logging.config
import logging.handlers
import queue
import socket
from .whisper_db import WhisperDB

# 自定义 MySQL 处理器
class MySQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.server_name = socket.gethostname()

    def emit(self, record):
        """向数据库插入日志信息"""
        try:
            log_entry = self.format(record)

            # 使用短连接模式，防止长时间持有数据库连接
            db = WhisperDB()  # 假设 WhisperDB 管理连接
            connection = db.connection  # 获取数据库连接
            cursor = connection.cursor()

            sql = """INSERT INTO openai_logs 
                     (server_name, level, message, logger_name, filename, line_no) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (self.server_name, record.levelname, log_entry, record.name, record.pathname, record.lineno)
            
            cursor.execute(sql, data)
            connection.commit()
        except Exception as e:
            # 打印错误并写入 stderr，以便发现问题
            print(f"MySQL logging error: {e}")
        finally:
            # 确保关闭 cursor
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def close(self):
        """无须显式关闭数据库连接，emit 中已处理"""
        super().close()

# 创建日志队列
log_queue = queue.Queue(-1)  # 无界队列
queue_handler = logging.handlers.QueueHandler(log_queue)

# 配置日志
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
        "mysql": {
            "()": MySQLHandler,
            "level": "INFO",
            "formatter": "default",  # 格式化日志消息
        },
        "queue": {
            "()": logging.handlers.QueueHandler,
            "queue": log_queue,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "queue"],
    },
}

def setup_logging():
    # 获取当前机器的主机名
    logging.config.dictConfig(LOGGING_CONFIG)  # 配置日志系统
    mysql_handler = MySQLHandler()  # 创建自定义的 MySQL 处理器
    listener = logging.handlers.QueueListener(log_queue, mysql_handler, respect_handler_level=True)
    listener.start()  # 启动队列监听器
