# OpenClaw Subagent 自动清理脚本 (PowerShell)
# 此脚本用于清理 OpenClaw 创建的 subagent worktree 分支

param(
    [switch]$Force,
    [switch]$Silent
)

$ErrorActionPreference = "Continue"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    if (-not $Silent) {
        Write-Host "[$Level] $Message"
    }
}

Write-Log "OpenClaw Subagent 清理脚本"
Write-Log "时间: $(Get-Date)"

$openclawDir = "$env:USERPROFILE\.openclaw"
if (-not (Test-Path $openclawDir)) {
    Write-Log "OpenClaw 目录不存在: $openclawDir" "ERROR"
    exit 1
}

Set-Location $openclawDir

# 获取所有 worktree-agent 分支
Write-Log "扫描 worktree-agent 分支..."
$branches = git branch | Select-String "worktree-agent" | ForEach-Object { $_.ToString().Trim() }

if (-not $branches) {
    Write-Log "没有发现需要清理的 worktree-agent 分支"
    exit 0
}

Write-Log "发现 $($branches.Count) 个分支需要清理"

if (-not $Force) {
    Write-Log "分支列表:"
    $branches | ForEach-Object { Write-Log "  - $_" }
}

# 删除每个分支
$deleted = 0
$failed = 0

foreach ($branch in $branches) {
    $branchName = $branch -replace '^\*?\s*', ''
    if ($branchName) {
        try {
            Write-Log "删除分支: $branchName"
            git branch -D $branchName 2>$null
            $deleted++
        } catch {
            Write-Log "无法删除分支: $branchName" "WARN"
            $failed++
        }
    }
}

Write-Log ""
Write-Log "清理完成!"
Write-Log "成功删除: $deleted, 失败: $failed"

# 验证
$remaining = (git branch | Select-String "worktree-agent" | Measure-Object).Count
Write-Log "剩余 worktree-agent 分支: $remaining"

if ($remaining -eq 0) {
    Write-Log "所有 subagent 分支已清理!" "OK"
} else {
    Write-Log "仍有 $remaining 个分支未清理" "WARN"
}
