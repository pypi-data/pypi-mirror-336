import logging
from unittest.mock import patch

from asmr_toolkit.utils.logging import get_logger, setup_logging


def test_get_logger():
    """测试获取日志器"""
    # 测试获取默认日志器
    logger = get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "asmr_toolkit"

    # 测试获取带名称的日志器
    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "asmr_toolkit.test"

    # 测试获取嵌套名称的日志器
    logger = get_logger("parent.child")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "asmr_toolkit.parent.child"


def test_setup_logging():
    """测试日志设置"""
    # 测试默认设置
    logger = setup_logging()
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO

    # 测试不同日志级别
    logger = setup_logging(level="debug")
    assert logger.level == logging.DEBUG

    logger = setup_logging(level="warning")
    assert logger.level == logging.WARNING

    # 测试显示路径选项
    with patch("asmr_toolkit.utils.logging.RichHandler") as mock_handler:
        logger = setup_logging(show_path=True)
        mock_handler.assert_called_once()
        args, kwargs = mock_handler.call_args
        assert kwargs["show_path"] is True
