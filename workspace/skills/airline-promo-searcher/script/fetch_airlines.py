"""获取航司数据模块
- 优先从接口获取
- 接口失败则用静态 AIRLINES 兜底
"""

import json
import urllib.request

# 航司数据接口
AIRLINE_LIST_URL = "http://ht.piaomou.com/servlet/ServiceServlet?method=getAirCompanyList&type=1"

# 静态航司数据（兜底用）
AIRLINES = [
    {
        "id": 1,
        "type": "国际",
        "cheapboat": "LCC",
        "name": "CEB",
        "cn_name": "宿雾航空",
        "iata_code": "5J",
        "icao_code": "CEB",
        "belong": "PH(菲律宾)",
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
        "iata_code": "6E",
        "icao_code": "IGO",
        "belong": "IN(印度)",
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
        "iata_code": "AK",
        "icao_code": "AXM",
        "belong": "MY(马来西亚)",
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
        "iata_code": "BR",
        "icao_code": "EVA",
        "belong": "TW(台湾)",
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
        "iata_code": "CI",
        "icao_code": "CAL",
        "belong": "TW(台湾)",
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
        "iata_code": "CX",
        "icao_code": "CPA",
        "belong": "HK(香港)",
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
        "iata_code": "EK",
        "icao_code": "UAE",
        "belong": "AE(阿联酋)",
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
        "iata_code": "F8",
        "icao_code": "FRE",
        "belong": "ES(西班牙)",
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
        "iata_code": "JL",
        "icao_code": "JAL",
        "belong": "JP(日本)",
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
        "iata_code": "KE",
        "icao_code": "KAL",
        "belong": "KR(韩国)",
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
        "iata_code": "NH",
        "icao_code": "ANA",
        "belong": "JP(日本)",
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
        "iata_code": "NK",
        "icao_code": "NKS",
        "belong": "US(美国)",
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
        "iata_code": "QR",
        "icao_code": "QTR",
        "belong": "QA(卡塔尔)",
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
        "iata_code": "SL",
        "icao_code": "TLM",
        "belong": "TH(泰国)",
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
        "iata_code": "SQ",
        "icao_code": "SIA",
        "belong": "SG(新加坡)",
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
        "iata_code": "TK",
        "icao_code": "THY",
        "belong": "TR(土耳其)",
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
        "iata_code": "UO",
        "icao_code": "HKE",
        "belong": "HK(香港)",
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
        "iata_code": "VJ",
        "icao_code": "VJC",
        "belong": "VN(越南)",
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
        "iata_code": "VN",
        "icao_code": "HVN",
        "belong": "VN(越南)",
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
        "iata_code": "W6",
        "icao_code": "WZZ",
        "belong": "US(美国)",
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
        "iata_code": "Y4",
        "icao_code": "VOI",
        "belong": "MX(墨西哥)",
        "keywords": ["VOI", "墨西哥 VOLARIS", "Y4"],
        "category": "airline",
        "website": "https://www.volaris.com/",
    },
]


def fetch_from_api():
    """从接口获取航司数据"""
    try:
        with urllib.request.urlopen(AIRLINE_LIST_URL, timeout=10) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            content = response.read().decode(charset, errors="replace")
        result = json.loads(content)
        if isinstance(result, list):
            return result
        return None
    except Exception:
        return None


def get_airlines():
    """获取航司列表（优先接口，失败则用静态数据兜底）"""
    airlines = fetch_from_api()
    if airlines:
        return airlines
    return AIRLINES


def get_airline_by_code(code: str):
    """按二字码/三字码查询航司"""
    airlines = get_airlines()
    for a in airlines:
        if a.get("iata_code") == code or a.get("icao_code") == code:
            return a
    return None


def get_airline_by_name(name: str):
    """按名称查询航司"""
    airlines = get_airlines()
    name = name.lower()
    for a in airlines:
        if (name in a.get("cn_name", "").lower() or
            name in a.get("name", "").lower()):
            return a
    return None


def search_airlines(keyword: str):
    """按关键词搜索航司"""
    airlines = get_airlines()
    keyword = keyword.lower()
    results = []
    for a in airlines:
        if (keyword in a.get("cn_name", "").lower() or
            keyword in a.get("name", "").lower() or
            keyword in a.get("iata_code", "").lower() or
            keyword in a.get("icao_code", "").lower()):
            results.append(a)
    return results


def main(params: dict = None):
    """
    入口函数：
    - params=None → 返回所有航司
    - params={query} → 搜索匹配的航司
    """
    if params is None:
        return get_airlines()

    # 搜索逻辑
    keyword = params.get("keyword") or params.get("name")
    if keyword:
        results = search_airlines(str(keyword))
        return {
            "success": True,
            "matched": len(results) > 0,
            "total": len(results),
            "data": results,
        }

    return get_airlines()


if __name__ == "__main__":
    # 测试
    print("=== 测试航司数据获取 ===")

    # 测试 1: 获取全部
    airlines = get_airlines()
    print(f"\n1. 获取全部航司：{len(airlines)} 家")

    # 测试 2: 按代码查询
    airline = get_airline_by_code("VN")
    print(f"\n2. 查询 VN: {airline}")

    # 测试 3: 按名称查询
    airline = get_airline_by_name("越南")
    print(f"\n3. 查询'越南': {airline}")

    # 测试 4: 搜索
    results = search_airlines("航空")
    print(f"\n4. 搜索'航空': {len(results)} 条结果")
