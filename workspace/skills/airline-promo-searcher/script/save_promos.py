"""保存优惠数据模块
- 读取 promo_data.json
- POST 到后端接口
"""

import json
import re
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# 优惠数据保存接口
SAVE_DISCOUNTS_URL = "http://192.168.1.173:7001/servlet/ServiceServlet?method=saveOrUpdateAiDiscounts"

# JSON 数据文件路径
PROMO_JSON_FILE = Path(__file__).parent.parent / "references" / "promo_data.json"


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


def load_promos_from_json(file_path: Path) -> list:
    """从 promo_data.json 加载优惠数据"""
    if not file_path.exists():
        print(f"文件不存在：{file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("promos", [])
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}")
        return []


def save_promo_to_json(promo: dict, file_path: Path = None) -> bool:
    """
    添加单条优惠记录到 JSON 文件
    如果已存在相同记录（source_url + promo_type 相同），则跳过
    """
    if file_path is None:
        file_path = PROMO_JSON_FILE

    # 加载现有数据
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {"updated_at": None, "promos": []}
    else:
        data = {"updated_at": None, "promos": []}

    # 检查是否已存在（source_url + promo_type 相同视为重复）
    for existing in data.get("promos", []):
        if (existing.get("source_url") == promo.get("source_url") and
                existing.get("promo_type") == promo.get("promo_type")):
            print(f"跳过重复记录：{promo.get('airline_name')} - {promo.get('promo_type')}")
            return False

    # 添加新记录
    data["promos"].append(promo)
    data["updated_at"] = datetime.now().astimezone().isoformat()

    # 写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return True


def init_promo_file(file_path: Path = None) -> bool:
    """初始化/清空 JSON 文件"""
    if file_path is None:
        file_path = PROMO_JSON_FILE

    data = {
        "updated_at": datetime.now().astimezone().isoformat(),
        "promos": []
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return True


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


def create_promo_entry(
    airline_name: str,
    iata_code: str,
    icao_code: str,
    promo_type: str,
    promo_content: str,
    source_url: str,
    validity: str = None,
    belong_map: dict = None
) -> dict:
    """
    创建单条优惠记录对象
    """
    # 解析有效期
    start_date = None
    end_date = None

    if validity:
        if "至" in validity:
            dates = validity.split("至")
            if len(dates) == 2:
                start_date = dates[0].strip()
                end_date = dates[1].strip()
        elif validity not in ["待确认", "限时", "-", ""]:
            end_date = validity

    # 获取 belong 字段
    belong = belong_map.get(iata_code, "") if belong_map else ""

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


def main():
    """主函数"""
    print("=== 航司优惠数据同步 ===")
    print(f"读取文件：{PROMO_JSON_FILE}")

    # 加载优惠数据
    promos = load_promos_from_json(PROMO_JSON_FILE)

    if not promos:
        print("未找到优惠记录")
        return

    print(f"加载到 {len(promos)} 条优惠记录")

    # 显示预览
    print("\n优惠预览:")
    for i, promo in enumerate(promos[:3]):
        content = promo.get('promo_content', '')[:40]
        print(f"  {i+1}. {promo['airline_name']} ({promo['airline_iata_code']}): {content}...")

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
