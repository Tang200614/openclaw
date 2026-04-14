@echo off
echo ==========================================
echo    OpenClaw 开机自启任务安装程序
echo ==========================================
echo.

:: 使用 VBS 脚本隐藏窗口启动
set "VBS_PATH=C:\Users\Administrator\.openclaw\start-openclaw.vbs"

:: 删除已存在的任务
schtasks /delete /tn "OpenClaw Gateway" /f >nul 2>&1

:: 创建开机自启任务
schtasks /create ^
  /tn "OpenClaw Gateway" ^
  /tr "wscript.exe \"%VBS_PATH%\"" ^
  /sc onstart ^
  /ru "SYSTEM" ^
  /rl HIGHEST ^
  /f

if %errorlevel% equ 0 (
    echo [OK] 计划任务创建成功！
    echo.
    echo 任务信息:
    echo   名称: OpenClaw Gateway
    echo   触发器: 系统启动时
    echo   执行: %VBS_PATH%
    echo   运行身份: SYSTEM
    echo.
    echo 网关配置:
    echo   端口: 18789
    echo   Web UI: http://localhost:18789
    echo.
    echo 可选操作:
    echo   1. 立即运行: schtasks /run /tn "OpenClaw Gateway"
    echo   2. 删除任务: schtasks /delete /tn "OpenClaw Gateway" /f
    echo   3. 查看状态: schtasks /query /tn "OpenClaw Gateway"
) else (
    echo [ERROR] 创建任务失败，错误码: %errorlevel%
)

echo.
pause
