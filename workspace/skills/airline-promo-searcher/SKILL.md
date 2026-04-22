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
当用户表达以下意图时触发：
1. **航司优惠搜索**：如"航司优惠搜索"、"搜索航司优惠"、"查航司促销"
2. **指定航司查询**：如"查南航优惠"、"看看亚航有什么折扣"
3. **批量汇总需求**：如"汇总所有航司优惠"、"整理廉航促销信息"
4. **机票折扣查询**：如"近期机票优惠"、"2026 年机票促销"

关键词匹配：航司、航空、机票、优惠、促销、折扣、LCC、廉航

## 核心规则
1. 检索仅使用 `WebSearch`;目标清单先尝试执行 `python workspace/skills/airline-promo-searcher/script/sync_airlines_list.py` 刷新。
2. 刷新失败不阻塞任务，继续使用 `workspace/skills/airline-promo-searcher/script/airlines_data.py`。
3. **不使用子代理**:当前代理直接串行处理所有目标。
4. 每个目标检索完成后立即写入 `promo_data.md`,采用"逐条追加"策略。
5. 任务开始先清空 `promo_data.md` 的优惠记录表。
6. 每完成 3-5 个目标输出一次进度。

## 目标字段
按 `airlines_data.py` 当前结构读取并校验:
- id
- type
- cheapboat
- name (三字码/ICAO 代码)
- cn_name (中文名称)
- iata_code (二字码)
- icao_code (三字码)
- keywords
- category
- website

## 检索与判定
1. 查询词基于 `name/cn_name/keywords/website/type/cheapboat` 动态拼接。
2. 单目标默认 1-2 次检索，最多 4 次;优先官网域名词。
3. 查询词必须带当前年份或下一年。
4. 提取字段固定：优惠类型、优惠内容、有效期、来源链接。
5. 过期判定:
- 截止日早于当前日期：已过期 (剔除)
- 仅"2025年有效/2025年促销/2025活动":已过期 (剔除)
- 长期有效但无截止日：需人工复核
- 无有效期信息：需人工复核
6. 详情表只写"有效优惠";复核/过期不写入详情表。
7. 同域名相似结果去重，单目标连续失败 2 次标记待复核。

## 写入规则
1. 写入文件:`workspace/skills/airline-promo-searcher/references/promo_data.md`。
2. 采用"逐条追加"策略，每个目标完成后立即写入表格。
3. 维护"已写入目标集合",同一目标只写一次。
4. 若任务中断，保留已写内容，恢复可通过检查已写入目标跳过。

## 详情模板
`## 记录模板`
`### 目标名称 (中文名 / 英文名)`
`| 航司 | 二字码 | 三字码 | 优惠类型 | 优惠内容 | 有效期 | 来源链接 | 状态 |`
`|----------|----------|----------|----------|----------|--------|----------|------|`
`| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | ✅ 有效 |`

## 最终回传
完成任务后:
1. 输出汇总信息（已完成数、有效优惠数、待复核数）
2. 在回复末尾添加钉钉文件标记自动上传并发送:
```
[DINGTALK_FILE]{"path":"workspace/skills/airline-promo-searcher/references/promo_data.md","fileName":"airline_promo_data.md","fileType":"md"}[/DINGTALK_FILE]
```

## 参考资料
- `workspace/skills/airline-promo-searcher/script/airlines_data.py`
- `workspace/skills/airline-promo-searcher/references/promo_data.md`
