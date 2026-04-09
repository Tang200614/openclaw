import json
from pathlib import Path
from urllib.request import urlopen


SOURCE_URL = "http://192.168.1.173:7001/servlet/ServiceServlet?method=getAirCompanyList&type=1"


def normalize_url(raw: str) -> str:
    value = (raw or "").strip().strip("`").strip().strip('"').strip("'")
    if not value:
        return ""
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def fetch_airline_data(url: str):
    with urlopen(url, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        content = response.read().decode(charset, errors="replace")
    payload = json.loads(content)
    if not isinstance(payload, list):
        raise ValueError("接口返回不是数组")
    return payload


def build_airline_item(raw_item: dict, index: int):
    website = normalize_url(raw_item.get("URL", ""))
    item_type = (raw_item.get("TYPE") or "").strip()
    cheapboat = (raw_item.get("CHEAPBOAT") or "").strip()
    cn_name = (raw_item.get("SHORTNAME") or "").strip()
    code = (raw_item.get("CODE") or "").strip()
    aircode = (raw_item.get("AIRCODE") or "").strip()
    name = aircode or code or cn_name
    keyword_candidates = [
        name,
        cn_name,
        code,
        aircode,
    ]
    keywords = []
    seen = set()
    for kw in keyword_candidates:
        k = (kw or "").strip()
        if not k:
            continue
        lower_k = k.lower()
        if lower_k in seen:
            continue
        seen.add(lower_k)
        keywords.append(k)
    return {
        "id": index,
        "type": item_type,
        "cheapboat": cheapboat,
        "name": name,
        "cn_name": cn_name or name,
        "keywords": keywords,
        "category": "airline",
        "website": website,
    }


def render_markdown(items):
    airline_count = sum(1 for x in items if x.get("category") == "airline")
    body = json.dumps(items, ensure_ascii=False, indent=2)
    return (
        "# 搜索目标列表配置\n\n"
        "## 使用说明\n\n"
        "- 本文件维护统一的搜索目标列表，采用连续编号结构。\n"
        "- 全部条目来自航司接口同步结果。\n"
        f"- 航司接口: `{SOURCE_URL}`\n"
        f"- 执行时按 `id` 顺序从 1 到 {airline_count} 依次搜索。\n"
        "- `category` 固定为 `airline`。\n\n"
        "```json\n"
        f"{body}\n"
        "```\n\n"
        "## 统计\n\n"
        f"- 搜索目标总数: {airline_count}\n"
        f"- 航空公司: {airline_count}\n"
        "- 订票平台: 0\n"
    )


def main():
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / "references" / "airlines_list.md",
        script_dir.parent / "references" / "airlines_list.md",
    ]
    target_file = next((p for p in candidates if p.exists()), candidates[-1])
    api_items = fetch_airline_data(SOURCE_URL)
    airlines = [
        build_airline_item(raw, idx + 1)
        for idx, raw in enumerate(api_items)
    ]
    target_file.write_text(render_markdown(airlines), encoding="utf-8")
    print(f"同步完成: airlines={len(airlines)}, platforms=0, total={len(airlines)}")
    print(f"输出文件: {target_file}")


if __name__ == "__main__":
    main()
