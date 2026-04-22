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
1. 检索仅使用 `WebSearch`
2. 航司数据获取：`python script/fetch_airlines.py`（接口 + 静态兜底）
3. 优惠数据保存：`python script/save_promos.py`（写入 promo_data.json → POST 到后端）
4. **不使用子代理**:当前代理直接串行处理所有目标。
5. 每个目标检索完成后立即写入 `promo_data.json`,采用"逐条追加"策略。
6. 任务开始先清空 `promo_data.json` 的优惠记录。
7. 每完成 3-5 个目标输出一次进度。

## 数据格式规范
### belong 字段格式
- **格式要求**：仅使用国家/地区二字码，如 `CN`、`US`、`QA`、`TW`
- **禁止格式**：不得使用 `CN(中国)`、`US(美国)` 等带括号的完整格式
- **来源**：从 `fetch_airlines.py` 的航司数据中自动获取

### JSON 导入格式
批量导入时使用的 JSON 格式：
```json
[
  {
    "airline_name": "航司名称",
    "airline_iata_code": "二字码",
    "airline_icao_code": "三字码",
    "belong": "CN",
    "promo_type": "优惠类型",
    "promo_content": "优惠内容详情",
    "promo_start_date": "2026-01-01",
    "promo_end_date": "2026-12-31",
    "source_url": "https://example.com"
  }
]
```

## 检索与判定
1. 查询词基于航司名称、二字码、三字码、官网域名动态拼接。
2. 单目标默认 1-2 次检索，最多 4 次;优先官网域名词。
3. 查询词必须带当前年份或下一年。
4. 提取字段固定：优惠类型、优惠内容、有效期、来源链接。
5. 仅记录有明确优惠信息的条目，无优惠/无法访问的航司不记录。
6. 同域名相似结果去重。

## 写入规则
1. 写入文件：`workspace/skills/airline-promo-searcher/references/promo_data.json`。
2. 采用"逐条追加"策略，每个目标完成后立即写入 JSON 文件。
3. 维护"已写入 URL+ 优惠类型集合",同一优惠不重复写入。
4. 若任务中断，保留已写内容，恢复可通过检查已写入记录跳过。
5. **belong 字段**：写入时需从航司数据中获取对应的国家/地区二字码
6. **文件格式**：标准 JSON 格式，包含 `updated_at` 和 `promos` 数组

## 详情模板

### 目标名称 (中文名 / 英文名)

JSON 记录格式：
```json
{
  "airline_name": "航司名称",
  "airline_iata_code": "BR",
  "airline_icao_code": "EVA",
  "belong": "TW",
  "promo_type": "限时折扣",
  "promo_content": "机票 8 折起",
  "promo_start_date": "2026-04-01",
  "promo_end_date": "2026-06-30",
  "source_url": "https://example.com"
}
```

## 最终回传
完成任务后:
1. 输出汇总信息（已完成数、有效优惠数）
2. 在回复末尾添加钉钉文件标记自动上传并发送:
```
[DINGTALK_FILE]{"path":"workspace/skills/airline-promo-searcher/references/promo_data.json","fileName":"airline_promo_data.json","fileType":"json"}[/DINGTALK_FILE]
```

## 参考资料
- `script/fetch_airlines.py` - 获取航司数据（接口 + 静态兜底）
- `script/save_promos.py` - 保存优惠数据到后端（写入 JSON + POST）
- `script/test_upload.py` - 测试上传脚本（读取 promo_import_example.json）
- `references/promo_data.json` - 优惠数据存储（JSON 格式）
