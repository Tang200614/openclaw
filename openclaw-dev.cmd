@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo    OpenClaw 开发调试工具
echo ==========================================
echo.

if "%~1"=="" goto :menu
if "%~1"=="reset" goto :reset
if "%~1"=="status" goto :status
if "%~1"=="logs" goto :logs
if "%~1"=="debug" goto :debug
if "%~1"=="clean" goto :clean
if "%~1"=="clean-subagents" goto :clean_subagents
if "%~1"=="restart" goto :restart
if "%~1"=="help" goto :help
goto :menu

:menu
echo 用法: openclaw-dev.cmd [命令]
echo.
echo 可用命令:
echo   reset          - 重置会话 (删除所有 jsonl 会话文件)
echo   status         - 查看当前 OpenClaw 状态
echo   logs           - 查看最近日志
echo   debug          - 启动调试模式
echo   clean          - 清理临时文件
echo   clean-subagents - 清理 subagent worktree 分支 [!重要!]
echo   restart        - 重启 OpenClaw 服务
echo   help           - 显示帮助信息
echo.
goto :eof

:reset
echo [INFO] 正在重置 OpenClaw 会话...
if exist "%USERPROFILE%\.claude\projects\C--Users-Administrator--openclaw\*.jsonl" (
    del /q "%USERPROFILE%\.claude\projects\C--Users-Administrator--openclaw\*.jsonl"
    echo [OK] 已删除所有 jsonl 会话文件
) else (
    echo [INFO] 没有需要清理的会话文件
)
echo [OK] 会话重置完成
goto :eof

:status
echo [INFO] OpenClaw 状态检查...
echo.
echo --- Git 分支 ---
cd /d %USERPROFILE%\.openclaw
git branch -a | findstr "worktree-agent"
echo.
echo --- Subagent Worktree 分支数量 ---
cd /d %USERPROFILE%\.openclaw
for /f %%a in ('git branch -a ^| findstr /c:"worktree-agent" ^| wc -l') do echo 当前 worktree-agent 分支: %%a
echo.
echo --- 会话文件 ---
if exist "%USERPROFILE%\.claude\projects\C--Users-Administrator--openclaw\" (
    dir /b "%USERPROFILE%\.claude\projects\C--Users-Administrator--openclaw\*.jsonl" 2>nul | find /c /v ""
) else (
    echo 0
)
echo.
echo --- 最近修改的 Subagent ---
cd /d %USERPROFILE%\.openclaw
git branch -a --sort=-committerdate | findstr "worktree-agent" | head -5
goto :eof

:logs
echo [INFO] 查看 OpenClaw 日志...
if exist "%USERPROFILE%\.openclaw\logs\" (
    dir /b /o-d "%USERPROFILE%\.openclaw\logs\" | head -10
) else (
    echo [WARN] 日志目录不存在
)
goto :eof

:debug
echo [INFO] 启动调试模式...
set OPENCLAW_DEBUG=1
set OPENCLAW_LOG_LEVEL=debug
echo [INFO] 环境变量已设置:
echo   OPENCLAW_DEBUG=1
echo   OPENCLAW_LOG_LEVEL=debug
echo [INFO] 请在当前窗口运行 openclaw 命令
goto :eof

:clean
echo [INFO] 开始清理临时文件...

:: 清理可能残留的临时文件
if exist "%TEMP%\openclaw-*" (
    rmdir /s /q "%TEMP%\openclaw-*" 2>nul
    echo [OK] 已清理临时目录
)

:: 清理空的 worktree 分支（没有对应 worktree 目录的分支）
cd /d %USERPROFILE%\.openclaw
echo [INFO] 检查孤立的 worktree 分支...
for /f "tokens=*" %%b in ('git branch -a ^| findstr /c:"worktree-agent"') do (
    echo   发现分支: %%b
)

echo [OK] 临时文件清理完成
echo [TIP] 使用 'clean-subagents' 命令彻底清理 subagent 分支
goto :eof

:clean_subagents
echo [INFO] ==========================================
echo [INFO]  开始清理 Subagent Worktree 分支
echo [INFO] ==========================================
echo.

cd /d %USERPROFILE%\.openclaw

:: 列出所有 worktree-agent 分支
echo [INFO] 当前存在的 worktree-agent 分支:
git branch -a | findstr /c:"worktree-agent" | findstr /v /c:"grep"
if errorlevel 1 (
    echo [INFO] 没有找到 worktree-agent 分支
    goto :eof
)

echo.
echo [WARN] 即将删除所有 worktree-agent 分支！
echo [WARN] 请确保没有正在运行的 subagent 任务！
echo.
set /p confirm="确认删除? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo [INFO] 操作已取消
    goto :eof
)

echo.
echo [INFO] 正在删除 worktree-agent 分支...

:: 删除本地 worktree-agent 分支
for /f "tokens=*" %%b in ('git branch ^| findstr /c:"worktree-agent"') do (
    set "branch=%%b"
    setlocal enabledelayedexpansion
    set "branch=!branch:* =!"
    echo [INFO] 删除分支: !branch!
    git branch -D !branch! 2>nul
    endlocal
)

:: 删除 remote worktree-agent 分支（如果有）
for /f "tokens=*" %%b in ('git branch -r ^| findstr /c:"worktree-agent"') do (
    set "branch=%%b"
    setlocal enabledelayedexpansion
    set "branch=!branch:origin/=!"
    echo [INFO] 删除远程分支: !branch!
    git push origin --delete !branch! 2>nul
    endlocal
)

echo.
echo [OK] Subagent worktree 分支清理完成！
echo.
echo [INFO] 当前剩余分支:
git branch -a | findstr /c:"worktree-agent" | findstr /v /c:"grep" || echo 无
goto :eof

:restart
echo [INFO] 重启 OpenClaw 服务...
echo [INFO] 停止服务...
taskkill /f /im openclaw.exe 2>nul
taskkill /f /im node.exe 2>nul
timeout /t 2 /nobreak >nul
echo [INFO] 启动服务...
start /b openclaw.exe >nul 2>&1
echo [OK] OpenClaw 已重启
goto :eof

:help
echo OpenClaw 开发调试工具 - 帮助信息
echo.
echo 主要功能:
echo   1. 重置会话: 删除所有 jsonl 会话文件，用于清理上下文
echo   2. 查看状态: 显示当前 subagent、会话等状态
echo   3. 清理 Subagent: 删除所有 worktree-agent 分支 [!重要功能!]
echo   4. 调试模式: 设置调试环境变量
echo.
echo 使用示例:
echo   openclaw-dev.cmd reset
echo   openclaw-dev.cmd clean-subagents
echo   openclaw-dev.cmd status
goto :eof
