# 贡献指南

感谢您考虑为 ASMR Toolkit 做出贡献！以下是一些指导原则，帮助您参与项目开发。

## 开发环境设置

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/asmr-toolkit.git
   cd asmr-toolkit
   ```

2. 创建虚拟环境
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # 在 Windows 上使用 .venv\Scripts\activate
   ```

3. 安装 uv 包管理器（如果尚未安装）
   ```bash
   pip install uv
   ```

4. 使用 uv 安装开发依赖
   ```bash
   uv pip install -e ".[dev]"
   ```

## 代码风格

我们使用 [Ruff](https://github.com/astral-sh/ruff) 进行代码格式化和导入排序。Ruff 提供了与 Black 兼容的格式化和与 isort 兼容的导入排序功能。在提交代码前，请运行：

```bash
# 格式化代码
ruff format .

# 整理导入
ruff check --select I --fix .
```

如果您使用 VS Code，可以利用以下功能：
- "Format Document"：执行与 Black 兼容的代码格式化
- "Organize Imports"：执行与 isort 兼容的导入排序

## Python 版本

项目使用 Python 3.13。请确保您的开发环境使用兼容的 Python 版本。

## 测试

请为新功能编写测试，并确保所有测试通过：

```bash
pytest
```

## 提交 Pull Request

1. 创建一个新分支
2. 进行更改
3. 运行测试
4. 提交 Pull Request

## 报告问题

如果您发现了问题，请在 GitHub 上创建一个 issue，并尽可能详细地描述问题。

感谢您的贡献！
