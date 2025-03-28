import os
import concurrent.futures
from typing import List, Tuple, Callable, Optional
from pathlib import Path

from asmr_toolkit.utils.ffmpeg import run_ffmpeg
from asmr_toolkit.utils.logging import get_logger

logger = get_logger("core.converter")


class AudioConverter:
    """音频转换器核心类"""

    def __init__(self, bitrate="128k", jobs=1, skip_existing=False):
        """
        初始化转换器

        参数:
            bitrate: 输出比特率
            jobs: 并行任务数
            skip_existing: 是否跳过已存在的文件
        """
        self.bitrate = bitrate
        self.jobs = max(1, jobs)
        self.skip_existing = skip_existing
        logger.debug(
            f"初始化转换器: "
            f"bitrate={bitrate}, jobs={jobs}, skip_existing={skip_existing}"
        )

    def convert_file(
        self, input_file: str, output_file: Optional[str] = None
    ) -> Optional[str]:
        """
        转换单个音频文件

        参数:
            input_file: 输入文件路径
            output_file: 输出文件路径，如果为None则自动生成

        返回:
            成功时返回输出文件路径，失败时返回None
        """
        if not os.path.exists(input_file):
            logger.error(f"文件不存在: {input_file}")
            return None

        # 如果没有指定输出文件，则使用输入文件名但更改扩展名
        if output_file is None:
            input_path = Path(input_file)
            output_file = str(input_path.with_suffix(".opus.ogg"))

        # 检查输出文件是否已存在
        if self.skip_existing and os.path.exists(output_file):
            logger.info(f"跳过已存在的文件: {output_file}")
            return output_file

        logger.info(f"转换文件: {input_file} -> {output_file}")

        # 确保输出目录存在
        output_path = Path(output_file)
        os.makedirs(output_path.parent, exist_ok=True)

        # 调用ffmpeg进行转换
        try:
            success = run_ffmpeg(
                input_file=input_file,
                output_file=output_file,
                audio_codec="libopus",
                bitrate=self.bitrate,
                options={
                    "vbr": "on",
                    "compression_level": "10",
                },
            )

            if success:
                logger.debug(f"文件转换成功: {output_file}")
                return output_file
            else:
                logger.error(f"文件转换失败: {input_file}")
                return None
        except Exception:
            logger.exception(f"转换过程中发生异常: {input_file}")
            return None

    def convert_batch(
        self,
        files: List[str],
        output_dir: Optional[str] = None,
        input_base_dir: Optional[str] = None,
        callback: Optional[Callable[[str], None]] = None,
    ) -> List[Tuple[str, Optional[str]]]:
        """
        批量转换音频文件

        参数:
            files: 输入文件列表
            output_dir: 输出目录
            input_base_dir: 输入基础目录，用于保持目录结构
            callback: 每个文件处理完成后的回调函数

        返回:
            转换结果列表，每项为 (输入文件, 输出文件或None)
        """
        if not files:
            logger.warning("没有文件需要转换")
            return []

        logger.info(f"开始批量转换 {len(files)} 个文件")
        if output_dir:
            logger.debug(f"输出目录: {output_dir}")
        if input_base_dir:
            logger.debug(f"输入基础目录: {input_base_dir}")

        results = []

        # 单线程处理
        if self.jobs == 1:
            logger.debug("使用单线程模式")
            for input_file in files:
                output_file = self._get_output_path(
                    input_file, output_dir, input_base_dir
                )
                result = self.convert_file(input_file, output_file)
                results.append((input_file, result))
                if callback:
                    callback(input_file)

        # 多线程处理
        else:
            logger.debug(f"使用多线程模式，线程数: {self.jobs}")
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.jobs
            ) as executor:
                future_to_file = {}

                for input_file in files:
                    output_file = self._get_output_path(
                        input_file, output_dir, input_base_dir
                    )
                    future = executor.submit(self.convert_file, input_file, output_file)
                    future_to_file[future] = input_file

                for future in concurrent.futures.as_completed(future_to_file):
                    input_file = future_to_file[future]
                    try:
                        result = future.result()
                        results.append((input_file, result))
                    except Exception:
                        logger.exception(f"处理文件时发生异常: {input_file}")
                        results.append((input_file, None))

                    if callback:
                        callback(input_file)

        # 统计结果
        success_count = sum(1 for _, result in results if result is not None)
        logger.info(f"批量转换完成: {success_count}/{len(files)} 个文件成功")

        return results

    @staticmethod
    def _get_output_path(
        input_file: str, output_dir: Optional[str], input_base_dir: Optional[str]
    ) -> str:
        """生成输出文件路径"""
        input_path = Path(input_file)

        # 如果没有指定输出目录，则在原位置生成
        if not output_dir:
            return str(input_path.with_suffix(".opus.ogg"))

        # 如果指定了输出目录，则保持相对路径结构
        if input_base_dir:
            try:
                rel_path = os.path.relpath(input_file, input_base_dir)
                rel_dir = os.path.dirname(rel_path)
                output_path = os.path.join(
                    output_dir, rel_dir, f"{input_path.stem}.opus.ogg"
                )
                logger.debug(f"计算相对路径: {input_file} -> {output_path}")
                return output_path
            except ValueError:
                # 如果计算相对路径失败，则使用文件名
                logger.warning(f"计算相对路径失败: {input_file}，将直接使用文件名")
                pass

        # 默认情况：直接使用文件名
        return os.path.join(output_dir, f"{input_path.stem}.opus.ogg")
