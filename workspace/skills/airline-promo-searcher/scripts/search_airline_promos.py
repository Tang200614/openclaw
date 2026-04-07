#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航空优惠搜索脚本（无分级版本）
"""

import os
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

TRACKING_FILE_REL = "references/promo_tracking.md"

TARGETS = [
    {"id": 1, "name": "Thai Lion Air", "cn_name": "泰国狮航", "keywords": ["Thai Lion Air", "泰国狮航", "泰狮航"], "category": "airline", "website": "https://www.lionairthai.com/"},
    {"id": 2, "name": "Cebu Pacific", "cn_name": "宿务航空", "keywords": ["Cebu Pacific", "宿务航空", "宿雾航空"], "category": "airline", "website": "https://www.cebu-pacific.com/"},
    {"id": 3, "name": "IndiGo", "cn_name": "靛蓝航空", "keywords": ["IndiGo", "靛蓝航空", "印地高航空"], "category": "airline", "website": "https://www.goindigo.in/"},
    {"id": 4, "name": "HK Express", "cn_name": "香港快运", "keywords": ["HK Express", "香港快运"], "category": "airline", "website": "https://www.hkexpress.com/"},
    {"id": 5, "name": "VietJet Air", "cn_name": "越捷航空", "keywords": ["VietJet Air", "越捷航空", "Thai VietJet"], "category": "airline", "website": "https://www.vietjetair.com/"},
    {"id": 6, "name": "AirAsia", "cn_name": "亚洲航空", "keywords": ["AirAsia", "亚航", "亚洲航空"], "category": "airline", "website": "https://www.airasia.com/"},
    {"id": 7, "name": "Emirates", "cn_name": "阿联酋航空", "keywords": ["Emirates", "阿联酋航空"], "category": "airline", "website": "https://www.emirates.com/"},
    {"id": 8, "name": "Qatar Airways", "cn_name": "卡塔尔航空", "keywords": ["Qatar Airways", "卡塔尔航空"], "category": "airline", "website": "https://www.qatarairways.com/"},
    {"id": 9, "name": "Turkish Airlines", "cn_name": "土耳其航空", "keywords": ["Turkish Airlines", "土耳其航空"], "category": "airline", "website": "https://www.turkishairlines.com/"},
    {"id": 10, "name": "EVA Air", "cn_name": "长荣航空", "keywords": ["EVA Air", "长荣航空"], "category": "airline", "website": "https://www.evaair.com/"},
    {"id": 11, "name": "China Airlines", "cn_name": "中华航空", "keywords": ["China Airlines", "中华航空", "华航"], "category": "airline", "website": "https://www.china-airlines.com/"},
    {"id": 12, "name": "Vietnam Airlines", "cn_name": "越南航空", "keywords": ["Vietnam Airlines", "越南航空"], "category": "airline", "website": "https://www.vietnamairlines.com/"},
    {"id": 13, "name": "Singapore Airlines", "cn_name": "新加坡航空", "keywords": ["Singapore Airlines", "新航", "新加坡航空"], "category": "airline", "website": "https://www.singaporeair.com/"},
    {"id": 14, "name": "Cathay Pacific", "cn_name": "国泰航空", "keywords": ["Cathay Pacific", "国泰航空"], "category": "airline", "website": "https://www.cathaypacific.com/"},
    {"id": 15, "name": "Japan Airlines", "cn_name": "日本航空", "keywords": ["JAL", "日本航空", "Japan Airlines"], "category": "airline", "website": "https://www.jal.co.jp/"},
    {"id": 16, "name": "ANA", "cn_name": "全日空", "keywords": ["ANA", "全日空"], "category": "airline", "website": "https://www.ana.co.jp/"},
    {"id": 17, "name": "Korean Air", "cn_name": "大韩航空", "keywords": ["Korean Air", "大韩航空"], "category": "airline", "website": "https://www.koreanair.com/"},
    {"id": 18, "name": "Flair Airlines", "cn_name": "弗莱尔航空", "keywords": ["Flair Airlines", "弗莱尔航空"], "category": "airline", "website": "https://flyflair.com/"},
    {"id": 19, "name": "Wizz Air", "cn_name": "威兹航空", "keywords": ["Wizz Air", "威兹航空"], "category": "airline", "website": "https://wizzair.com/"},
    {"id": 20, "name": "Spirit Airlines", "cn_name": "精神航空", "keywords": ["Spirit Airlines", "精神航空"], "category": "airline", "website": "https://www.spirit.com/"},
    {"id": 21, "name": "Volaris", "cn_name": "沃拉里斯航空", "keywords": ["Volaris", "沃拉里斯航空"], "category": "airline", "website": "https://www.volaris.com/"},
    {"id": 22, "name": "Trip.com", "cn_name": "携程", "keywords": ["Trip.com", "携程", "携程机票"], "category": "platform", "website": "https://www.trip.com/"},
    {"id": 23, "name": "Skyscanner", "cn_name": "天巡", "keywords": ["Skyscanner", "天巡"], "category": "platform", "website": "https://www.skyscanner.net/"},
    {"id": 24, "name": "Google Flights", "cn_name": "谷歌航班", "keywords": ["Google Flights", "谷歌航班"], "category": "platform", "website": "https://www.google.com/flights"},
    {"id": 25, "name": "Kayak", "cn_name": "Kayak", "keywords": ["Kayak", "kayak 机票"], "category": "platform", "website": "https://www.kayak.com/"},
    {"id": 26, "name": "Momondo", "cn_name": "Momondo", "keywords": ["Momondo", "momondo 机票"], "category": "platform", "website": "https://www.momondo.com/"},
    {"id": 27, "name": "Expedia", "cn_name": "亿行", "keywords": ["Expedia", "亿行"], "category": "platform", "website": "https://www.expedia.com/"},
    {"id": 28, "name": "Traveloka", "cn_name": "Traveloka", "keywords": ["Traveloka"], "category": "platform", "website": "https://www.traveloka.com/"},
    {"id": 29, "name": "Agoda", "cn_name": "安可达", "keywords": ["Agoda", "安可达"], "category": "platform", "website": "https://www.agoda.com/"},
    {"id": 30, "name": "Booking.com", "cn_name": "缤客", "keywords": ["Booking.com", "缤客"], "category": "platform", "website": "https://www.booking.com/"},
    {"id": 31, "name": "Airpaz", "cn_name": "Airpaz", "keywords": ["Airpaz"], "category": "platform", "website": "https://www.airpaz.com/"},
    {"id": 32, "name": "去哪儿网", "cn_name": "去哪儿网", "keywords": ["去哪儿网", "去哪儿机票"], "category": "platform", "website": "https://www.qunar.com/"},
    {"id": 33, "name": "飞猪", "cn_name": "飞猪", "keywords": ["飞猪", "飞猪机票"], "category": "platform", "website": "https://www.fliggy.com/"},
    {"id": 34, "name": "同程旅行", "cn_name": "同程旅行", "keywords": ["同程旅行", "同程机票"], "category": "platform", "website": "https://www.ly.com/"}
]

SEARCH_TEMPLATES = [
    "{name} {target_year} promo code discount",
    "{cn_name} {target_year} 促销 优惠 特价机票",
    "{name} {target_year} special fare deal",
    "{name} {target_year} coupon sale",
]


def generate_search_queries(target, target_year):
    return [
        template.format(name=target["name"], cn_name=target["cn_name"], target_year=target_year)
        for template in SEARCH_TEMPLATES
    ]


def search_google(query, max_results=3):
    if not HAS_DEPS:
        return [{"type": "搜索链接", "content": f"[预览模式] {query}", "validity": "需在线验证", "source": ""}]
    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num={max_results * 2}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for g in soup.find_all("div", class_="g")[:max_results]:
            h3 = g.find("h3")
            if not h3:
                continue
            title = h3.get_text(strip=True)
            a = g.find("a")
            link = a.get("href", "") if a else ""
            if link.startswith("/url?q="):
                link = link[7:].split("&")[0]
            span = g.find("span", class_="aCOpFe")
            summary = span.get_text(strip=True) if span else ""
            results.append({"type": "搜索结果", "content": f"{title} {summary}".strip(), "validity": "需在线验证", "source": link})
        if not results:
            results = [{"type": "搜索结果", "content": f"未检索到可解析结果: {query}", "validity": "需在线验证", "source": ""}]
        return results
    except Exception as e:
        return [{"type": "搜索异常", "content": str(e), "validity": "需在线验证", "source": ""}]


def search_target_promos(target, target_year):
    queries = generate_search_queries(target, target_year)
    all_promos = []
    for query in queries[:3]:
        results = search_google(query)
        all_promos.extend(results)
        time.sleep(1)
    filtered = []
    seen = set()
    for promo in all_promos:
        key = promo.get("content", "")
        text = key.lower()
        if key in seen:
            continue
        if ("优惠" in key) or ("折扣" in key) or ("特价" in key) or ("promo" in text) or ("sale" in text):
            filtered.append(promo)
            seen.add(key)
    if not filtered:
        filtered = [{"type": "结果", "content": "需要进一步人工核验实时优惠", "validity": "需在线验证", "source": ""}]
    return filtered[:5]


def decide_write_mode():
    return "append" if os.environ.get("PROMO_WRITE_MODE", "").strip().lower() == "append" else "overwrite"


def build_markdown_content(all_results, timestamp, mode_text):
    airline_count = sum(1 for r in all_results if r["target"]["category"] == "airline")
    platform_count = sum(1 for r in all_results if r["target"]["category"] == "platform")
    lines = []
    lines.append(f"# 航空优惠搜索追踪 ({timestamp})")
    lines.append("")
    lines.append("## 汇总说明")
    lines.append(f"- 搜索目标: {len(all_results)} 个")
    lines.append(f"- 航空公司: {airline_count} 个")
    lines.append(f"- 订票平台: {platform_count} 个")
    lines.append("- 结构: 连续编号，无分级")
    lines.append(f"- 写入策略: {mode_text}")
    lines.append("")
    lines.append("## 优惠详情")
    for result in all_results:
        target = result["target"]
        lines.append("")
        lines.append(f"### {target['id']}. {target['name']} ({target['cn_name']})")
        lines.append(f"- 类型: {target['category']}")
        lines.append(f"- 官网: {target['website']}")
        lines.append("| 优惠类型 | 优惠内容 | 有效期 | 来源链接 |")
        lines.append("|----------|----------|--------|----------|")
        for promo in result["promos"]:
            promo_type = str(promo.get("type", "")).replace("|", " ")
            promo_content = str(promo.get("content", "")).replace("|", " ")
            promo_validity = str(promo.get("validity", "")).replace("|", " ")
            source = str(promo.get("source", "")).replace("|", " ")
            if source:
                source_text = f"[链接]({source})"
            else:
                source_text = "-"
            lines.append(f"| {promo_type} | {promo_content} | {promo_validity} | {source_text} |")
    lines.append("")
    return "\n".join(lines)


def write_tracking_doc(tracking_path, content, write_mode):
    mode_text = "覆盖重写" if write_mode == "overwrite" else "续写补充"
    if write_mode == "overwrite":
        tracking_path.parent.mkdir(parents=True, exist_ok=True)
        tracking_path.write_text(content, encoding="utf-8")
    else:
        existing = tracking_path.read_text(encoding="utf-8") if tracking_path.exists() else ""
        merged = existing.rstrip() + "\n\n" + content.lstrip("\n")
        tracking_path.write_text(merged, encoding="utf-8")
    return mode_text


def to_plain_text_summary(all_results, mode_text):
    airline_count = sum(1 for r in all_results if r["target"]["category"] == "airline")
    platform_count = sum(1 for r in all_results if r["target"]["category"] == "platform")
    lines = []
    lines.append(f"搜索完成，共 {len(all_results)} 个目标")
    lines.append(f"航空公司: {airline_count} 个")
    lines.append(f"订票平台: {platform_count} 个")
    lines.append(f"写入策略: {mode_text}")
    lines.append("结构: 连续编号，无分级")
    lines.append("追踪文件: references/promo_tracking.md")
    return "\n".join(lines)


def main():
    workspace = Path(os.environ.get("WORKSPACE", Path.cwd()))
    tracking_path = workspace / TRACKING_FILE_REL
    current_year = datetime.now().year
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    all_results = []
    for index, target in enumerate(TARGETS, 1):
        print(f"[{index}/{len(TARGETS)}] 搜索 {target['name']}")
        promos = search_target_promos(target, current_year)
        all_results.append({"target": target, "promos": promos})
    write_mode = decide_write_mode()
    mode_text = "覆盖重写" if write_mode == "overwrite" else "续写补充"
    content = build_markdown_content(all_results, timestamp, mode_text)
    write_tracking_doc(tracking_path, content, write_mode)
    summary = to_plain_text_summary(all_results, mode_text)
    print(summary)
    return summary


if __name__ == "__main__":
    main()
