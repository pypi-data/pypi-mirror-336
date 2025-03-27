# 安装指南

## 系统要求

- Python 3.8 或更高版本（推荐 Python 3.13）
- FFmpeg（用于音频处理）

## 安装步骤

### 使用 pip 安装

```bash
pip install asmr-toolkit
```

### 使用 uv 安装（推荐）

[uv](https://github.com/astral-sh/uv) 是一个快速的 Python 包管理器。如果您已安装 uv，可以使用：

```bash
uv pip install asmr-toolkit
```

### 从源码安装

```bash
git clone https://github.com/yourusername/asmr-toolkit.git
cd asmr-toolkit

# 使用 pip
pip install -e .

# 或使用 uv（推荐）
uv pip install -e .
```

## 验证安装

安装完成后，运行以下命令验证安装是否成功：

```bash
asmr --version
```

## 开发环境

如果您想参与开发，请参考 [CONTRIBUTING.md](../CONTRIBUTING.md) 文件了解如何设置开发环境。
