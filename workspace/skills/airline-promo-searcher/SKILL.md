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

## 执行总则

1. 仅使用 `WebSearch` 执行检索；目标清单同步阶段允许直接请求航司接口。
2. 先请求 `http://192.168.1.173:7001/servlet/ServiceServlet?method=getAirCompanyList&type=1` 同步航司基准，再从 `workspace/skills/airline-promo-searcher/references/airlines_list.md` 读取目标清单并**按批次串行执行**（避免 LLM 空闲超时）。
3. 写入 `workspace/skills/airline-promo-searcher/references/promo_tracking.md` 时，任务开始先清空旧内容。
4. **每完成一批次就立即追加写入一次**，不得等全部目标完成后再统一写入。
5. 每完成一批次立即输出进度，避免触发 60 秒空闲超时。
6. 最终回复必须是固定模板的纯文本，不输出航司/平台长列表。

## 触发规则

当用户表达以下意图时触发：

1. 查询航司优惠或平台优惠
2. 生成优惠汇总
3. 查询特定航司或平台折扣

## 核心职责

1. 基于“接口同步后的统一目标列表”执行优惠检索。
2. 每个目标默认执行 1-2 次检索，命中不足时再扩展到 3-4 次。
3. 仅保留当前有效或有效期明确的优惠信息。
4. 输出到单一追踪文件 `workspace/skills/airline-promo-searcher/references/promo_tracking.md`。
5. 不创建按日期命名的新报告文件。

## 输出要求

1. 文档中必须包含汇总信息（目标总数、更新日期、搜索工具、写入策略）。
2. 文档中必须包含 `## 目标详情` 段，并覆盖本轮应检索的全部目标。
3. 每个目标详情必须使用以下固定模板：
   `## 记录模板`
   `### 目标名称（中文名 / 英文名）`
   `| 优惠类型 | 优惠内容 | 有效期 | 来源链接 |`
   `|----------|----------|--------|----------|`
   `| 示例 | 示例 | 示例 | 示例 |`
4. 来源链接必须可追溯，无法确认时标记为"需人工复核"。
5. 不允许把详情改写成“按编号罗列一句话”的清单式输出。
6. 发送给用户时返回固定模板纯文本，不输出 Markdown 标记。

## 工作流程

### 步骤 1：同步并读取目标列表

1. 先请求 `http://192.168.1.173:7001/servlet/ServiceServlet?method=getAirCompanyList&type=1` 获取航司列表。
2. 以接口返回为航司基准，更新 `workspace/skills/airline-promo-searcher/references/airlines_list.md` 后再读取字段。
3. 若接口不可用，保留现有 `workspace/skills/airline-promo-searcher/references/airlines_list.md` 继续执行，并在结果中标记“航司基准未刷新”。
4. 保存后的目标字段按当前清单结构识别：
- id
- type
- cheapboat
- name
- cn_name
- keywords
- category
- website
5. 字段以 `airlines_list.md` 当前结构为准，不做额外重命名。

### 步骤 2：构造 WebSearch 查询

1. 以目标 `name`、`cn_name`、`keywords`、`website`、`type`、`cheapboat` 动态拼接查询词。
2. 单目标默认查询 1-2 次，最多不超过 4 次。
3. 查询优先级：官网域名词 > 优惠词 > 年份词。
4. 推荐组合：`name + promo/deal`、`cn_name + 促销/特价`、`name + cheapboat + promotion`、`name + type + deal`、`官网域名 + offers`。

### 步骤 3：执行搜索与提取（关键：避免超时）

1. 采用串行批次执行，不并行启动子代理。
2. 每批处理 4-5 个目标，按目标总数动态分批。
3. 每批内逐个目标检索并提取：优惠类型、优惠内容、有效期、来源链接。
4. 同域名相似结果去重，仅保留可验证来源。
5. 单目标连续失败 2 次，标记为“待复核”，继续下一个目标。
6. 每批完成后立即输出 heartbeat 进度，再启动下一批。

### 步骤 4：分批追加写入追踪文件

写入 `workspace/skills/airline-promo-searcher/references/promo_tracking.md` 规则：
1. 任务开始先清空旧内容，并写入本轮汇总头部。
2. 每完成一批次立即追加写入，不等待全量完成。
3. 每次写入都必须包含状态总表与详情模板（固定为“记录模板”）：
 `## 记录模板`
   `### 目标名称（中文名 / 英文名）`
   `| 优惠类型 | 优惠内容 | 有效期 | 来源链接 |`
   `|----------|----------|--------|----------|`
   `| 示例 | 示例 | 示例 | 示例 |`
4. 禁止在内存中累计后一次性写入。

### 步骤 5：回传固定格式纯文本

1. 严格使用以下 4 行模板回传，不得添加额外段落：
   `搜索完成：<已完成数>/<总数>`
   `写入文件：workspace/skills/airline-promo-searcher/references/promo_tracking.md`
   `有效优惠：<条数>，待复核：<条数>`
   `说明：详情已按“记录模板”写入追踪文件`
2. 禁止回传“航司核心优惠/平台核心优惠/1-34 编号列表”这类长摘要。
3. 仅返回纯文本，不包含 Markdown 格式。

## 注意事项

1. 目标清单字段以当前文件结构为准：`id/type/cheapboat/name/cn_name/keywords/category/website`。
2. 目标清单字段校验必须通过：每条记录都包含上述 8 个字段，缺失则标记“待复核”并继续后续目标。
3. 优先使用官网、航司新闻室、官方社媒、可信平台。
4. 仅保留当前有效或有效期明确的优惠；无法确认时标记“需人工复核”。
5. 必须写入 `workspace/skills/airline-promo-searcher/references/promo_tracking.md`，禁止创建 `workspace/skills/airline-promo-searcher/references/airline-promo-*.md`。
6. 仅使用 `WebSearch`；每批次完成后必须输出 heartbeat 进度，避免空闲超时。
7. 若 `WebSearch` 不可用，输出“本轮检索受限”并保留可验证来源。
8. 结果展示优先级固定：先写文件模板，再回传 4 行摘要；不得输出自由发挥的长文本。
9. 统一执行“先清空 + 分批追加”的单一路径，不使用续写模式分支。

## 参考资料

- `workspace/skills/airline-promo-searcher/references/airlines_list.md`
- `workspace/skills/airline-promo-searcher/references/promo_tracking.md`
