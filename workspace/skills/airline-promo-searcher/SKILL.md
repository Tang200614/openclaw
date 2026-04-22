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
1. 检索仅使用 `WebSearch`;目标清单先尝试执行 `python workspace/skills/airline-promo-searcher/script/sync_airlines_list.py` 刷新。
2. 刷新失败不阻塞任务，继续使用 `workspace/skills/airline-promo-searcher/script/airlines_data.py`。
3. **不使用子代理**:当前代理直接串行处理所有目标。
4. 每个目标检索完成后立即写入 `promo_tracking.md`,采用"逐条追加"策略。
5. 任务开始先清空 `promo_tracking.md`。
6. 每完成 3-5 个目标输出一次进度。

## 目标字段
按 `airlines_data.py` 当前结构读取并校验:
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
1. 写入文件:`workspace/skills/airline-promo-searcher/references/promo_tracking.md`。
2. 采用"逐目标追加"策略，每个目标完成后立即写入。
3. 维护"已写入目标集合",同一目标只写一次。
4. 若任务中断，保留已写内容，恢复可通过检查已写入目标跳过。
5. 禁止创建 `workspace/skills/airline-promo-searcher/references/airline-promo-*.md`。

## 详情模板
`## 记录模板`
`### 目标名称 (中文名 / 英文名)`
`| 优惠类型 | 优惠内容 | 有效期 | 来源链接 |`
`|----------|----------|--------|----------|`
`| 示例 | 示例 | 示例 | 示例 |`

## 最终回传
完成任务后:
1. 输出汇总信息（已完成数、有效优惠数、待复核数）
2. 在回复末尾添加钉钉文件标记自动上传并发送:
```
[DINGTALK_FILE]{"path":"workspace/skills/airline-promo-searcher/references/promo_tracking.md","fileName":"airline_promo_export.md","fileType":"md"}[/DINGTALK_FILE]
```

## 参考资料
- `workspace/skills/airline-promo-searcher/script/airlines_data.py`
- `workspace/skills/airline-promo-searcher/references/promo_tracking.md`
