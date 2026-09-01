@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist "%~dp0logs" mkdir "%~dp0logs" >nul 2>&1
set "SUPERVISOR_LOG=%~dp0logs\gateway-supervisor.log"
set "NETWORK_HOST=open.feishu.cn"
set "NETWORK_RETRY_SECONDS=15"

>>"%SUPERVISOR_LOG%" echo [%date% %time%] OpenClaw task runner started.

:wait_for_network
powershell.exe -NoLogo -NoProfile -NonInteractive -Command "try { [void][System.Net.Dns]::GetHostAddresses('%NETWORK_HOST%'); exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    >>"%SUPERVISOR_LOG%" echo [%date% %time%] Waiting for DNS resolution: %NETWORK_HOST%
    timeout.exe /t %NETWORK_RETRY_SECONDS% /nobreak >nul
    goto wait_for_network
)

>>"%SUPERVISOR_LOG%" echo [%date% %time%] Network is ready; starting gateway.
call "%~dp0gateway.cmd" >>"%SUPERVISOR_LOG%" 2>&1
set "GATEWAY_EXIT=%ERRORLEVEL%"
>>"%SUPERVISOR_LOG%" echo [%date% %time%] Gateway exited with code %GATEWAY_EXIT%.

rem Task Scheduler restarts only failed actions. Treat every unexpected gateway
rem exit as a failure, including exit code 0, so the service is always restored.
if "%GATEWAY_EXIT%"=="0" set "GATEWAY_EXIT=1"
exit /b %GATEWAY_EXIT%
