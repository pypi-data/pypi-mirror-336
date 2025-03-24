import logging
import sys
import os
from loguru import logger as loguru_logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys.exc_info()[2], 2
        while frame and frame.tb_frame.f_code.co_filename == logging.__file__:
            frame = frame.tb_next
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # 确保日志目录存在
    os.makedirs("logs", exist_ok=True)
    
    # 移除所有现有的处理器
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 配置 loguru
    loguru_logger.remove()  # 移除默认的 sink
    
    # 添加控制台输出
    loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}",
        level="INFO",
        enqueue=True
    )
    
    # 添加文件输出 - 普通日志（每小时切割）
    loguru_logger.add(
        "logs/app_{time:YYYY-MM-DD_HH}.log",
        rotation="1h",  # 每小时轮换
        retention="30 days",  # 保留30天
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        enqueue=True
    )
    
    # 添加文件输出 - 错误日志（每小时切割）
    loguru_logger.add(
        "logs/error_{time:YYYY-MM-DD_HH}.log",
        rotation="1h",  # 每小时轮换
        retention="30 days",  # 保留30天
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        enqueue=True
    )

    # 配置拦截器
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


# 在模块导入时立即设置日志
setup_logging()
