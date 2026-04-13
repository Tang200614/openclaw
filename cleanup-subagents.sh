#!/bin/bash
# OpenClaw Subagent 自动清理脚本
# 此脚本用于清理 OpenClaw 创建的 subagent worktree 分支

set -e

echo "[INFO] OpenClaw Subagent 清理脚本"
echo "[INFO] 时间: $(date)"
echo ""

cd "$HOME/.openclaw" || exit 1

# 获取所有 worktree-agent 分支
echo "[INFO] 扫描 worktree-agent 分支..."
BRANCHES=$(git branch | grep "worktree-agent" || true)

if [ -z "$BRANCHES" ]; then
    echo "[INFO] 没有发现需要清理的 worktree-agent 分支"
    exit 0
fi

echo "[INFO] 发现以下分支需要清理:"
echo "$BRANCHES"
echo ""

# 删除每个分支
echo "$BRANCHES" | while read -r branch; do
    # 去除前导空格
    branch=$(echo "$branch" | sed 's/^ *//')
    if [ -n "$branch" ]; then
        echo "[INFO] 删除分支: $branch"
        git branch -D "$branch" 2>/dev/null || echo "[WARN] 无法删除分支: $branch"
    fi
done

echo ""
echo "[INFO] 清理完成！"
echo "[INFO] 剩余 worktree-agent 分支: $(git branch | grep -c 'worktree-agent' || echo 0)"
