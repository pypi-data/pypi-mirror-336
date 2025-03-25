import os
import sys
from datetime import datetime
from loguru import logger
import logging
import inspect
"""
#更新日志:2024-7-9 12:12:38
# loguru是一个Python的第三方日志库，它提供了简单易用的API来记录日志。
# logger.add("my_log_file.log")  # 将日志输出到文件
# logger.info("这是一条信息日志")
# logger.warning("这是一条警告日志")
# logger.error("这是一条错误日志")
# logger.critical("这是一条严重错误日志")
# logger.debug("这是一条调试日志")
# logger.success("操作成功")
"""

class Log_Info:
    def __init__(self, local_ip=None,local_port=None,local_window=None,debug=False):
        # 日志前置信息
        self.local_ip=local_ip
        self.local_port=local_port
        self.local_window=local_window
        self.debug=debug
        if not local_ip:
            self.local_ip="127.0.0.1" #本机ip
        if not local_port:
            self.local_port="5901" #本机端口
        if not local_window:
            self.local_window="001" #本机窗口

    def log_init(self):
        # 指定日志文件的路径, 默认放在桌面
        log_folder = r"C:/Users/Administrator/Desktop/log"

        # 获取当前日期并格式化为 YYYY-MM-DD
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_folder, f"{self.local_window}_{current_date}.log")

        # 确保日志文件夹存在
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        if not self.debug:
            # 移除所有默认的日志处理器
            logger.remove()

        # 添加一个日志处理器，指定编码为 UTF-8
        logger.add(log_file, level="DEBUG", format="{time} {level} {module}:{line} - {message}",
                   rotation="1 day", retention="10 days", enqueue=True, encoding="utf-8")

        # 在日志记录开始时写入指定内容
        self.safe_log("========== facility information ==========")
        self.safe_log(f"Local IP: {self.local_ip}")
        self.safe_log(f"Local Port: {self.local_port}")
        self.safe_log(f"Local Window: {self.local_window}")
        self.safe_log("========== Log session started ==========")

    def safe_log(self, message):
        """安全地记录日志，处理编码问题"""
        try:
            # 直接记录消息
            logger.debug(message)
        except UnicodeEncodeError:
            # 如果遇到编码错误，进行处理
            safe_message = message.encode('gbk', 'replace').decode('gbk')
            logger.debug(safe_message)

class ColoredFormatter(logging.Formatter):
    """自定义格式化器，带有颜色支持"""
    # 定义颜色
    COLORS = {
        'DEBUG': "\033[0;37m",  # 白色
        'INFO': "\033[0;32m",   # 绿色
        'WARNING': "\033[0;33m", # 黄色
        'ERROR': "\033[0;31m",   # 红色
        'CRITICAL': "\033[1;31m", # 高亮红色
    }
    RESET = "\033[0m"  # 重置颜色
    def format(self, record):
        # 获取日志级别的颜色
        color = self.COLORS.get(record.levelname, self.RESET)
        # 生成带颜色的日志消息
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

class ColoredLogger:
    """带有颜色输出的自定义日志记录器"""
    def __init__(self, name='ColoredLogger', level=logging.DEBUG):
        """初始化 ColoredLogger
        :param name: 日志记录器名称
        :param level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        # 创建自定义格式化器，包含行号
        formatter = ColoredFormatter('%(lineno)d - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        # 将处理器添加到记录器
        self.logger.addHandler(console_handler)
    def debug(self, message):
        """记录调试信息"""
        try:
            self.logger.debug(message, stacklevel=2)
        except Exception as e:
            print(f"Error in ColoredLogger.debug: {e}")
    def info(self, message):
        """记录普通信息"""
        try:
            self.logger.info(message, stacklevel=2)
        except Exception as e:
            print(f"Error in ColoredLogger.info: {e}")

    def warning(self, message):
        """记录警告信息"""
        try:
            self.logger.warning(message, stacklevel=2)
        except Exception as e:
            print(f"Error in ColoredLogger.warning: {e}")

    def error(self, message):
        """记录错误信息"""
        try:
            self.logger.error(message, stacklevel=2)
        except Exception as e:
            print(f"Error in ColoredLogger.error: {e}")

    def critical(self, message):
        """记录严重错误信息"""
        try:
            self.logger.critical(message, stacklevel=2)
        except Exception as e:
            print(f"Error in ColoredLogger.critical: {e}")

# # 示例用法
# if __name__ == "__main__":
#     colored_logger = ColoredLogger()
#     # 记录不同级别的日志消息
#     colored_logger.debug("这是一个调试信息")
#     colored_logger.info("这是一个信息")
#     colored_logger.warning("这是一个警告信息")
#     colored_logger.error("这是一个错误信息")
#     colored_logger.critical("这是一个严重错误信息")