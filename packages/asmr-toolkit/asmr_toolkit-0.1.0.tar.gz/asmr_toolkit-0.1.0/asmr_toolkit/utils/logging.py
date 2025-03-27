import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

# 创建控制台实例
console = Console()

# 日志级别映射
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def setup_logging(level: str = "info", show_path: bool = False) -> logging.Logger:
    """
    设置日志系统

    参数:
        level: 日志级别 (debug, info, warning, error, critical)
        show_path: 是否显示文件路径

    返回:
        配置好的日志器实例
    """
    log_level = LOG_LEVELS.get(level.lower(), logging.INFO)

    # 配置Rich处理器
    rich_handler = RichHandler(
        console=console,
        show_path=show_path,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        omit_repeated_times=False,
    )

    # 配置日志格式
    format_str = "%(message)s"
    if show_path:
        format_str = "%(pathname)s:%(lineno)d - %(message)s"

    logging.basicConfig(
        level=log_level,
        format=format_str,
        datefmt="[%X]",
        handlers=[rich_handler],
    )

    # 获取根日志器
    logger = logging.getLogger("asmr_toolkit")
    logger.setLevel(log_level)

    # 确保不会传播到父日志器
    logger.propagate = False

    return logger


# 创建默认日志器
logger = setup_logging()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取命名日志器

    参数:
        name: 日志器名称，如果为None则返回根日志器

    返回:
        日志器实例
    """
    if name:
        return logging.getLogger(f"asmr_toolkit.{name}")
    return logger
