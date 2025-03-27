import subprocess
from typing import Any, Dict, Optional

from asmr_toolkit.utils.logging import get_logger

logger = get_logger("utils.ffmpeg")


def check_ffmpeg() -> bool:
    """检查ffmpeg是否已安装"""
    try:
        # Using Popen instead of run for consistency with other functions
        process = subprocess.Popen(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        process.communicate()
        return process.returncode == 0
    except FileNotFoundError:
        return False


def run_ffmpeg(
    input_file: str,
    output_file: str,
    audio_codec: str = "libopus",
    bitrate: str = "128k",
    options: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    运行 FFmpeg 命令进行音频转换

    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
        audio_codec: 音频编解码器
        bitrate: 比特率
        options: 附加选项

    返回:
        转换是否成功
    """
    cmd = ["ffmpeg", "-i", input_file, "-c:a", audio_codec, "-b:a", bitrate]

    # 添加附加选项
    if options:
        for key, value in options.items():
            cmd.extend([f"-{key}", str(value)])

    # 添加输出文件
    cmd.append(output_file)

    logger.debug(f"执行命令: {' '.join(cmd)}")

    try:
        # 使用 subprocess.PIPE 捕获输出，并设置 errors='ignore' 忽略编码错误
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",  # 忽略编码错误
        )

        # 等待进程完成
        stdout, stderr = process.communicate()

        # 检查返回码
        if process.returncode != 0:
            logger.error(f"FFmpeg 命令失败，返回码: {process.returncode}")
            logger.debug(f"FFmpeg 错误输出: {process.stderr}")
            return False

        logger.debug("FFmpeg 命令成功完成")
        return True
    except Exception as e:
        logger.exception(f"执行 FFmpeg 时发生异常: {str(e)}")
        return False
