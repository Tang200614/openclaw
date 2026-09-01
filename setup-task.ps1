#requires -RunAsAdministrator

[CmdletBinding()]
param(
    [string]$TaskName = 'OpenClaw Gateway',
    [switch]$NoStart
)

$ErrorActionPreference = 'Stop'

$OpenClawHome = $PSScriptRoot
$RunnerPath = Join-Path $OpenClawHome 'openclaw-task-runner.cmd'

if (-not (Test-Path -LiteralPath $RunnerPath -PathType Leaf)) {
    throw "Task runner not found: $RunnerPath"
}

Write-Host "[INFO] Installing scheduled task: $TaskName"
Write-Host "[INFO] OpenClaw home: $OpenClawHome"

# Stop and remove the previous definition. The old task launched a short-lived
# VBS process asynchronously, so Task Scheduler could not supervise the actual
# gateway process after the VBS process exited.
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($null -ne $ExistingTask) {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Clean up only stale OpenClaw gateway Node processes. Never terminate every
# node.exe process because other development tools may be using Node.js.
try {
    Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
        Where-Object {
            $_.CommandLine -and
            $_.CommandLine -match 'openclaw[\\/]+dist[\\/]+index\.js' -and
            $_.CommandLine -match '(?<![A-Za-z])gateway(?![A-Za-z])'
        } |
        ForEach-Object {
            Write-Host "[INFO] Stopping stale gateway process PID $($_.ProcessId)"
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
        }
}
catch {
    Write-Warning "Could not inspect stale gateway processes: $($_.Exception.Message)"
}

$CmdExe = Join-Path $env:SystemRoot 'System32\cmd.exe'
$ActionArguments = '/d /c ""{0}""' -f $RunnerPath
$Action = New-ScheduledTaskAction -Execute $CmdExe -Argument $ActionArguments -WorkingDirectory $OpenClawHome

$BootTrigger = New-ScheduledTaskTrigger -AtStartup
$BootTrigger.Delay = 'PT30S'

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0) `
    -MultipleInstances IgnoreNew

$Principal = New-ScheduledTaskPrincipal `
    -UserId 'SYSTEM' `
    -LogonType ServiceAccount `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName $TaskName `
    -Description 'OpenClaw Gateway with automatic restart and Feishu connection recovery' `
    -Action $Action `
    -Trigger $BootTrigger `
    -Settings $Settings `
    -Principal $Principal `
    -Force | Out-Null

if (-not $NoStart) {
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 3
}

$Task = Get-ScheduledTask -TaskName $TaskName
$TaskInfo = Get-ScheduledTaskInfo -TaskName $TaskName

Write-Host ''
Write-Host '[OK] OpenClaw Gateway task installed.' -ForegroundColor Green
Write-Host "  State:        $($Task.State)"
Write-Host "  Last result:  $($TaskInfo.LastTaskResult)"
Write-Host "  Runner:       $RunnerPath"
Write-Host '  Trigger:      system startup, delayed 30 seconds'
Write-Host '  Recovery:     restart every 1 minute after failure (up to 999 times)'
Write-Host '  Run account:  SYSTEM'
Write-Host '  Gateway port: 18789'
