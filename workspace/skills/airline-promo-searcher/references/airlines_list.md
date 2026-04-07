# 搜索目标列表配置

## 使用说明

- 本文件维护统一的搜索目标列表，采用连续编号结构。
- 执行时按 `id` 顺序从 1 到 34 依次搜索。
- `category` 用于区分 `airline` 与 `platform`。

```json
[
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
```

## 统计

- 搜索目标总数: 34
- 航空公司: 21
- 订票平台: 13
