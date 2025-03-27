import sys

import click
from rich.console import Console

from asmr_toolkit.utils.logging import logger, setup_logging
from asmr_toolkit.commands.convert import convert

console = Console()


@click.group()
@click.version_option(package_name="asmr_toolkit")
@click.option(
    "--log-level",
    type=click.Choice(
        ["debug", "info", "warning", "error", "critical"], case_sensitive=False
    ),
    default="info",
    help="设置日志级别",
)
@click.option(
    "--show-paths",
    is_flag=True,
    help="在日志中显示文件路径",
)
def main(log_level, show_paths):
    """ASMR Toolkit - 音频处理工具集"""
    # 设置日志级别
    setup_logging(level=log_level, show_path=show_paths)
    logger.debug("ASMR Toolkit 启动")


# 注册子命令
main.add_command(convert)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"程序执行过程中发生错误: {e}")
        sys.exit(1)
