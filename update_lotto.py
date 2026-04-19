import json
import time
from pathlib import Path
from datetime import date

import requests

API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
OUT_FILE = Path("lotto_recent_year.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.dhlottery.co.kr/",
}

FIRST_DRAW_DATE = date(2002, 12, 7)  # 1회 추첨일


def estimate_round() -> int:
    today = date.today()
    weeks = (today - FIRST_DRAW_DATE).days // 7
    return weeks + 1


def fetch_round(round_no: int):
    url = API_URL.format(round_no)
    res = requests.get(url, headers=HEADERS, timeout=15)
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


def find_latest_round() -> int:
    guessed = estimate_round() + 2  # 여유 2회

    # 예상 최신 회차부터 아래로 15회만 확인
    for round_no in range(guessed, max(guessed - 15, 0), -1):
        try:
            row = fetch_round(round_no)
            if row:
                return round_no
        except Exception:
            pass
        time.sleep(0.05)

    raise RuntimeError("최신 회차를 찾지 못했어.")


def main():
    latest_round = find_latest_round()
    results = []

    # 최근 52회 저장
    for round_no in range(latest_round, max(latest_round - 52, 0), -1):
        try:
            row = fetch_round(round_no)
            if row:
                results.append(row)
        except Exception as e:
            print(f"{round_no}회차 실패: {e}")
        time.sleep(0.03)

    if not results:
        raise RuntimeError("저장할 데이터가 없어.")

    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"완료: 최신 {latest_round}회차까지 저장됨")


if __name__ == "__main__":
    main()
