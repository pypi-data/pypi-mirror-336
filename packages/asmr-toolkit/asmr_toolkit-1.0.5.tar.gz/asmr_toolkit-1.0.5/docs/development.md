# 开发指南

本文档提供了 ASMR Toolkit 项目的开发指南。

## 开发环境设置

### 前提条件

- Python 3.13
- uv 包管理器
- FFmpeg

### 设置步骤

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

3. 使用 uv 安装开发依赖
   ```bash
   uv pip install -e ".[dev]"
   ```

## 代码风格

我们使用 Ruff 进行代码格式化和导入排序。Ruff 提供了与 Black 兼容的格式化和与 isort 兼容的导入排序功能。

### 使用 VS Code

如果您使用 VS Code，可以利用以下功能：
- "Format Document"：执行与 Black 兼容的代码格式化
- "Organize Imports"：执行与 isort 兼容的导入排序

### 命令行使用

```bash
# 格式化代码
ruff format .

# 整理导入
ruff check --select I --fix .

# 运行所有 lint 检查
ruff check .
```

## 项目结构

```
asmr-toolkit/
├── asmr_toolkit/         # 主源代码目录
│   ├── __init__.py
│   ├── cli.py            # 命令行接口
│   ├── commands/         # 命令实现
│   └── core/             # 核心功能
├── docs/                 # 文档
├── tests/                # 测试
├── pyproject.toml        # 项目配置
├── README.md             # 项目说明
└── CONTRIBUTING.md       # 贡献指南
```

## 测试

我们使用 pytest 进行测试。运行测试：

```bash
pytest
```

## 版本控制

我们使用语义化版本控制（[SemVer](https://semver.org/)）。版本号格式为 X.Y.Z：
- X：主版本号，不兼容的 API 更改
- Y：次版本号，向后兼容的功能添加
- Z：修订号，向后兼容的问题修复

## 发布流程

### 发布新版本

1. 确保安装了 Bump My Version：
   ```bash
   # 使用 pip
   pip install bump-my-version

   # 或使用 uv（推荐）
   uv tool install bump-my-version
   ```

2. 使用 bump-my-version 更新版本并创建标签：
   ```bash
   # 更新补丁版本 (Z in X.Y.Z)
   bump-my-version bump patch

   # 或更新次要版本 (Y in X.Y.Z)
   bump-my-version bump minor

   # 或更新主要版本 (X in X.Y.Z)
   bump-my-version bump major
   ```

   这将自动：
   - 更新项目中的版本号（在 pyproject.toml 和 asmr_toolkit/__init__.py 中）
   - 创建一个提交记录
   - 创建一个新的标签

3. 推送更改和标签到远程仓库：
   ```bash
   git push && git push --tags
   ```

   这将触发 GitHub Actions 工作流，该工作流会：
   - 发布包到 PyPI
   - 创建 GitHub Release
   - 自动生成 changelog 并添加到 Release 说明中

### 查看版本信息

可以使用以下命令查看当前版本和可能的版本升级路径：

```bash
# 查看当前版本
bump-my-version show current_version

# 查看可能的版本升级路径
bump-my-version show-bump
```

### 注意事项

- 确保在创建版本更新前，所有更改都已提交
- 标签将自动遵循 `vX.Y.Z` 格式（例如 `v0.1.0`）
- 可以使用 `--new-version X.Y.Z` 参数指定具体版本号：`bump-my-version bump --new-version 1.2.3 patch`
- 使用 `--dry-run` 选项可以预览将要进行的更改：`bump-my-version bump patch --dry-run`
- 版本配置存储在项目的 pyproject.toml 文件中
