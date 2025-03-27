# API 参考

## 核心模块

### AudioConverter

`AudioConverter` 类是 ASMR Toolkit 的核心组件，负责音频文件的转换。

```python
from asmr_toolkit.core.converter import AudioConverter

# 创建转换器实例
converter = AudioConverter(bitrate="192k", jobs=4)

# 转换单个文件
output_file = converter.convert_file("input.mp3", "output.opus.ogg")

# 批量转换文件
files = ["file1.mp3", "file2.wav", "file3.flac"]
results = converter.convert_batch(files, output_dir="converted/")
```

#### 参数

- `bitrate`: 输出音频的比特率，默认为 "128k"
- `jobs`: 并行处理的任务数，默认为 1

#### 方法

##### convert_file

```python
def convert_file(self, input_file: str, output_file: Optional[str] = None) -> Optional[str]
```

转换单个音频文件。

- `input_file`: 输入文件路径
- `output_file`: 输出文件路径，如果为 None 则自动生成
- 返回: 成功时返回输出文件路径，失败时返回 None

##### convert_batch

```python
def convert_batch(
    self,
    files: List[str],
    output_dir: Optional[str] = None,
    input_base_dir: Optional[str] = None,
    callback: Optional[Callable[[str], None]] = None
) -> List[Tuple[str, Optional[str]]]
```

批量转换音频文件。

- `files`: 输入文件列表
- `output_dir`: 输出目录
- `input_base_dir`: 输入基础目录，用于保持目录结构
- `callback`: 每个文件处理完成后的回调函数
- 返回: 转换结果列表，每项为 (输入文件, 输出文件或None)
