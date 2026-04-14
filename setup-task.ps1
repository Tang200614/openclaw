# OpenClaw Gateway 开机自启任务配置脚本
$TaskName = 'OpenClaw Gateway'
$VbsPath = 'C:\Users\Administrator\.openclaw\start-openclaw.vbs'

# 删除已存在的任务
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# 创建任务操作
$Action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument '"$VbsPath"'

# 创建触发器（系统启动时）
$Trigger = New-ScheduledTaskTrigger -AtStartup

# 创建任务设置
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 使用 SYSTEM 账户运行
$Principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest

# 注册任务
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force

Write-Host '[OK] OpenClaw Gateway 计划任务创建成功！'
Write-Host ''
Write-Host '任务信息:'
Write-Host "  名称: $TaskName"
Write-Host '  触发器: 系统启动时'
Write-Host "  执行: $VbsPath"
Write-Host '  运行身份: SYSTEM'
Write-Host ''
Write-Host '网关配置:'
Write-Host '  端口: 18789'
Write-Host '  Web UI: http://localhost:18789'
Write-Host ''
Write-Host '可用操作:'
Write-Host "  立即运行: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "  停止任务: Stop-ScheduledTask -TaskName '$TaskName'"
Write-Host "  删除任务: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:\$false"
Write-Host "  查看状态: Get-ScheduledTask -TaskName '$TaskName'"
