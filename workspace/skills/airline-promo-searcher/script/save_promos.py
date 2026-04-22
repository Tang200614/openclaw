"""保存优惠数据模块
- 读取 promo_data.md
- 解析表格中的优惠记录
- POST 到后端接口
"""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

# 优惠数据保存接口
SAVE_DISCOUNTS_URL = "http://192.168.1.173:7001/servlet/ServiceServlet?method=saveOrUpdateAiDiscounts"


def normalize_belong(belong: str) -> str:
    """
    规范化 belong 字段格式
    从 "US(美国)" 或 "QA(卡塔尔)" 转换为纯二字码 "US" 或 "QA"
    """
    if not belong:
        return ""

    # 匹配 "XX(YYY)" 格式，提取括号前的二字码
    match = re.match(r'^([A-Z]{2})\(', belong)
    if match:
        return match.group(1)

    # 如果没有括号格式，直接返回原值（假设已是二字码）
    return belong


def build_belong_map() -> dict:
    """从航司数据构建 belong 映射表（二字码 -> 国家/地区二字码）"""
    try:
        from fetch_airlines import get_airlines
        airlines = get_airlines()
        belong_map = {}
        for a in airlines:
            iata = a.get("iata_code", "")
            belong = a.get("belong", "")
            if iata and belong:
                belong_map[iata] = normalize_belong(belong)
        return belong_map
    except Exception as e:
        print(f"构建 belong 映射表失败：{e}")
        return {}


def parse_promos_from_file(file_path: Path, belong_map: dict = None) -> list:
    """从 promo_data.md 解析优惠数据"""
    if not file_path.exists():
        print(f"文件不存在：{file_path}")
        return []

    # 如果没有提供 belong_map，尝试从航司数据构建
    if belong_map is None:
        belong_map = build_belong_map()

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    promos = []
    lines = content.split("\n")
    in_table = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测表格开始
        if line.startswith("| 航司 |") and "二字码" in line:
            in_table = True
            continue

        # 跳过表头分隔线
        if in_table and line.startswith("|---"):
            continue

        # 解析数据行
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 6 and parts[0] not in ["航司", "示例"]:
                # 解析优惠记录（不再检查状态列）
                promo = parse_promo_row(parts, belong_map)
                if promo:
                    promos.append(promo)

        # 检测表格结束
        if in_table and not line.startswith("|"):
            break

    return promos


def parse_promo_row(parts: list, belong_map: dict = None) -> dict | None:
    """解析表格行为优惠对象"""
    try:
        airline_name = parts[0] if len(parts) > 0 else ""
        iata_code = parts[1] if len(parts) > 1 else ""
        icao_code = parts[2] if len(parts) > 2 else ""
        promo_type = parts[3] if len(parts) > 3 else ""
        promo_content = parts[4] if len(parts) > 4 else ""
        validity = parts[5] if len(parts) > 5 else ""
        source_url = parts[6] if len(parts) > 6 else ""

        if not airline_name or not promo_content:
            return None

        # 从 belong_map 中获取规范化的 belong 字段
        belong = belong_map.get(iata_code, "") if belong_map else ""

        # 解析有效期
        start_date = None
        end_date = None

        if "至" in validity:
            dates = validity.split("至")
            if len(dates) == 2:
                start_date = dates[0].strip()
                end_date = dates[1].strip()
        elif validity and validity not in ["待确认", "限时", "-", ""]:
            end_date = validity

        return {
            "airline_name": airline_name,
            "airline_iata_code": iata_code,
            "airline_icao_code": icao_code,
            "belong": belong,
            "promo_type": promo_type,
            "promo_content": promo_content,
            "promo_start_date": start_date,
            "promo_end_date": end_date,
            "source_url": source_url,
        }
    except Exception as e:
        print(f"解析行失败：{e}")
        return None


def sync_to_backend(promos: list) -> bool:
    """同步优惠数据到后端接口"""
    if not promos:
        print("没有优惠数据需要同步")
        return False

    # 构建表单数据
    discounts_json = json.dumps(promos, ensure_ascii=False)
    form_data = f"discountsJson={urllib.parse.quote(discounts_json, encoding='utf-8')}".encode("utf-8")

    # 构建请求
    req = urllib.request.Request(
        SAVE_DISCOUNTS_URL,
        data=form_data,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(len(form_data)),
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            content = response.read().decode(charset, errors="replace")

        print(f"同步成功！响应内容：{content}")
        return True

    except urllib.error.HTTPError as e:
        error_content = e.read().decode(e.headers.get_content_charset() or "utf-8", errors="replace")
        print(f"HTTP 错误 {e.code}: {error_content}")
        return False

    except Exception as e:
        print(f"同步失败：{e}")
        return False


def main():
    """主函数"""
    promo_file = Path(__file__).parent.parent / "references" / "promo_data.md"

    print("=== 航司优惠数据同步 ===")
    print(f"读取文件：{promo_file}")

    # 解析优惠数据
    promos = parse_promos_from_file(promo_file)

    if not promos:
        print("未找到优惠记录")
        return

    print(f"解析到 {len(promos)} 条优惠记录")

    # 显示预览
    print("\n优惠预览:")
    for i, promo in enumerate(promos[:3]):
        print(f"  {i+1}. {promo['airline_name']} ({promo['airline_iata_code']}): {promo['promo_content'][:40]}...")

    if len(promos) > 3:
        print(f"  ... 还有 {len(promos) - 3} 条")

    # 同步到后端
    print(f"\n正在同步到：{SAVE_DISCOUNTS_URL}")
    success = sync_to_backend(promos)

    if success:
        print(f"\n✓ 同步完成！共 {len(promos)} 条记录")
    else:
        print(f"\n✗ 同步失败")


if __name__ == "__main__":
    main()
