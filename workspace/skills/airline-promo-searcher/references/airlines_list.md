# 搜索目标列表配置

## 使用说明

- 本文件维护统一的搜索目标列表，采用连续编号结构。
- 全部条目来自航司接口同步结果。
- 航司接口: `http://192.168.1.173:7001/servlet/ServiceServlet?method=getAirCompanyList&type=1`
- 执行时按 `id` 顺序从 1 到 21 依次搜索。
- `category` 固定为 `airline`。

```json
[
  {
    "id": 1,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "CEB",
    "cn_name": "宿雾航空",
    "keywords": [
      "CEB",
      "宿雾航空",
      "5J"
    ],
    "category": "airline",
    "website": "https://www.cebu-pacific.com/"
  },
  {
    "id": 2,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "IGO",
    "cn_name": "靛蓝航空",
    "keywords": [
      "IGO",
      "靛蓝航空",
      "6E"
    ],
    "category": "airline",
    "website": "https://www.goindigo.in/"
  },
  {
    "id": 3,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "AXM",
    "cn_name": "亚洲亚航",
    "keywords": [
      "AXM",
      "亚洲亚航",
      "AK"
    ],
    "category": "airline",
    "website": "https://www.airasia.com/"
  },
  {
    "id": 4,
    "type": "国际",
    "cheapboat": "FSC",
    "name": "EVA",
    "cn_name": "长荣航空",
    "keywords": [
      "EVA",
      "长荣航空",
      "BR"
    ],
    "category": "airline",
    "website": "https://www.evaair.com/"
  },
  {
    "id": 5,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "CAL",
    "cn_name": "中华航空",
    "keywords": [
      "CAL",
      "中华航空",
      "CI"
    ],
    "category": "airline",
    "website": "https://www.china-airlines.com/"
  },
  {
    "id": 6,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "CPA",
    "cn_name": "国泰航空",
    "keywords": [
      "CPA",
      "国泰航空",
      "CX"
    ],
    "category": "airline",
    "website": "https://www.cathaypacific.com/"
  },
  {
    "id": 7,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "UAE",
    "cn_name": "阿联酋航",
    "keywords": [
      "UAE",
      "阿联酋航",
      "EK"
    ],
    "category": "airline",
    "website": "https://www.emirates.com/"
  },
  {
    "id": 8,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "FRE",
    "cn_name": "福莱尔航空",
    "keywords": [
      "FRE",
      "福莱尔航空",
      "F8"
    ],
    "category": "airline",
    "website": "https://flyflair.com/"
  },
  {
    "id": 9,
    "type": "国际",
    "cheapboat": "FSC",
    "name": "JAL",
    "cn_name": "日本航空",
    "keywords": [
      "JAL",
      "日本航空",
      "JL"
    ],
    "category": "airline",
    "website": "https://www.jal.co.jp/"
  },
  {
    "id": 10,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "KAL",
    "cn_name": "大韩航空",
    "keywords": [
      "KAL",
      "大韩航空",
      "KE"
    ],
    "category": "airline",
    "website": "https://www.koreanair.com/"
  },
  {
    "id": 11,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "ANA",
    "cn_name": "全日空",
    "keywords": [
      "ANA",
      "全日空",
      "NH"
    ],
    "category": "airline",
    "website": "https://www.ana.co.jp/"
  },
  {
    "id": 12,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "NKS",
    "cn_name": "精神航空",
    "keywords": [
      "NKS",
      "精神航空",
      "NK"
    ],
    "category": "airline",
    "website": "https://www.spirit.com/"
  },
  {
    "id": 13,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "QTR",
    "cn_name": "卡塔尔航空",
    "keywords": [
      "QTR",
      "卡塔尔航空",
      "QR"
    ],
    "category": "airline",
    "website": "https://www.qatarairways.com/"
  },
  {
    "id": 14,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "TLM",
    "cn_name": "狮航",
    "keywords": [
      "TLM",
      "狮航",
      "SL"
    ],
    "category": "airline",
    "website": "https://www.lionairthai.com/"
  },
  {
    "id": 15,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "SIA",
    "cn_name": "新加坡航",
    "keywords": [
      "SIA",
      "新加坡航",
      "SQ"
    ],
    "category": "airline",
    "website": "https://www.singaporeair.com/"
  },
  {
    "id": 16,
    "type": "国际",
    "cheapboat": "FSC",
    "name": "THY",
    "cn_name": "土耳其航",
    "keywords": [
      "THY",
      "土耳其航",
      "TK"
    ],
    "category": "airline",
    "website": "https://www.turkishairlines.com/"
  },
  {
    "id": 17,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "HKE",
    "cn_name": "香港快运航空公司",
    "keywords": [
      "HKE",
      "香港快运航空公司",
      "UO"
    ],
    "category": "airline",
    "website": "https://www.hkexpress.com/"
  },
  {
    "id": 18,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "VJC",
    "cn_name": "越捷航空",
    "keywords": [
      "VJC",
      "越捷航空",
      "VJ"
    ],
    "category": "airline",
    "website": "https://www.vietjetair.com/"
  },
  {
    "id": 19,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "HVN",
    "cn_name": "越南航空",
    "keywords": [
      "HVN",
      "越南航空",
      "VN"
    ],
    "category": "airline",
    "website": "https://www.vietnamairlines.com/"
  },
  {
    "id": 20,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "WZZ",
    "cn_name": "维兹航空",
    "keywords": [
      "WZZ",
      "维兹航空",
      "W6"
    ],
    "category": "airline",
    "website": "https://wizzair.com/"
  },
  {
    "id": 21,
    "type": "国际",
    "cheapboat": "LCC",
    "name": "VOI",
    "cn_name": "墨西哥VOLARIS",
    "keywords": [
      "VOI",
      "墨西哥VOLARIS",
      "Y4"
    ],
    "category": "airline",
    "website": "https://www.volaris.com/"
  }
]
```

## 统计

- 搜索目标总数: 21
- 航空公司: 21
- 订票平台: 0
