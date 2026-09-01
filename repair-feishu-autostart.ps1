#requires -RunAsAdministrator

[CmdletBinding()]
param(
    [switch]$SkipSdkInstall,
    [switch]$SkipTaskInstall
)

$ErrorActionPreference = 'Stop'
$OpenClawHome = $PSScriptRoot
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Step {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Get-NpmPath {
    $Command = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($null -ne $Command) {
        return $Command.Path
    }

    $ProfileRoot = Split-Path -Parent $OpenClawHome
    $Candidates = @(
        (Join-Path $ProfileRoot 'AppData\Local\Programs\nodejs\npm.cmd'),
        (Join-Path $env:LOCALAPPDATA 'Programs\nodejs\npm.cmd'),
        'C:\Program Files\nodejs\npm.cmd',
        'C:\Users\Administrator\AppData\Local\Programs\nodejs\npm.cmd'
    ) | Where-Object { $_ }

    foreach ($Candidate in $Candidates) {
        if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
            return $Candidate
        }
    }

    throw 'npm.cmd was not found. Install Node.js 22+ or add npm to PATH.'
}

function Patch-LarkClient {
    param([Parameter(Mandatory = $true)][string]$ClientPath)

    $Text = [System.IO.File]::ReadAllText($ClientPath)
    $NewLine = if ($Text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $Changed = $false

    if ($Text -notmatch 'wsConfig\s*:\s*\{\s*pingTimeout\s*:\s*150\s*\}') {
        $Needle = '            loggerLevel: Lark.LoggerLevel.info,' + $NewLine + '        });'
        $Replacement = '            loggerLevel: Lark.LoggerLevel.info,' + $NewLine +
            '            // Feishu server ping cadence is 120 seconds. Enable the SDK' + $NewLine +
            '            // liveness watchdog so half-open NAT/TUN connections self-heal.' + $NewLine +
            '            wsConfig: { pingTimeout: 150 },' + $NewLine +
            '        });'

        $Index = $Text.IndexOf($Needle, [System.StringComparison]::Ordinal)
        if ($Index -lt 0) {
            throw "Could not locate the WSClient constructor in $ClientPath"
        }

        $ContextStart = [Math]::Max(0, $Index - 350)
        $ContextLength = $Index - $ContextStart
        $Context = $Text.Substring($ContextStart, $ContextLength)
        if ($Context -notmatch 'this\._wsClient\s*=\s*new\s+Lark\.WSClient') {
            throw "The matched loggerLevel block is not the Feishu WSClient constructor: $ClientPath"
        }

        $Text = $Text.Remove($Index, $Needle.Length).Insert($Index, $Replacement)
        $Changed = $true
    }

    $AsyncNeedle = '                void this._wsClient.start({ eventDispatcher: dispatcher });'
    if ($Text.Contains($AsyncNeedle) -and $Text -notmatch 'Promise\.resolve\(this\._wsClient\.start') {
        $AsyncReplacement = '                Promise.resolve(this._wsClient.start({ eventDispatcher: dispatcher })).catch((err) => {' + $NewLine +
            '                    this.disconnect();' + $NewLine +
            '                    reject(err instanceof Error ? err : new Error(String(err)));' + $NewLine +
            '                });'
        $Text = $Text.Replace($AsyncNeedle, $AsyncReplacement)
        $Changed = $true
    }

    if ($Changed) {
        $BackupPath = "$ClientPath.bak-$Timestamp"
        Copy-Item -LiteralPath $ClientPath -Destination $BackupPath -Force
        [System.IO.File]::WriteAllText($ClientPath, $Text, $Utf8NoBom)
        Write-Host "[OK] Patched: $ClientPath" -ForegroundColor Green
        Write-Host "     Backup: $BackupPath"
    }
    else {
        Write-Host "[OK] Liveness patch already present: $ClientPath" -ForegroundColor Green
    }
}

Write-Step "OpenClaw home: $OpenClawHome"

$ProfileRoot = Split-Path -Parent $OpenClawHome
$PluginCandidates = @(
    (Join-Path $OpenClawHome 'extensions\openclaw-lark'),
    (Join-Path $env:USERPROFILE '.openclaw\extensions\openclaw-lark'),
    (Join-Path $ProfileRoot 'AppData\Local\Programs\nodejs\node_modules\openclaw\extensions\openclaw-lark'),
    (Join-Path $env:LOCALAPPDATA 'Programs\nodejs\node_modules\openclaw\extensions\openclaw-lark'),
    (Join-Path $env:APPDATA 'npm\node_modules\openclaw\extensions\openclaw-lark'),
    'C:\Users\Administrator\.openclaw\extensions\openclaw-lark',
    'C:\Users\Administrator\AppData\Local\Programs\nodejs\node_modules\openclaw\extensions\openclaw-lark'
) | Where-Object { $_ } | Select-Object -Unique

$PluginDirectories = @()
foreach ($Candidate in $PluginCandidates) {
    $PackagePath = Join-Path $Candidate 'package.json'
    $ClientPath = Join-Path $Candidate 'src\core\lark-client.js'
    if ((Test-Path -LiteralPath $PackagePath -PathType Leaf) -and
        (Test-Path -LiteralPath $ClientPath -PathType Leaf)) {
        $PluginDirectories += (Get-Item -LiteralPath $Candidate).FullName
    }
}
$PluginDirectories = $PluginDirectories | Select-Object -Unique

if ($PluginDirectories.Count -eq 0) {
    throw 'No compatible openclaw-lark installation was found.'
}

$NpmPath = $null
if (-not $SkipSdkInstall) {
    $NpmPath = Get-NpmPath
    Write-Step "Using npm: $NpmPath"
}

foreach ($PluginDirectory in $PluginDirectories) {
    Write-Step "Repairing Feishu plugin: $PluginDirectory"

    if (-not $SkipSdkInstall) {
        $PackageJson = Join-Path $PluginDirectory 'package.json'
        $PackageLock = Join-Path $PluginDirectory 'package-lock.json'
        Copy-Item -LiteralPath $PackageJson -Destination "$PackageJson.bak-$Timestamp" -Force
        if (Test-Path -LiteralPath $PackageLock -PathType Leaf) {
            Copy-Item -LiteralPath $PackageLock -Destination "$PackageLock.bak-$Timestamp" -Force
        }

        Push-Location $PluginDirectory
        try {
            & $NpmPath install '@larksuiteoapi/node-sdk@1.64.0' --save-exact --no-audit --no-fund
            if ($LASTEXITCODE -ne 0) {
                throw "npm install failed with exit code $LASTEXITCODE in $PluginDirectory"
            }
        }
        finally {
            Pop-Location
        }

        $SdkPackagePath = Join-Path $PluginDirectory 'node_modules\@larksuiteoapi\node-sdk\package.json'
        if (-not (Test-Path -LiteralPath $SdkPackagePath -PathType Leaf)) {
            throw "SDK package was not installed: $SdkPackagePath"
        }
        $SdkVersion = (Get-Content -LiteralPath $SdkPackagePath -Raw | ConvertFrom-Json).version
        if ($SdkVersion -ne '1.64.0') {
            throw "Expected Feishu SDK 1.64.0, found $SdkVersion in $PluginDirectory"
        }
        Write-Host '[OK] Feishu Node SDK 1.64.0 installed.' -ForegroundColor Green
    }

    Patch-LarkClient -ClientPath (Join-Path $PluginDirectory 'src\core\lark-client.js')
}

if (-not $SkipTaskInstall) {
    $SetupTaskScript = Join-Path $OpenClawHome 'setup-task.ps1'
    if (-not (Test-Path -LiteralPath $SetupTaskScript -PathType Leaf)) {
        throw "Task setup script not found: $SetupTaskScript"
    }

    Write-Step 'Installing the hardened Windows startup task'
    & $SetupTaskScript
}

Write-Step 'Waiting for Gateway port 18789'
$Deadline = (Get-Date).AddSeconds(90)
$PortReady = $false
while ((Get-Date) -lt $Deadline) {
    $Client = New-Object System.Net.Sockets.TcpClient
    try {
        $Connect = $Client.BeginConnect('127.0.0.1', 18789, $null, $null)
        if ($Connect.AsyncWaitHandle.WaitOne(1000, $false)) {
            $Client.EndConnect($Connect)
            $PortReady = $true
            break
        }
    }
    catch {
        # Gateway is still starting; retry below.
    }
    finally {
        $Client.Close()
    }
    Start-Sleep -Seconds 3
}

if (-not $PortReady) {
    $LogPath = Join-Path $OpenClawHome 'logs\gateway-supervisor.log'
    Write-Warning "Gateway port 18789 did not become ready within 90 seconds. Review: $LogPath"
    exit 2
}

Write-Host ''
Write-Host '[OK] Repair completed successfully.' -ForegroundColor Green
Write-Host '  - Feishu SDK pinned to 1.64.0'
Write-Host '  - WebSocket half-open detection enabled (pingTimeout: 150s)'
Write-Host '  - asynchronous WebSocket startup errors are now observed'
Write-Host '  - Windows Task Scheduler directly supervises the gateway process'
Write-Host '  - automatic restart is enabled after process failure'
Write-Host '  - Gateway is listening on port 18789'
