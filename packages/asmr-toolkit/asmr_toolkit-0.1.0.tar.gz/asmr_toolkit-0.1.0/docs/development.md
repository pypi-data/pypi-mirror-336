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

### 安装 Git Hooks

首先，安装 git hooks 以启用自动版本更新：

Linux/macOS:
```bash
# 确保脚本有执行权限
chmod +x scripts/install-hooks.sh

# 安装 hooks
./scripts/install-hooks.sh
```

Windows:
```powershell
# 以管理员身份运行 PowerShell
# 允许执行脚本
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 安装 hooks
./scripts/install-hooks.ps1
```

### 发布新版本

1. 确保安装了 bump2version：
   ```bash
   pip install bump2version
   ```

2. 创建并推送新版本标签：
   ```bash
   # 创建标签
   git tag v0.1.1

   # 推送标签到远程仓库
   git push origin v0.1.1
   ```

   这将自动：
   - 更新项目中的版本号
   - 创建一个提交记录
   - 推送标签到远程仓库
   - 触发 GitHub Actions 发布工作流
   - 创建 GitHub Release 并发布到 PyPI

### 注意事项

- 确保在创建标签前，所有更改都已提交
- 标签必须遵循 `vX.Y.Z` 格式（例如 `v0.1.0`）
- 确保已安装 bump2version (`pip install bump2version`)
