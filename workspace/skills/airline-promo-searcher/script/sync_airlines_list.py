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
        "iata_code": code,  # 二字码
        "icao_code": aircode,  # 三字码
        "keywords": keywords,
        "category": "airline",
        "website": website,
    }


def render_python(items):
    """渲染为 Python 文件格式"""
    body = json.dumps(items, ensure_ascii=False, indent=4)
    return (
        '"""航司数据文件\n'
        '包含航空公司列表及搜索匹配逻辑\n'
        '"""\n\n'
        'import re\n\n\n'
        f'AIRLINES = {body}\n\n'
        'AIRLINE_ALIASES = {\n'
        '    "CAL": ["中国航空", "华航", "china airlines"],\n'
        '    "VJC": ["vietjet", "vietjet air", "vj air"],\n'
        '    "CPA": ["cathay", "国泰"],\n'
        '    "EVA": ["eva air", "长荣"],\n'
        '}\n\n'
        'NOISE_TERMS = {\n'
        '    "帮我",\n'
        '    "执行",\n'
        '    "帮我执行",\n'
        '    "优惠搜索",\n'
        '    "搜索优惠",\n'
        '    "优惠",\n'
        '    "搜索",\n'
        '    "查优惠",\n'
        '    "查一下",\n'
        '    "查下",\n'
        '    "查询",\n'
        '    "帮忙",\n'
        '    "一下",\n'
        '    "的",\n'
        '}\n\n\n'
        'def normalize_text(value):\n'
        '    return str(value or "").strip().lower()\n\n\n'
        'def normalize_term(term):\n'
        '    value = normalize_text(term)\n'
        '    value = re.sub(r"[`\'\\\"\u201c\u201d\u2018\u2019\u0028\u0029]+", "", value)\n'
        '    return value.strip()\n\n\n'
        'def split_terms(raw_value):\n'
        '    if raw_value is None:\n'
        '        return []\n'
        '    if isinstance(raw_value, list):\n'
        '        values = raw_value\n'
        '    else:\n'
        '        values = [raw_value]\n'
        '    result = []\n'
        '    for value in values:\n'
        '        text = str(value or "").strip()\n'
        '        if not text:\n'
        '            continue\n'
        '        parts = re.split(r"[,\uff0c\u3001/\\s]+", text)\n'
        '        for part in parts:\n'
        '            normalized = normalize_term(part)\n'
        '            if normalized:\n'
        '                result.append(normalized)\n'
        '            embedded_parts = re.findall(r"[a-zA-Z0-9]{2,}|[\\u4e00-\\u9fff]{2,}", part)\n'
        '            for embedded in embedded_parts:\n'
        '                normalized_embedded = normalize_term(embedded)\n'
        '                if normalized_embedded:\n'
        '                    result.append(normalized_embedded)\n'
        '    return result\n\n\n'
        'def cleanup_terms(terms):\n'
        '    cleaned = []\n'
        '    seen = set()\n'
        '    for term in terms:\n'
        '        normalized = normalize_term(term)\n'
        '        if not normalized or normalized in NOISE_TERMS:\n'
        '            continue\n'
        '        normalized = re.sub(r"(\u7684)?(\u4f18\u60e0|\u641c\u7d22|\u4f18\u60e0\u641c\u7d22|\u4fc3\u9500|\u6298\u6263)+$", "", normalized).strip()\n'
        '        normalized = re.sub(r"^(\u5e2e\u6211|\u8bf7|\u6267\u884c|\u67e5\u8be2|\u67e5\u4e00\u4e0b|\u67e5\u4e0b)+", "", normalized).strip()\n'
        '        if not normalized or normalized in NOISE_TERMS:\n'
        '            continue\n'
        '        if normalized in seen:\n'
        '            continue\n'
        '        seen.add(normalized)\n'
        '        cleaned.append(normalized)\n'
        '    return cleaned\n\n\n'
        'def collect_match_terms(params):\n'
        '    candidate_keys = [\n'
        '        "air_params",\n'
        '        "airline",\n'
        '        "airlines",\n'
        '        "keyword",\n'
        '        "keywords",\n'
        '        "query",\n'
        '        "text",\n'
        '        "content",\n'
        '        "name",\n'
        '        "names",\n'
        '    ]\n'
        '    terms = []\n'
        '    for key in candidate_keys:\n'
        '        terms.extend(split_terms(params.get(key)))\n'
        '    deduped = []\n'
        '    seen = set()\n'
        '    for term in terms:\n'
        '        if term in seen:\n'
        '            continue\n'
        '        seen.add(term)\n'
        '        deduped.append(term)\n'
        '    return cleanup_terms(deduped)\n\n\n'
        'def build_search_tokens(airline):\n'
        '    tokens = {\n'
        '        normalize_text(airline.get("id")),\n'
        '        normalize_text(airline.get("name")),\n'
        '        normalize_text(airline.get("cn_name")),\n'
        '        normalize_text(airline.get("website")),\n'
        '    }\n'
        '    for keyword in airline.get("keywords") or []:\n'
        '        tokens.add(normalize_text(keyword))\n'
        '    for alias in AIRLINE_ALIASES.get(airline.get("name"), []):\n'
        '        tokens.add(normalize_text(alias))\n'
        '    return {token for token in tokens if token}\n\n\n'
        'def is_match(airline, terms):\n'
        '    if not terms:\n'
        '        return False\n'
        '    tokens = build_search_tokens(airline)\n'
        '    for term in terms:\n'
        '        for token in tokens:\n'
        '            if term == token or term in token or token in term:\n'
        '                return True\n'
        '    return False\n\n\n'
        'def main(params: dict):\n'
        '    """入口函数，用于航司匹配搜索"""\n'
        '    params = params or {}\n'
        '    match_terms = collect_match_terms(params)\n'
        '    matched_airlines = [airline for airline in AIRLINES if is_match(airline, match_terms)]\n'
        '    data = matched_airlines if matched_airlines else AIRLINES\n'
        '    return {\n'
        '        "success": True,\n'
        '        "matched": bool(matched_airlines),\n'
        '        "match_terms": match_terms,\n'
        '        "total": len(data),\n'
        '        "data": data,\n'
        '    }\n'
    )


def main():
    script_dir = Path(__file__).resolve().parent
    target_file = script_dir / "airlines_data.py"
    api_items = fetch_airline_data(SOURCE_URL)
    airlines = [
        build_airline_item(raw, idx + 1)
        for idx, raw in enumerate(api_items)
    ]
    target_file.write_text(render_python(airlines), encoding="utf-8")
    print(f"同步完成：airlines={len(airlines)}, platforms=0, total={len(airlines)}")
    print(f"输出文件：{target_file}")


if __name__ == "__main__":
    main()
