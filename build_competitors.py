# -*- coding: utf-8 -*-
"""把 大程_門市營收預測/競爭店明細.csv 處理成前端地圖用的輕量 JSON。
原始 34,446 筆是「每個 7-11 錨點門市 200m 內查到的競爭店」，同一家競爭店
會被多個鄰近的 7-11 錨點重複列到，所以先用 (品牌,經緯度,店名) 去重，
只留下每家實體競爭店一筆，供地圖畫點用。
"""
import json

import pandas as pd

SRC = "../../大程_門市營收預測/大程_門市營收預測/競爭店明細.csv"
OUT = "data_competitors.json"

BRAND_MAP = {
    "全家 FamilyMart": "fm",
    "萊爾富 Hi-Life": "hl",
    "OK mart": "ok",
    "美廉社": "px",  # 標籤不純，見前端註記：實際混了全聯/家樂福/好市多等
}


def main():
    df = pd.read_csv(SRC, encoding="utf-8-sig")
    df["latr"] = df["latitude"].round(5)
    df["lngr"] = df["longitude"].round(5)
    dedup = df.drop_duplicates(subset=["competingTypeName", "latr", "lngr", "competitorName"])

    out = []
    for _, row in dedup.iterrows():
        b = BRAND_MAP.get(row["competingTypeName"])
        if not b:
            continue
        out.append({
            "b": b,
            "n": row["competitorName"],
            "c": [round(float(row["longitude"]), 6), round(float(row["latitude"]), 6)],
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    counts = {}
    for x in out:
        counts[x["b"]] = counts.get(x["b"], 0) + 1
    print(f"總筆數 {len(out)}，寫入 {OUT}")
    print(counts)


if __name__ == "__main__":
    main()
