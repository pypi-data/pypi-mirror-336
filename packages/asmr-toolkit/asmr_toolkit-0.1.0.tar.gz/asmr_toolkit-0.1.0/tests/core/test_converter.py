import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from asmr_toolkit.core.converter import AudioConverter

EXPECTED_FILE_COUNT = 2
EXPECTED_CALL_COUNT = 2


@pytest.fixture
def sample_audio_file():
    """创建一个临时的模拟音频文件"""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
        # 写入一些假数据
        temp.write(b"fake audio data")
        temp_path = temp.name

    yield temp_path

    # 测试后清理
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@patch("subprocess.Popen")
def test_convert_file(mock_popen, sample_audio_file):
    """测试文件转换功能"""
    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"", b"")
    mock_popen.return_value = process_mock

    # 创建转换器
    converter = AudioConverter(bitrate="128k")

    # 执行转换
    output_file = converter.convert_file(sample_audio_file)

    # 验证结果
    assert output_file is not None
    assert output_file.endswith(".opus.ogg")
    mock_popen.assert_called_once()
    # 验证调用FFmpeg的命令包含正确的参数
    args, kwargs = mock_popen.call_args
    cmd = args[0]
    assert "ffmpeg" in cmd[0] or "ffmpeg" == cmd[0]
    assert "-i" in cmd
    assert sample_audio_file in cmd
    assert "-c:a" in cmd
    assert "libopus" in cmd
    assert "-b:a" in cmd
    assert "128k" in cmd


@patch("subprocess.Popen")
def test_convert_file_with_custom_output(mock_popen, sample_audio_file):
    """测试指定输出文件的转换"""
    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"", b"")
    mock_popen.return_value = process_mock

    # 创建转换器
    converter = AudioConverter(bitrate="128k")

    # 创建临时输出路径
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "output.opus.ogg")

        # 执行转换
        result = converter.convert_file(sample_audio_file, output_path)

        # 验证结果
        assert result == output_path
        mock_popen.assert_called_once()
        # 验证输出文件路径正确传递给FFmpeg
        args, kwargs = mock_popen.call_args
        cmd = args[0]
        assert output_path in cmd


@patch("subprocess.Popen")
def test_convert_file_error(mock_popen, sample_audio_file):
    """测试转换失败的情况"""
    # 设置模拟子进程运行结果为失败
    process_mock = MagicMock()
    process_mock.returncode = 1
    process_mock.communicate.return_value = (b"", b"error output")
    mock_popen.return_value = process_mock

    # 创建转换器
    converter = AudioConverter(bitrate="128k")

    # 执行转换
    result = converter.convert_file(sample_audio_file)

    # 验证结果
    assert result is None  # 失败时应返回None


@patch("subprocess.Popen")
def test_convert_batch(mock_popen, tmp_path):
    """测试批量转换功能"""
    # 创建测试文件
    file1 = tmp_path / "file1.mp3"
    file2 = tmp_path / "file2.mp3"
    file1.write_bytes(b"fake audio data")
    file2.write_bytes(b"fake audio data")

    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"", b"")
    mock_popen.return_value = process_mock

    # 创建转换器
    converter = AudioConverter(bitrate="128k")

    # 执行批量转换
    results = converter.convert_batch([str(file1), str(file2)])

    # 验证结果
    assert len(results) == EXPECTED_FILE_COUNT
    assert all(result[1] is not None for result in results)
    assert mock_popen.call_count == EXPECTED_CALL_COUNT


@patch("subprocess.Popen")
@patch("concurrent.futures.ThreadPoolExecutor")
def test_parallel_conversion(mock_executor_class, mock_popen, tmp_path):
    """测试并行转换功能"""
    # 创建测试文件
    file1 = tmp_path / "file1.mp3"
    file2 = tmp_path / "file2.mp3"
    file1.write_bytes(b"fake audio data")
    file2.write_bytes(b"fake audio data")

    # 设置模拟子进程运行结果
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.communicate.return_value = (b"", b"")
    mock_popen.return_value = process_mock

    # 设置模拟线程池执行器
    mock_executor = MagicMock()
    mock_executor.__enter__.return_value = mock_executor
    mock_executor_class.return_value = mock_executor

    # 直接模拟convert_batch的行为，而不是使用map
    mock_results = [
        (str(file1), str(file1) + ".opus.ogg"),
        (str(file2), str(file2) + ".opus.ogg"),
    ]

    # 模拟submit方法和future对象
    mock_future1 = MagicMock()
    mock_future1.result.return_value = mock_results[0][1]
    mock_future2 = MagicMock()
    mock_future2.result.return_value = mock_results[1][1]

    # 设置submit方法返回mock future
    mock_executor.submit.side_effect = [mock_future1, mock_future2]

    # 模拟as_completed方法
    with patch(
        "concurrent.futures.as_completed", return_value=[mock_future1, mock_future2]
    ):
        # 创建转换器，设置并行任务数为2
        converter = AudioConverter(bitrate="128k", jobs=2)

        # 执行批量转换
        results = converter.convert_batch([str(file1), str(file2)])

        # 验证结果
        assert len(results) == EXPECTED_FILE_COUNT
        assert all(result[1] for result in results)

        # 验证使用了ThreadPoolExecutor并设置了正确的最大工作线程数
        mock_executor_class.assert_called_with(max_workers=2)

        # 验证submit被调用了两次
        assert mock_executor.submit.call_count == EXPECTED_CALL_COUNT


# 添加测试 _get_output_path 方法
def test_get_output_path():
    """测试输出路径生成逻辑"""
    converter = AudioConverter()

    # 测试没有输出目录的情况
    input_file = "test.mp3"
    output_path = converter._get_output_path(input_file, None, None)
    assert output_path == "test.opus.ogg"

    # 测试指定输出目录
    output = converter._get_output_path("test.mp3", "output_dir", None)
    assert output == os.path.join("output_dir", "test.opus.ogg")

    # 测试保持目录结构
    output = converter._get_output_path(
        os.path.join("dir1", "dir2", "test.mp3"), "output_dir", "dir1"
    )
    assert output == os.path.join("output_dir", "dir2", "test.opus.ogg")

    # 测试输入路径与基础路径相同
    output = converter._get_output_path(
        os.path.join("base_dir", "test.mp3"), "output_dir", "base_dir"
    )
    assert output == os.path.join("output_dir", "test.opus.ogg")

    # 测试有输出目录但没有基础目录的情况
    output_path = converter._get_output_path(input_file, "output", None)
    assert output_path == os.path.join("output", "test.opus.ogg")

    # 测试有输出目录和基础目录的情况
    input_file = os.path.join("base", "subdir", "test.mp3")
    output_path = converter._get_output_path(input_file, "output", "base")
    assert output_path == os.path.join("output", "subdir", "test.opus.ogg")

    # 测试计算相对路径失败的情况 - 使用mock来模拟这种情况
    with patch("os.path.relpath") as mock_relpath:
        # 模拟os.path.relpath抛出ValueError异常
        mock_relpath.side_effect = ValueError("Cannot make relative path")
        input_file = os.path.join("different_drive", "test.mp3")
        output_path = converter._get_output_path(input_file, "output", "base")
        assert output_path == os.path.join("output", "test.opus.ogg")


def test_convert_file_exception():
    """测试文件转换过程中的异常处理"""
    converter = AudioConverter()

    # 模拟FFmpeg运行时抛出异常
    with patch("asmr_toolkit.utils.ffmpeg.run_ffmpeg") as mock_run:
        mock_run.side_effect = Exception("FFmpeg error")
        result = converter.convert_file("test.mp3")
        assert result is None


def test_convert_batch_empty():
    """测试批量转换空列表"""
    converter = AudioConverter()
    result = converter.convert_batch([])
    assert result == []


def test_convert_batch_exception():
    """测试批量转换过程中的异常处理"""
    converter = AudioConverter(jobs=2)

    # 模拟并行执行时的异常
    with patch("concurrent.futures.ThreadPoolExecutor.submit") as mock_submit:
        mock_submit.side_effect = Exception("Thread error")

        # 应该捕获异常并返回空结果
        with pytest.raises(Exception):
            converter.convert_batch(["test1.mp3", "test2.mp3"])


def test_convert_file_nonexistent():
    """测试转换不存在的文件"""
    converter = AudioConverter()
    with patch("os.path.exists", return_value=False):
        result = converter.convert_file("nonexistent_file.mp3")
        assert result is None


def test_convert_batch_with_callback():
    """测试带回调函数的批量转换"""
    converter = AudioConverter()

    # 创建测试文件
    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
        # 模拟FFmpeg运行
        with patch("asmr_toolkit.core.converter.run_ffmpeg", return_value=True):
            # 创建回调函数并跟踪调用
            callback_mock = MagicMock()

            # 执行批量转换
            results = converter.convert_batch([temp_file.name], callback=callback_mock)

            # 验证结果
            assert len(results) == 1
            assert results[0][1] is not None
            callback_mock.assert_called_once_with(temp_file.name)


def test_convert_batch_partial_failure():
    """测试批量转换部分失败的情况"""
    converter = AudioConverter()

    # 创建两个测试文件
    with tempfile.NamedTemporaryFile(
        suffix=".mp3"
    ) as file1, tempfile.NamedTemporaryFile(suffix=".mp3") as file2:
        # 模拟第一个文件转换成功，第二个失败
        def mock_convert_file(input_file, output_file=None):
            if input_file == file1.name:
                return input_file + ".opus.ogg"
            return None

        with patch.object(converter, "convert_file", side_effect=mock_convert_file):
            # 执行批量转换
            results = converter.convert_batch([file1.name, file2.name])

            # 验证结果
            assert len(results) == EXPECTED_FILE_COUNT
            assert results[0][1] is not None  # 第一个文件成功
            assert results[1][1] is None  # 第二个文件失败
