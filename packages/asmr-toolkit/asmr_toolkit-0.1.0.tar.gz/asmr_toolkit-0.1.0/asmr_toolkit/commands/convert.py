import os
import multiprocessing
from typing import Optional
from pathlib import Path
from functools import wraps
from dataclasses import dataclass

import click
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn

from asmr_toolkit.utils.logging import get_logger
from asmr_toolkit.core.converter import AudioConverter

logger = get_logger("commands.convert")
console = Console()


@dataclass
class ConversionConfig:
    output_dir: Optional[str]
    recursive: bool
    bitrate: str
    jobs: int
    skip_existing: bool

    def validate(self):
        """验证参数有效性"""
        # 检查比特率格式
        if not self.bitrate.endswith("k"):
            raise ValueError("比特率格式无效，必须以k结尾")

        # 检查并行任务数
        if self.jobs < 0:
            raise ValueError("并行任务数必须大于等于0")


def conversion_options(f):
    """Click装饰器工厂，用于收集转换参数并封装为ConversionConfig对象"""

    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        help="输出目录，默认为输入路径下的out文件夹",
    )
    @click.option("--recursive", "-r", is_flag=True, help="递归处理子目录")
    @click.option("--bitrate", "-b", default="128k", help="输出音频比特率，默认为128k")
    @click.option(
        "--jobs", "-j", default=0, type=int, help="并行任务数，默认为CPU核心数"
    )
    @click.option("--skip-existing", "-s", is_flag=True, help="跳过已存在的输出文件")
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 提取参数并构造配置对象
        config = ConversionConfig(
            output_dir=kwargs.pop("output_dir"),
            recursive=kwargs.pop("recursive"),
            bitrate=kwargs.pop("bitrate"),
            jobs=kwargs.pop("jobs"),
            skip_existing=kwargs.pop("skip_existing"),
        )
        config.validate()
        return f(*args, **kwargs, config=config)

    return wrapper


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@conversion_options
def convert(input_path, config):
    """转换音频文件为Opus格式"""
    # 如果jobs为0，自动设置为CPU核心数
    if config.jobs <= 0:
        config.jobs = max(1, multiprocessing.cpu_count())
        logger.debug(f"自动设置并行任务数为CPU核心数: {config.jobs}")
    # 创建转换器（参数从config对象获取）
    converter = AudioConverter(
        bitrate=config.bitrate, jobs=config.jobs, skip_existing=config.skip_existing
    )
    # 处理输入路径
    if os.path.isdir(input_path):
        _handle_directory_conversion(
            converter, input_path, config.output_dir, config.recursive
        )
    elif os.path.isfile(input_path):
        _handle_file_conversion(converter, input_path, config.output_dir)
    else:
        logger.error(f"无效的输入路径: {input_path}")
        console.print(f"[bold red]错误: '{input_path}' 不是有效的文件或目录[/]")


def _find_audio_files(directory, recursive):
    """查找音频文件"""
    audio_extensions = (".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg")
    found_files = []

    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    found_files.extend([os.path.join(root, file)])
    else:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) and any(
                file.lower().endswith(ext) for ext in audio_extensions
            ):
                found_files.append(file_path)

    return found_files


def _handle_directory_conversion(converter, input_path, output_dir, recursive):
    """处理目录转换"""
    logger.info(f"输入是目录: {input_path}")

    # 确定输出目录
    if not output_dir:
        output_dir = os.path.join(input_path, "out")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 查找音频文件
    files_to_convert = _find_audio_files(input_path, recursive)

    if not files_to_convert:
        logger.warning(f"在目录中未找到音频文件: {input_path}")
        console.print("[bold yellow]警告: 未找到音频文件[/]")
        return

    logger.info(f"找到 {len(files_to_convert)} 个音频文件")

    # 转换文件
    _batch_convert_files(converter, files_to_convert, output_dir, input_path)


def _handle_file_conversion(converter, input_path, output_dir):
    """处理单个文件转换"""
    logger.info(f"输入是文件: {input_path}")

    # 确定输出文件路径
    output_file = None
    if output_dir:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{Path(input_path).stem}.opus.ogg")
    else:
        # 如果未指定输出目录，使用输入文件所在目录下的out文件夹
        default_output_dir = os.path.join(os.path.dirname(input_path), "out")
        os.makedirs(default_output_dir, exist_ok=True)
        output_file = os.path.join(
            default_output_dir, f"{Path(input_path).stem}.opus.ogg"
        )

    # 转换文件
    try:
        result = converter.convert_file(input_path, output_file)
        if result:
            logger.info(f"文件转换成功: {result}")
            console.print(f"[bold green]转换成功: {result}[/]")
        else:
            logger.error(f"文件转换失败: {input_path}")
            console.print(f"[bold red]转换失败: {input_path}[/]")
    except Exception:
        logger.exception(f"转换文件时发生异常: {input_path}")
        console.print("[bold red]错误: 转换过程中发生异常[/]")


def _batch_convert_files(converter, files_to_convert, output_dir, input_base_dir):
    """批量转换文件"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold green]{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("转换中...", total=len(files_to_convert))

        try:
            results = converter.convert_batch(
                files_to_convert,
                output_dir=output_dir,
                input_base_dir=input_base_dir,
                callback=lambda _: progress.update(task, advance=1),
            )
        except Exception:
            logger.exception("批量转换过程中发生异常")
            console.print("[bold red]错误: 转换过程中发生异常[/]")
            return

    # 显示结果统计
    success = sum(1 for r in results if r[1])
    console.print(
        f"[bold green]转换完成: {success}/{len(files_to_convert)} 个文件成功[/]"
    )
