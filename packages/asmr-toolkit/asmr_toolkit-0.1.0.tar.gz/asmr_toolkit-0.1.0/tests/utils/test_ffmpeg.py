from unittest.mock import MagicMock, patch

from asmr_toolkit.utils.ffmpeg import run_ffmpeg, check_ffmpeg


@patch("subprocess.Popen")
def test_check_ffmpeg_success(mock_popen):
    """测试FFmpeg检查成功的情况"""
    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"ffmpeg version 4.2.2", b"")
    mock_popen.return_value = process_mock

    # 执行检查
    result = check_ffmpeg()

    # 验证结果
    assert result is True
    mock_popen.assert_called_once()


@patch("subprocess.Popen")
def test_check_ffmpeg_failure(mock_popen):
    """测试FFmpeg检查失败的情况"""
    # 设置模拟子进程运行结果为失败
    mock_popen.side_effect = FileNotFoundError("No such file or directory")

    # 执行检查
    result = check_ffmpeg()

    # 验证结果
    assert result is False
    mock_popen.assert_called_once()


@patch("subprocess.Popen")
def test_run_ffmpeg_success(mock_popen):
    """测试FFmpeg运行成功的情况"""
    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"", b"")
    mock_popen.return_value = process_mock

    # 执行FFmpeg命令
    result = run_ffmpeg("input.mp3", "output.opus.ogg")

    # 验证结果
    assert result is True
    mock_popen.assert_called_once()


@patch("subprocess.Popen")
def test_run_ffmpeg_failure(mock_popen):
    """测试FFmpeg运行失败的情况"""
    # 设置模拟子进程运行结果为失败
    process_mock = MagicMock()
    process_mock.returncode = 1
    process_mock.communicate.return_value = (b"", b"error")
    mock_popen.return_value = process_mock

    # 执行FFmpeg命令
    result = run_ffmpeg("input.mp3", "output.opus.ogg")

    # 验证结果
    assert result is False
    mock_popen.assert_called_once()


@patch("subprocess.Popen")
def test_run_ffmpeg_with_options(mock_popen):
    """测试带选项的FFmpeg命令"""
    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"", b"")
    mock_popen.return_value = process_mock

    # 执行FFmpeg命令
    options = {"vbr": "on", "compression_level": "10"}
    result = run_ffmpeg("input.mp3", "output.opus.ogg", options=options)

    # 验证结果
    assert result is True
    mock_popen.assert_called_once()
    # 验证选项被正确添加到命令中
    args, kwargs = mock_popen.call_args
    cmd = args[0]
    assert "-vbr" in cmd
    assert "on" in cmd
    assert "-compression_level" in cmd
    assert "10" in cmd
