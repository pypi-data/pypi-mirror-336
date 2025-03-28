import os
import tempfile

import pytest

from asmr_toolkit.utils.ffmpeg import check_ffmpeg
from asmr_toolkit.core.converter import AudioConverter

# 跳过集成测试如果FFmpeg未安装
pytestmark = pytest.mark.skipif(not check_ffmpeg(), reason="FFmpeg not installed")


def test_real_conversion():
    """测试实际的FFmpeg转换功能"""
    # 创建一个简单的测试音频文件
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
        # 创建一个简单的WAV文件头和一些静音数据
        # 这不是一个完整的WAV文件，但足够FFmpeg识别
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
        temp.write(wav_header)
        # 添加一些静音数据
        temp.write(b"\x00" * 1000)
        temp_path = temp.name

    try:
        # 创建转换器
        converter = AudioConverter(bitrate="128k")

        # 执行转换
        output_file = converter.convert_file(temp_path)

        # 验证结果
        assert output_file is not None
        assert os.path.exists(output_file)
        assert output_file.endswith(".opus.ogg")
        assert os.path.getsize(output_file) > 0

        # 清理
        os.unlink(output_file)
    finally:
        # 清理测试文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)
