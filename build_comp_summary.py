# -*- coding: utf-8 -*-
"""把 競爭店明細.csv 依「錨點門市(storeId)」彙總成每家店周邊各品牌競爭店數量，
供前端「競爭飽和度警示」卡片用。跟 build_competitors.py 是同一份原始資料，
但這支不去重——目的不同：這裡要的是「這家 7-11 旁邊到底有幾家競爭店」，
同一家競爭店被兩個不同錨點各查到一次，對兩個錨點來說都是真的「旁邊有一家」。
"""
import json

import pandas as pd

SRC = "../../大程_門市營收預測/大程_門市營收預測/競爭店明細.csv"
OUT = "data_comp_summary.json"

BRAND_MAP = {
    "全家 FamilyMart": "fm",
    "萊爾富 Hi-Life": "hl",
    "OK mart": "ok",
    "美廉社": "px",
}


def main():
    df = pd.read_csv(SRC, encoding="utf-8-sig")
    df["b"] = df["competingTypeName"].map(BRAND_MAP)
    df = df.dropna(subset=["b"])

    out = {}
    for store_id, g in df.groupby("storeId"):
        counts = g["b"].value_counts().to_dict()
        rec = {k: int(counts.get(k, 0)) for k in ["fm", "hl", "ok", "px"]}
        rec["total"] = sum(rec.values())
        out[str(store_id)] = rec

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    totals = [v["total"] for v in out.values()]
    print(f"涵蓋 {len(out)} 家錨點門市，寫入 {OUT}")
    print(f"total 分布: min={min(totals)} max={max(totals)} avg={sum(totals)/len(totals):.2f}")


if __name__ == "__main__":
    main()
