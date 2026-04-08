@echo off
rem OpenClaw Gateway (v2026.4.5)
set "ARK_API_KEY=bdfb66d3-3383-4e27-8478-ce803ace7af5"
set "ARK_MODEL_ID=glm-4.7"
set "ARK_CODING_PLAN=true"
set "DINGTALK_CLIENT_ID=dingwt8xy0eacc51gr5c"
set "DINGTALK_CLIENT_SECRET=x3DJkPL-NT_qd5vloHvyBAqSEEsQXaQoUhEcfWQf9hIRvpDOCpy77MjCuFb2jG28"
set "TAVILY_API_KEY=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"
set "HOME=C:\Users\Administrator"
set "TMPDIR=C:\Users\ADMINI~1\AppData\Local\Temp"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.4.5"
C:\Users\Administrator\AppData\Local\Programs\nodejs\node.exe C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789
