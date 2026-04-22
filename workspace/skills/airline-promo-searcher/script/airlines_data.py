"""航司数据文件
包含航空公司列表及搜索匹配逻辑
"""

import re


AIRLINES = [
    {
        "id": 1,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "CEB",
        "cn_name": "宿雾航空",
        "keywords": ["CEB", "宿雾航空", "5J"],
        "category": "airline",
        "website": "https://www.cebu-pacific.com/",
    },
    {
        "id": 2,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "IGO",
        "cn_name": "靛蓝航空",
        "keywords": ["IGO", "靛蓝航空", "6E"],
        "category": "airline",
        "website": "https://www.goindigo.in/",
    },
    {
        "id": 3,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "AXM",
        "cn_name": "亚洲亚航",
        "keywords": ["AXM", "亚洲亚航", "AK"],
        "category": "airline",
        "website": "https://www.airasia.com/",
    },
    {
        "id": 4,
        "type": "国际",
        "cheapboat": "FSC",
        "name": "EVA",
        "cn_name": "长荣航空",
        "keywords": ["EVA", "长荣航空", "BR"],
        "category": "airline",
        "website": "https://www.evaair.com/",
    },
    {
        "id": 5,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "CAL",
        "cn_name": "中华航空",
        "keywords": ["CAL", "中华航空", "CI"],
        "category": "airline",
        "website": "https://www.china-airlines.com/",
    },
    {
        "id": 6,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "CPA",
        "cn_name": "国泰航空",
        "keywords": ["CPA", "国泰航空", "CX"],
        "category": "airline",
        "website": "https://www.cathaypacific.com/",
    },
    {
        "id": 7,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "UAE",
        "cn_name": "阿联酋航",
        "keywords": ["UAE", "阿联酋航", "EK"],
        "category": "airline",
        "website": "https://www.emirates.com/",
    },
    {
        "id": 8,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "FRE",
        "cn_name": "福莱尔航空",
        "keywords": ["FRE", "福莱尔航空", "F8"],
        "category": "airline",
        "website": "https://flyflair.com/",
    },
    {
        "id": 9,
        "type": "国际",
        "cheapboat": "FSC",
        "name": "JAL",
        "cn_name": "日本航空",
        "keywords": ["JAL", "日本航空", "JL"],
        "category": "airline",
        "website": "https://www.jal.co.jp/",
    },
    {
        "id": 10,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "KAL",
        "cn_name": "大韩航空",
        "keywords": ["KAL", "大韩航空", "KE"],
        "category": "airline",
        "website": "https://www.koreanair.com/",
    },
    {
        "id": 11,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "ANA",
        "cn_name": "全日空",
        "keywords": ["ANA", "全日空", "NH"],
        "category": "airline",
        "website": "https://www.ana.co.jp/",
    },
    {
        "id": 12,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "NKS",
        "cn_name": "精神航空",
        "keywords": ["NKS", "精神航空", "NK"],
        "category": "airline",
        "website": "https://www.spirit.com/",
    },
    {
        "id": 13,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "QTR",
        "cn_name": "卡塔尔航空",
        "keywords": ["QTR", "卡塔尔航空", "QR"],
        "category": "airline",
        "website": "https://www.qatarairways.com/",
    },
    {
        "id": 14,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "TLM",
        "cn_name": "狮航",
        "keywords": ["TLM", "狮航", "SL"],
        "category": "airline",
        "website": "https://www.lionairthai.com/",
    },
    {
        "id": 15,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "SIA",
        "cn_name": "新加坡航",
        "keywords": ["SIA", "新加坡航", "SQ"],
        "category": "airline",
        "website": "https://www.singaporeair.com/",
    },
    {
        "id": 16,
        "type": "国际",
        "cheapboat": "FSC",
        "name": "THY",
        "cn_name": "土耳其航",
        "keywords": ["THY", "土耳其航", "TK"],
        "category": "airline",
        "website": "https://www.turkishairlines.com/",
    },
    {
        "id": 17,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "HKE",
        "cn_name": "香港快运航空公司",
        "keywords": ["HKE", "香港快运航空公司", "UO"],
        "category": "airline",
        "website": "https://www.hkexpress.com/",
    },
    {
        "id": 18,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "VJC",
        "cn_name": "越捷航空",
        "keywords": ["VJC", "越捷航空", "VJ"],
        "category": "airline",
        "website": "https://www.vietjetair.com/",
    },
    {
        "id": 19,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "HVN",
        "cn_name": "越南航空",
        "keywords": ["HVN", "越南航空", "VN"],
        "category": "airline",
        "website": "https://www.vietnamairlines.com/",
    },
    {
        "id": 20,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "WZZ",
        "cn_name": "维兹航空",
        "keywords": ["WZZ", "维兹航空", "W6"],
        "category": "airline",
        "website": "https://wizzair.com/",
    },
    {
        "id": 21,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "VOI",
        "cn_name": "墨西哥 VOLARIS",
        "keywords": ["VOI", "墨西哥 VOLARIS", "Y4"],
        "category": "airline",
        "website": "https://www.volaris.com/",
    },
]

AIRLINE_ALIASES = {
    "CAL": ["中国航空", "华航", "china airlines"],
    "VJC": ["vietjet", "vietjet air", "vj air"],
    "CPA": ["cathay", "国泰"],
    "EVA": ["eva air", "长荣"],
}

NOISE_TERMS = {
    "帮我",
    "执行",
    "帮我执行",
    "优惠搜索",
    "搜索优惠",
    "优惠",
    "搜索",
    "查优惠",
    "查一下",
    "查下",
    "查询",
    "帮忙",
    "一下",
    "的",
}


def normalize_text(value):
    return str(value or "").strip().lower()


def normalize_term(term):
    value = normalize_text(term)
    value = re.sub(r"[`'\"""''""()]+", "", value)
    return value.strip()


def split_terms(raw_value):
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        values = raw_value
    else:
        values = [raw_value]
    result = []
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        parts = re.split(r"[,，、/\s]+", text)
        for part in parts:
            normalized = normalize_term(part)
            if normalized:
                result.append(normalized)
            # 从自然语言里额外抽取英文代码和中文短语
            embedded_parts = re.findall(r"[a-zA-Z0-9]{2,}|[\u4e00-\u9fff]{2,}", part)
            for embedded in embedded_parts:
                normalized_embedded = normalize_term(embedded)
                if normalized_embedded:
                    result.append(normalized_embedded)
    return result


def cleanup_terms(terms):
    cleaned = []
    seen = set()
    for term in terms:
        normalized = normalize_term(term)
        if not normalized or normalized in NOISE_TERMS:
            continue
        # 去掉句尾动作词，让"中国航空的优惠搜索"变成"中国航空"
        normalized = re.sub(r"(的)?(优惠 | 搜索 | 优惠搜索 | 促销 | 折扣)+$", "", normalized).strip()
        normalized = re.sub(r"^(帮我 | 请 | 执行 | 查询 | 查一下 | 查下)+", "", normalized).strip()
        if not normalized or normalized in NOISE_TERMS:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        cleaned.append(normalized)
    return cleaned


def collect_match_terms(params):
    candidate_keys = [
        "air_params",
        "airline",
        "airlines",
        "keyword",
        "keywords",
        "query",
        "text",
        "content",
        "name",
        "names",
    ]
    terms = []
    for key in candidate_keys:
        terms.extend(split_terms(params.get(key)))
    deduped = []
    seen = set()
    for term in terms:
        if term in seen:
            continue
        seen.add(term)
        deduped.append(term)
    return cleanup_terms(deduped)


def build_search_tokens(airline):
    tokens = {
        normalize_text(airline.get("id")),
        normalize_text(airline.get("name")),
        normalize_text(airline.get("cn_name")),
        normalize_text(airline.get("website")),
    }
    for keyword in airline.get("keywords") or []:
        tokens.add(normalize_text(keyword))
    for alias in AIRLINE_ALIASES.get(airline.get("name"), []):
        tokens.add(normalize_text(alias))
    return {token for token in tokens if token}


def is_match(airline, terms):
    if not terms:
        return False
    tokens = build_search_tokens(airline)
    for term in terms:
        for token in tokens:
            if term == token or term in token or token in term:
                return True
    return False


def main(params: dict):
    """入口函数，用于航司匹配搜索
    函数的返回值将作为结果填入字段中"""
    params = params or {}
    match_terms = collect_match_terms(params)
    matched_airlines = [airline for airline in AIRLINES if is_match(airline, match_terms)]
    data = matched_airlines if matched_airlines else AIRLINES

    return {
        "success": True,
        "matched": bool(matched_airlines),
        "match_terms": match_terms,
        "total": len(data),
        "data": data,
    }
