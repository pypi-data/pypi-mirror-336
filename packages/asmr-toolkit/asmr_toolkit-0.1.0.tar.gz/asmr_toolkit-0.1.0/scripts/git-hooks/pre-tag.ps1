# 获取标签名称
$TagName = git describe --abbrev=0 --tags 2>$null
if ($LASTEXITCODE -ne 0) { $TagName = "" }

# 检查标签是否以 v 开头并且后面跟着版本号
if ($TagName -match "^v(\d+)\.(\d+)\.(\d+)$") {
    # 提取版本号
    $Version = $TagName.Substring(1)

    # 检查当前版本号
    $CurrentVersion = (Get-Content pyproject.toml | Select-String 'version = "(.+)"').Matches.Groups[1].Value

    # 如果版本号不同，则更新
    if ($Version -ne $CurrentVersion) {
        Write-Host "更新版本号从 $CurrentVersion 到 $Version"

        # 使用 bump2version 更新版本号
        bump2version --new-version $Version --allow-dirty --no-commit --no-tag patch

        # 提交更改
        git add pyproject.toml asmr_toolkit/__init__.py README.md
        git commit -m "❓chore: update version to $Version"
    }
}

exit 0
