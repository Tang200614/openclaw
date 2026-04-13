# OpenClaw Subagent 自动清理机制

## 问题描述

OpenClaw 在执行多 Agent 任务时，会创建 `worktree-agent-*` 分支来隔离子代理的执行环境。这些分支在任务完成后不会被自动清理，导致 git 分支堆积。

## 解决方案

### 1. 配置自动清理 (已添加到 openclaw.json)

```json
"subagents": {
  "maxConcurrent": 8,
  "cleanup": {
    "enabled": true,      // 启用自动清理
    "mode": "auto",       // 自动模式
    "onComplete": true,   // 任务完成后清理
    "onError": false,     // 错误时不清理 (保留现场)
    "maxAge": 3600,       // 最大保留时间(秒)
    "keepLast": 5         // 保留最近N个分支
  }
}
```

### 2. 手动清理工具

#### Windows 命令行工具 (openclaw-dev.cmd)

```batch
# 查看当前状态
openclaw-dev.cmd status

# 清理所有 subagent 分支
openclaw-dev.cmd clean-subagents

# 重置会话
openclaw-dev.cmd reset

# 重启 OpenClaw
openclaw-dev.cmd restart
```

#### PowerShell 脚本

```powershell
# 交互式清理 (显示确认)
.\cleanup-subagents.ps1

# 强制清理 (无确认)
.\cleanup-subagents.ps1 -Force

# 静默模式
.\cleanup-subagents.ps1 -Silent
```

#### Bash 脚本 (Git Bash/WSL)

```bash
# 执行清理
bash cleanup-subagents.sh
```

### 3. 定时自动清理

可以配置定时任务自动清理:

**Windows 任务计划程序:**
```powershell
# 每小时清理一次
schtasks /create /tn "OpenClaw Cleanup" /tr "powershell -File %USERPROFILE%\.openclaw\cleanup-subagents.ps1 -Silent" /sc hourly
```

**Cron (WSL/Git Bash):**
```bash
# 编辑 crontab
crontab -e

# 添加每小时执行
0 * * * * bash ~/.openclaw/cleanup-subagents.sh >/dev/null 2>&1
```

## 清理效果

清理前:
```
$ git branch | grep worktree-agent
  worktree-agent-a3436a1c
  worktree-agent-a4ec9c9e
  ... (可能有很多)
```

清理后:
```
$ git branch | grep worktree-agent
# 无输出，所有分支已清理
```

## 注意事项

1. **不要在子代理运行时清理** - 可能导致正在执行的任务中断
2. **错误排查时保留分支** - 设置 `onError: false` 保留现场
3. **定期手动检查** - 使用 `openclaw-dev.cmd status` 查看分支数量
4. **Git 工作区清理** - 如果使用了 `isolation: worktree`，可能需要额外清理 `.claude/worktrees/` 目录

## 相关文件

- `openclaw.json` - 主配置，包含 subagent 清理配置
- `openclaw-dev.cmd` - Windows 调试工具
- `cleanup-subagents.ps1` - PowerShell 清理脚本
- `cleanup-subagents.sh` - Bash 清理脚本
