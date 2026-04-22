@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo    OpenClaw 开机自启任务安装程序
echo ==========================================
echo.

:: 删除已存在的任务
echo [INFO] 删除已存在的任务...
schtasks /delete /tn "OpenClaw Gateway" /f >nul 2>&1

:: 创建开机自启任务
echo [INFO] 创建新的计划任务...
schtasks /create /tn "OpenClaw Gateway" /tr "wscript.exe \"C:\Users\Administrator\.openclaw\start-openclaw.vbs\"" /sc onstart /ru "SYSTEM" /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo.
    echo [OK] 计划任务创建成功！
    echo.
    echo ==========================================
    echo 任务信息:
    echo ==========================================
    echo   名称: OpenClaw Gateway
    echo   触发器: 系统启动时
    echo   执行: C:\Users\Administrator\.openclaw\start-openclaw.vbs
    echo   运行身份: SYSTEM
    echo.
    echo ==========================================
    echo 网关配置:
    echo ==========================================
    echo   端口: 18789
    echo   Web UI: http://localhost:18789
    echo.
    echo ==========================================
    echo 可用操作:
    echo ==========================================
    echo   立即运行: schtasks /run /tn "OpenClaw Gateway"
    echo   停止任务: schtasks /end /tn "OpenClaw Gateway"
    echo   删除任务: schtasks /delete /tn "OpenClaw Gateway" /f
    echo   查看状态: schtasks /query /tn "OpenClaw Gateway"
    echo.
    echo [TIP] 重启计算机后，OpenClaw 将自动启动
) else (
    echo.
    echo [ERROR] 创建任务失败，错误码: %errorlevel%
)

echo.
pause
