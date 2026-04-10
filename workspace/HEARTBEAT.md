# 状态自检清单 (Heartbeat)

## 任务收尾与大规模变更后的自检
在认为任务即将闭环宣告完成时，执行以下心跳确认：
1. **Linter Status**: `npm run lint` （或其他可用语法检查器）必须通过，严禁将致命警告带入主干。
2. **Build Integrity**: 对核心编译/构建步骤进行一次预演（可选）。
3. **Memory Overflow**: 审视包括本目录下的 `MEMORY.md` 记忆载体是否过度膨胀？是否夹杂了失效过程日志？若是，进行无损压缩再结束任务。
4. **Agent Doc**: 检查 ` docs/agent.md ` 是否已经更新最新的关键结论、架构取舍。
5. **Subagent Cleanup**: 子代理调度结束后确认 `c:\Users\Administrator\.openclaw\subagents\runs.json` 已销毁。

*(如有一项不符合，打回 Execute 环节进行重塑)*
