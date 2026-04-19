import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

MAIN_URL = "https://www.dhlottery.co.kr/common.do?method=main"
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
OUT_FILE = Path("lotto_recent_year.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.dhlottery.co.kr/",
}

def get_latest_round():
    res = requests.get(MAIN_URL, headers=HEADERS, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    el = soup.find("strong", id="lottoDrwNo")
    if not el:
        raise RuntimeError("최신 회차 못찾음")

    return int(el.text.strip())

def fetch_round(round_no: int):
    res = requests.get(API_URL.format(round_no), headers=HEADERS, timeout=10)
    res.raise_for_status()
    data = res.json()

    if data.get("returnValue") != "success":
        return None

    return {
        "round": data["drwNo"],
        "draw_date": data["drwNoDate"],
        "numbers": [
            data["drwtNo1"],
            data["drwtNo2"],
            data["drwtNo3"],
            data["drwtNo4"],
            data["drwtNo5"],
            data["drwtNo6"],
        ],
        "bonus": data["bnusNo"],
    }

def main():
    latest = get_latest_round()
    results = []

    for n in range(latest, max(latest - 52, 0), -1):
        row = fetch_round(n)
        if row:
            results.append(row)
        time.sleep(0.05)

    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"완료: {latest}회차까지 저장됨")

if __name__ == "__main__":
    main()
