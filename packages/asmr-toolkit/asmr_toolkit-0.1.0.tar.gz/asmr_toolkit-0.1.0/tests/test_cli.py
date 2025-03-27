from unittest.mock import patch

import pytest
from click.testing import CliRunner

from asmr_toolkit.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_main_help(runner):
    """测试主命令帮助信息显示正确"""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ASMR Toolkit - 音频处理工具集" in result.output


def test_version_option(runner):
    """测试版本选项正常工作"""
    from asmr_toolkit import __version__

    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


@patch("asmr_toolkit.cli.setup_logging")
def test_log_level_option(mock_setup_logging, runner):
    """测试日志级别选项"""
    result = runner.invoke(main, ["--log-level", "debug", "convert", "--help"])
    assert result.exit_code == 0
    # 验证setup_logging被调用
    mock_setup_logging.assert_called_once()
    args, kwargs = mock_setup_logging.call_args
    assert kwargs.get("level") == "debug" or "debug" in args


@patch("asmr_toolkit.cli.setup_logging")
def test_show_paths_option(mock_setup_logging, runner):
    """测试显示路径选项"""
    result = runner.invoke(main, ["--show-paths", "convert", "--help"])
    assert result.exit_code == 0
    # 验证setup_logging被调用
    mock_setup_logging.assert_called_once()
    args, kwargs = mock_setup_logging.call_args
    assert kwargs.get("show_path") is True or True in args
