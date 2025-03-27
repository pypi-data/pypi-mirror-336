import os
import tempfile
from unittest.mock import ANY, MagicMock, patch

import pytest
from click.testing import CliRunner

from asmr_toolkit.cli import main
from asmr_toolkit.core.converter import AudioConverter

EXPECTED_FILE_COUNT = 2


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


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_converter():
    with patch("asmr_toolkit.commands.convert.AudioConverter") as mock:
        converter_instance = MagicMock()
        mock.return_value = converter_instance
        yield converter_instance


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_single_file(mock_converter, runner, sample_audio_file):
    """测试转换单个文件"""
    # 设置模拟转换器
    converter_instance = mock_converter()
    converter_instance.convert_file.return_value = f"{sample_audio_file}.opus.ogg"
    mock_converter.return_value = converter_instance

    # 执行命令
    result = runner.invoke(main, ["convert", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0
    converter_instance.convert_file.assert_called_once()
    assert "转换成功" in result.output


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_single_file_failure(mock_converter_class, runner, sample_audio_file):
    """测试转换单个文件失败的情况"""
    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_file.return_value = None
    mock_converter_class.return_value = converter_instance

    # 执行命令
    result = runner.invoke(main, ["convert", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0
    converter_instance.convert_file.assert_called_once()
    assert "转换失败" in result.output


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_directory_no_files(mock_converter_class, runner, tmp_path):
    """测试转换目录但没有找到音频文件的情况"""
    # 创建空目录
    test_dir = tmp_path / "empty_dir"
    test_dir.mkdir()

    # 设置模拟转换器
    converter_instance = MagicMock()
    mock_converter_class.return_value = converter_instance

    # 模拟没有找到文件的情况
    with patch("asmr_toolkit.commands.convert._find_audio_files", return_value=[]):
        # 执行命令
        result = runner.invoke(main, ["convert", str(test_dir)])

        # 验证结果
        assert result.exit_code == 0
        assert "在目录中未找到音频文件" in result.output
        converter_instance.convert_batch.assert_not_called()


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_batch_exception(mock_converter_class, runner, tmp_path):
    """测试批量转换过程中发生异常的情况"""
    # 创建测试目录和文件
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "test1.mp3").write_bytes(b"fake audio data")
    (test_dir / "test2.mp3").write_bytes(b"fake audio data")

    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_batch.side_effect = Exception("Test exception")
    mock_converter_class.return_value = converter_instance

    # 模拟找到文件
    with patch(
        "asmr_toolkit.commands.convert._find_audio_files",
        return_value=[str(test_dir / "test1.mp3"), str(test_dir / "test2.mp3")],
    ):
        # 执行命令
        result = runner.invoke(main, ["convert", str(test_dir)])

        # 验证结果
        assert result.exit_code == 0
        assert "错误: 转换过程中发生异常" in result.output


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_file_nonexistent(mock_converter):
    """测试转换不存在的文件"""
    converter = AudioConverter()
    result = converter.convert_file("nonexistent_file.mp3")
    assert result is None


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_batch_with_callback(mock_converter):
    """测试带回调函数的批量转换"""
    # 设置模拟转换器
    converter_instance = MagicMock()

    # 定义一个side_effect函数来模拟convert_batch的行为
    def mock_convert_batch(files, callback=None, **kwargs):
        # 确保调用回调函数
        if callback:
            for file in files:
                callback(file)
        return [("test.mp3", "test.mp3.opus.ogg")]

    converter_instance.convert_batch.side_effect = mock_convert_batch
    mock_converter.return_value = converter_instance

    # 创建测试文件
    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
        # 执行命令
        callback_mock = MagicMock()

        # 使用模拟的转换器实例
        results = converter_instance.convert_batch(
            [temp_file.name], callback=callback_mock
        )

        # 验证结果
        assert len(results) == 1
        assert results[0][1] is not None
        callback_mock.assert_called_once_with(temp_file.name)


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_batch_partial_failure(mock_converter):
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


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_with_output_dir(mock_converter, runner, sample_audio_file):
    """测试指定输出目录的转换"""
    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_file.return_value = "output/file.opus.ogg"
    mock_converter.return_value = converter_instance

    with tempfile.TemporaryDirectory() as output_dir:
        # 执行命令
        result = runner.invoke(
            main, ["convert", "--output-dir", output_dir, sample_audio_file]
        )

        # 验证结果
        assert result.exit_code == 0
        converter_instance.convert_file.assert_called_once()
        assert "转换成功" in result.output


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_with_bitrate(mock_converter, runner, sample_audio_file):
    """测试指定比特率的转换"""
    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_file.return_value = f"{sample_audio_file}.opus.ogg"
    mock_converter.return_value = converter_instance

    # 执行命令
    result = runner.invoke(main, ["convert", "--bitrate", "192k", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0
    # 验证创建转换器时使用了正确的比特率
    mock_converter.assert_called_with(bitrate="192k", jobs=ANY, skip_existing=False)


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_directory(mock_converter, runner, tmp_path):
    """测试转换目录"""
    # 创建测试目录和文件
    test_dir = tmp_path / "test_audio"
    test_dir.mkdir()
    test_file1 = test_dir / "file1.mp3"
    test_file2 = test_dir / "file2.mp3"
    test_file1.write_bytes(b"fake audio data")
    test_file2.write_bytes(b"fake audio data")

    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_batch.return_value = [
        (str(test_file1), f"{test_file1}.opus.ogg"),
        (str(test_file2), f"{test_file2}.opus.ogg"),
    ]
    mock_converter.return_value = converter_instance

    # 执行命令
    result = runner.invoke(main, ["convert", str(test_dir)])

    # 验证结果
    assert result.exit_code == 0
    converter_instance.convert_batch.assert_called_once()
    assert "转换完成" in result.output


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_recursive(mock_converter, runner, tmp_path):
    """测试递归转换目录"""
    # 创建嵌套目录结构
    test_dir = tmp_path / "test_audio"
    test_dir.mkdir()
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()

    test_file1 = test_dir / "file1.mp3"
    test_file2 = sub_dir / "file2.mp3"
    test_file1.write_bytes(b"fake audio data")
    test_file2.write_bytes(b"fake audio data")

    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_batch.return_value = [
        (str(test_file1), f"{test_file1}.opus.ogg"),
        (str(test_file2), f"{test_file2}.opus.ogg"),
    ]
    mock_converter.return_value = converter_instance

    # 执行命令
    result = runner.invoke(main, ["convert", "--recursive", str(test_dir)])

    # 验证结果
    assert result.exit_code == 0
    converter_instance.convert_batch.assert_called_once()
    # 验证递归模式下找到了子目录中的文件
    files_arg = converter_instance.convert_batch.call_args[0][0]
    assert len(files_arg) == EXPECTED_FILE_COUNT
    assert any(str(test_file2) in f for f in files_arg)


def test_convert_nonexistent_directory(runner):
    """测试转换不存在的目录"""
    # 使用一个肯定不存在的路径
    nonexistent_path = "/path/that/definitely/does/not/exist/12345"
    result = runner.invoke(main, ["convert", nonexistent_path])

    # 检查命令是否失败
    assert result.exit_code != 0
    # 检查错误消息中是否包含关键词
    assert "does not exist" in result.output


def test_convert_invalid_output_dir(runner, sample_audio_file):
    """测试无效的输出目录"""
    # 使用文件作为输出目录（这是无效的）
    result = runner.invoke(
        main, ["convert", "--output-dir", sample_audio_file, sample_audio_file]
    )

    # 检查命令是否失败或有错误输出
    assert "错误" in result.output or result.exit_code != 0


@patch("asmr_toolkit.core.converter.run_ffmpeg")
def test_convert_file_failure(mock_run_ffmpeg, runner, sample_audio_file):
    """测试文件转换失败的情况"""
    # 设置模拟FFmpeg运行结果为失败
    mock_run_ffmpeg.return_value = False

    result = runner.invoke(main, ["convert", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0
    assert "转换失败" in result.output
    mock_run_ffmpeg.assert_called_once()


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_default_output_dir(mock_converter, runner, sample_audio_file):
    """测试默认输出目录设置"""
    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_file.return_value = f"{sample_audio_file}.opus.ogg"
    mock_converter.return_value = converter_instance

    # 执行命令，不指定输出目录
    result = runner.invoke(main, ["convert", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0

    # 验证默认输出目录是输入文件所在目录下的out文件夹
    expected_output_dir = os.path.join(os.path.dirname(sample_audio_file), "out")

    # 检查是否使用了正确的输出目录
    args, kwargs = converter_instance.convert_file.call_args
    output_file = args[1] if len(args) > 1 else None
    assert output_file is not None
    assert expected_output_dir in output_file


@patch("asmr_toolkit.commands.convert.AudioConverter")
@patch("asmr_toolkit.commands.convert.multiprocessing.cpu_count")
def test_convert_auto_jobs(mock_cpu_count, mock_converter, runner, sample_audio_file):
    """测试自动设置并行任务数"""
    # 模拟CPU核心数
    mock_cpu_count.return_value = 4

    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_file.return_value = f"{sample_audio_file}.opus.ogg"
    mock_converter.return_value = converter_instance

    # 执行命令，不指定jobs参数
    result = runner.invoke(main, ["convert", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0

    # 验证创建转换器时使用了CPU核心数作为jobs参数
    mock_converter.assert_called_with(bitrate="128k", jobs=4, skip_existing=False)


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_skip_existing(mock_converter, runner, sample_audio_file):
    """测试跳过已存在文件选项"""
    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_file.return_value = f"{sample_audio_file}.opus.ogg"
    mock_converter.return_value = converter_instance

    # 执行命令，启用跳过已存在文件选项
    result = runner.invoke(main, ["convert", "--skip-existing", sample_audio_file])

    # 验证结果
    assert result.exit_code == 0

    # 验证创建转换器时启用了skip_existing参数
    mock_converter.assert_called_with(bitrate="128k", jobs=ANY, skip_existing=True)


@patch("asmr_toolkit.commands.convert.AudioConverter")
def test_convert_directory_default_output_dir(mock_converter, runner, tmp_path):
    """测试转换目录时的默认输出目录设置"""
    # 创建测试目录
    test_dir = tmp_path / "test_audio"
    test_dir.mkdir()

    # 设置模拟转换器
    converter_instance = MagicMock()
    converter_instance.convert_batch.return_value = []
    mock_converter.return_value = converter_instance

    # 模拟找到文件
    with patch(
        "asmr_toolkit.commands.convert._find_audio_files",
        return_value=[str(test_dir / "test1.mp3")],
    ):
        # 执行命令，不指定输出目录
        result = runner.invoke(main, ["convert", str(test_dir)])

        # 验证结果
        assert result.exit_code == 0

        # 验证默认输出目录是输入目录下的out文件夹
        expected_output_dir = os.path.join(str(test_dir), "out")

        # 检查是否使用了正确的输出目录
        args, kwargs = converter_instance.convert_batch.call_args
        assert "output_dir" in kwargs
        assert kwargs["output_dir"] == expected_output_dir
