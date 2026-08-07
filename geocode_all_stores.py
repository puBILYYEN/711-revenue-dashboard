# -*- coding: utf-8 -*-
"""把 data_stores.json 裡全部7,313家店的地址預先轉成經緯度(lnglat)，直接存進資料檔。
目的：現在每次點門市才臨時打Mapbox Geocoding API，網路來回時間讓地圖顯示變慢；
預先算好、存進JSON後，前端就不用再等API，點了立刻顯示。
"""
import json
import time
import urllib.parse

import requests  # pip-system-certs 的 .pth hook 會在直譯器啟動時自動修好SSL，這裡不用手動import

TOKEN = "pk.eyJ1IjoiYmlsbHl5ZW4iLCJhIjoiY21zYXp4cWlpMDRxYjJ4cjE3N3doeG5qcSJ9.-6z8zmeICOQDIyCGZIeWGQ"
DATA_FILE = "data_stores.json"
PROGRESS_FILE = "geocode_progress.json"
RATE_DELAY = 0.12  # ~8 req/sec，留餘裕不撞到免費方案限速


def geocode(addr):
    url = (
        "https://api.mapbox.com/geocoding/v5/mapbox.places/"
        f"{urllib.parse.quote(addr)}.json"
    )
    try:
        resp = requests.get(
            url, params={"access_token": TOKEN, "limit": 1, "country": "tw"}, timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        feats = data.get("features") or []
        if feats:
            return feats[0]["center"]  # [lng, lat]
    except Exception as e:
        print(f"  失敗: {addr[:30]} -> {e}")
    return None


def main():
    with open(DATA_FILE, encoding="utf-8-sig") as f:
        stores = json.load(f)

    done = {}
    try:
        with open(PROGRESS_FILE, encoding="utf-8") as f:
            done = json.load(f)
    except FileNotFoundError:
        pass

    total = len(stores)
    ok, fail = 0, 0
    for i, s in enumerate(stores):
        sid = s["id"]
        if sid in done:
            if done[sid]:
                ok += 1
            continue
        coords = geocode(s["addr"])
        done[sid] = coords
        if coords:
            ok += 1
        else:
            fail += 1
        time.sleep(RATE_DELAY)
        if (i + 1) % 200 == 0:
            print(f"進度 {i+1}/{total}  成功{ok} 失敗{fail}")
            with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(done, f, ensure_ascii=False)

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)

    for s in stores:
        coords = done.get(s["id"])
        if coords:
            s["lnglat"] = coords

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, separators=(",", ":"))

    print(f"完成。總數{total} 成功{ok} 失敗{fail}")


if __name__ == "__main__":
    main()
