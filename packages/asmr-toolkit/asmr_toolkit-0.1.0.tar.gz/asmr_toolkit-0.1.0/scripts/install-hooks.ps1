# 确保脚本目录存在
if (-not (Test-Path scripts/git-hooks)) {
    New-Item -ItemType Directory -Path scripts/git-hooks -Force | Out-Null
}

# 确保 git hooks 目录存在
if (-not (Test-Path .git/hooks)) {
    New-Item -ItemType Directory -Path .git/hooks -Force | Out-Null
}

# 复制 PowerShell 脚本到 git hooks 目录
Copy-Item -Path scripts/git-hooks/pre-tag.ps1 -Destination .git/hooks/pre-tag.ps1 -Force

# 创建一个批处理文件作为入口点
@"
@echo off
powershell.exe -ExecutionPolicy Bypass -File "%~dp0pre-tag.ps1"
"@ | Out-File -FilePath .git/hooks/pre-tag -Encoding ascii -Force

Write-Host "Git hooks 安装完成"
