---
name: airline-promo-searcher
description: 深度搜索 34 个目标（21 家航空公司 + 13 个订票平台）的最新优惠政策并输出追踪结果
metadata:
  {
    "openclaw":
      {
        "emoji": "✈️",
        "requires": { "anyBins": ["python3", "python"] },
      },
  }
---

# 航空优惠深度搜索技能 (airline-promo-searcher)

## 执行总则

1. 使用 `web_search` 执行检索，不运行脚本。
2. 从 `references/airlines_list.md` 读取目标清单。
3. 按编号顺序对 34 个目标逐个搜索。
4. 将完整结果覆盖写入 `references/promo_tracking.md`。
5. 返回简洁纯文本摘要。

## 触发规则

当用户表达以下意图时触发：

1. 查询航司优惠或平台优惠
2. 生成优惠汇总
3. 查询特定航司或平台折扣

## 核心职责

1. 读取并使用统一搜索列表，按编号顺序执行。
2. 每个目标执行 3-6 次搜索，优先官网和权威来源。
3. 提取当前有效优惠，优先当前年，其次下一年。
4. 输出到单一追踪文件 `references/promo_tracking.md`。
5. 不创建按日期命名的新报告文件。

## 输出要求

1. 文档中必须包含汇总信息（目标总数、更新日期、搜索工具、写入策略）。
2. 文档中必须包含 34 个目标的状态或结果。
3. 每个目标的优惠信息表头固定为：`| 优惠类型 | 优惠内容 | 有效期 | 来源链接 |`
4. 每个目标必须包含官网链接。
5. 发送给用户时返回纯文本摘要，不输出 Markdown 标记。

## 工作流程

### 步骤 1：读取目标列表

从 `references/airlines_list.md` 读取以下字段：
- id
- name
- cn_name
- keywords
- category
- website

### 步骤 2：生成搜索查询

```python
SEARCH_TEMPLATES = [
    "{name} {target_year} promo code discount",
    "{cn_name} {target_year} 促销 优惠 特价机票",
    "{name} {target_year} special fare deal",
    "{name} {target_year} coupon sale",
]
```

### 步骤 3：执行搜索与提取

1. 每个目标执行多关键词搜索。
2. 去除过期或无明确信息的结果。
3. 提取优惠类型、优惠内容、有效期、来源链接。

### 步骤 4：覆盖写入追踪文件

默认覆盖写入 `references/promo_tracking.md`：
1. 未显式指定时，清空旧内容后写入本轮结果。
2. 仅当用户明确要求“补充/续写/追加”时，使用续写模式。

### 步骤 5：回传纯文本摘要

1. 汇总总目标数和完成情况。
2. 列出重点发现。
3. 给出追踪文件路径。

## 注意事项

1. 优先使用官网、航司新闻室、官方社媒、可信平台。
2. 仅保留当前有效或明确有效期的优惠。
3. 必须写入 `references/promo_tracking.md`。
4. 禁止创建 `references/airline-promo-*.md` 文件。

## 参考资料

- `references/airlines_list.md`
- `references/promo_tracking.md`
