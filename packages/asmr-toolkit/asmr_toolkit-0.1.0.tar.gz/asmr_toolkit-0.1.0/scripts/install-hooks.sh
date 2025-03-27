#!/bin/bash

# 确保脚本目录存在
mkdir -p scripts/git-hooks

# 确保 hook 脚本有执行权限
chmod +x scripts/git-hooks/pre-tag

# 创建 git hooks 目录
mkdir -p .git/hooks

# 创建 git hooks 目录的符号链接
ln -sf ../../scripts/git-hooks/pre-tag .git/hooks/pre-tag

echo "Git hooks 安装完成"
