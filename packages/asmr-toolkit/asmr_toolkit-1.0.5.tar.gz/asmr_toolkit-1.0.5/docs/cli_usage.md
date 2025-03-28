# 命令行使用

ASMR Toolkit 提供了一系列命令行工具，用于音频文件的转换和处理。

## 基本用法

```bash
asmr [命令] [选项]
```

## 可用命令

### convert - 音频转换

将音频文件转换为 Opus 格式。

```bash
asmr convert [选项] <输入文件/目录>
```

#### 选项

- `--output-dir, -o`: 指定输出目录（默认：输入路径下的out文件夹）
- `--bitrate, -b`: 设置输出比特率（默认：128k）
- `--jobs, -j`: 并行处理的任务数（默认：CPU核心数）
- `--recursive, -r`: 递归处理目录中的文件
- `--skip-existing, -s`: 跳过已存在的输出文件

#### 示例

```bash
# 转换单个文件
asmr convert music.mp3

# 转换目录中的所有音频文件
asmr convert --recursive music_folder/

# 指定输出目录和比特率
asmr convert --output-dir converted/ --bitrate 192k music.mp3

# 使用4个并行任务处理
asmr convert --jobs 4 --recursive music_folder/
```
