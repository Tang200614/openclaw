@echo off
setlocal EnableExtensions
chcp 65001 >nul

echo.
echo ==========================================
echo    OpenClaw 开机自启与故障恢复安装程序
echo ==========================================
echo.

net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 请右键此文件，选择“以管理员身份运行”。
    echo.
    pause
    exit /b 1
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-task.ps1"
set "INSTALL_EXIT=%ERRORLEVEL%"

if not "%INSTALL_EXIT%"=="0" (
    echo.
    echo [ERROR] 安装失败，错误码: %INSTALL_EXIT%
    echo [TIP] 请查看上方 PowerShell 错误信息。
    echo.
    pause
    exit /b %INSTALL_EXIT%
)

echo.
echo [OK] 安装完成。计划任务现在直接监管 Gateway 进程，
echo      Gateway 异常退出后会自动重启，不再依赖短命的 VBS 启动器。
echo.
echo 常用命令:
echo   立即运行: schtasks /run /tn "OpenClaw Gateway"
echo   停止任务: schtasks /end /tn "OpenClaw Gateway"
echo   查看状态: schtasks /query /tn "OpenClaw Gateway" /v /fo list
echo   查看日志: type "%~dp0logs\gateway-supervisor.log"
echo.
pause
exit /b 0
