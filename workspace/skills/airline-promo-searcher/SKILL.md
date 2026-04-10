---
name: airline-promo-searcher
description: 批量查询航司和机票优惠政策
metadata:
  {
    "openclaw":
      {
        "emoji": "✈️",
        "requires": {},
      },
  }
---

# 航空优惠深度搜索技能 (airline-promo-searcher)

## 触发
用户查询航司/平台优惠、要求批量汇总或指定目标折扣时触发。

## 核心规则
1. 检索仅使用 `WebSearch`；目标清单先尝试执行 `python workspace/skills/airline-promo-searcher/script/sync_airlines_list.py` 刷新。
2. 刷新失败不阻塞任务，继续使用 `workspace/skills/airline-promo-searcher/references/airlines_list.md`。
3. 使用并行 subagents：按“分批”分发任务，不按“单目标”分发。
4. 固定分批策略：总目标按 5 批切分；前 4 批每批 4 个目标，最后 1 批处理剩余目标（如：21 个目标时最后一批 5 个）。
5. 每个 subagent 负责 1 个批次（不是 1 个目标），批内串行检索并产出该批完整结果。
6. 子代理只回传结构化批次结果，禁止写文件；调度主代理统一汇总并写 `workspace/skills/airline-promo-searcher/references/promo_tracking.md`。
7. 任务开始先清空 `promo_tracking.md`；按“批次完成”追加写入，不等待全部批次结束。
8. 每完成一个批次输出一次 heartbeat 进度。

## 目标字段
按 `airlines_list.md` 当前结构读取并校验：
- id
- type
- cheapboat
- name
- cn_name
- keywords
- category
- website

## 检索与判定
1. 查询词基于 `name/cn_name/keywords/website/type/cheapboat` 动态拼接。
2. 单目标默认 1-2 次检索，最多 4 次；优先官网域名词。
3. 查询词必须带当前年份或下一年。
4. 提取字段固定：优惠类型、优惠内容、有效期、来源链接。
5. 过期判定：
- 截止日早于当前日期：已过期（剔除）
- 仅“2025年有效/2025年促销/2025活动”：已过期（剔除）
- 长期有效但无截止日：需人工复核
- 无有效期信息：需人工复核
6. 详情表只写“有效优惠”；复核/过期不写入详情表。
7. 同域名相似结果去重，单目标连续失败 2 次标记待复核。

## 写入规则
1. 写入文件：`workspace/skills/airline-promo-searcher/references/promo_tracking.md`。
2. 主代理维护“已写入批次集合 + 已写入目标集合”，同一批次和同一目标都只允许写一次。
3. 采用“单批次完成即追加”的原子写入，禁止内存累计后一次性写入。
4. 若任务中断，保留已写内容，恢复后从未写入批次继续。
5. 禁止创建 `workspace/skills/airline-promo-searcher/references/airline-promo-*.md`。

## 详情模板
`## 记录模板`
`### 目标名称（中文名 / 英文名）`
`| 优惠类型 | 优惠内容 | 有效期 | 来源链接 |`
`|----------|----------|--------|----------|`
`| 示例 | 示例 | 示例 | 示例 |`

## 最终回传
只返回纯文本 4 行，不加其它段落：
`搜索完成：<已完成数>/<总数>`
`写入文件：workspace/skills/airline-promo-searcher/references/promo_tracking.md`
`有效优惠：<条数>，待复核：<条数>`
`说明：详情已按“记录模板”写入追踪文件`

## 参考资料
- `workspace/skills/airline-promo-searcher/references/airlines_list.md`
- `workspace/skills/airline-promo-searcher/references/promo_tracking.md`
