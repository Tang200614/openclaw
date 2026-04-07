@echo off
rem OpenClaw Gateway (v2026.4.5)
set "HOME=C:\Users\Administrator"
set "TMPDIR=C:\Users\ADMINI~1\AppData\Local\Temp"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.4.5"
C:\Users\Administrator\AppData\Local\Programs\nodejs\node.exe C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\entry.js gateway --port 18789
