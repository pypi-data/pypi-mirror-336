import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from asmr_toolkit.cli import main
from asmr_toolkit.utils.ffmpeg import check_ffmpeg

# 跳过集成测试如果FFmpeg未安装
pytestmark = pytest.mark.skipif(not check_ffmpeg(), reason="FFmpeg not installed")


def test_default_output_dir_integration():
    """测试默认输出目录功能的集成测试"""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建一个简单但有效的WAV测试文件
        input_file = Path(temp_dir) / "test.wav"
        with open(input_file, "wb") as f:
            # 创建一个简单的WAV文件头和一些静音数据
            wav_header = bytes.fromhex(
                "52494646"  # "RIFF"
                + "24000000"  # 文件大小 (36 bytes)
                + "57415645"  # "WAVE"
                + "666d7420"  # "fmt "
                + "10000000"  # 块大小 (16 bytes)
                + "0100"  # 格式代码 (PCM = 1)
                + "0100"  # 通道数 (1 = 单声道)
                + "44AC0000"  # 采样率 (44100 Hz)
                + "88580100"  # 字节率 (44100*2 = 88200)
                + "0200"  # 块对齐 (2 bytes)
                + "1000"  # 位深度 (16 bits)
                + "64617461"  # "data"
                + "00000000"  # 数据大小 (0 bytes)
            )
            f.write(wav_header)
            # 添加一些静音数据
            f.write(b"\x00" * 1000)

        # 预期的默认输出目录
        expected_output_dir = Path(temp_dir) / "out"
        expected_output_file = expected_output_dir / "test.opus.ogg"

        try:
            # 执行命令，不指定输出目录
            result = runner.invoke(main, ["convert", str(input_file)])

            # 验证结果
            assert result.exit_code == 0
            assert expected_output_dir.exists()
            assert expected_output_file.exists()
            assert expected_output_file.stat().st_size > 0

        finally:
            # 清理
            if expected_output_file.exists():
                expected_output_file.unlink()
            if expected_output_dir.exists():
                expected_output_dir.rmdir()
