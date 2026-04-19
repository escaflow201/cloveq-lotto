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

FIRST_DRAW_DATE = date(2002, 12, 7)  # 로또 1회 추첨일


def estimated_latest_round() -> int:
    today = date.today()
    weeks = (today - FIRST_DRAW_DATE).days // 7
    return weeks + 1 + 2  # 여유분 2회


def fetch_round(round_no: int):
    url = API_URL.format(round_no)
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

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
    start_guess = estimated_latest_round()

    # 예상 최신 회차부터 최근 10회 안에서만 찾기
    for round_no in range(start_guess, max(start_guess - 10, 0), -1):
        try:
            result = fetch_round(round_no)
            if result:
                return round_no
        except Exception:
            pass
        time.sleep(0.1)

    raise RuntimeError("최신 회차를 찾지 못했어.")


def main():
    latest_round = find_latest_round()
    results = []

    # 최근 52회 저장
    for round_no in range(latest_round, max(latest_round - 52, 0), -1):
        try:
            result = fetch_round(round_no)
            if result:
                results.append(result)
        except Exception as e:
            print(f"{round_no}회차 실패: {e}")
        time.sleep(0.05)

    if not results:
        raise RuntimeError("저장할 데이터가 없어.")

    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"완료: 최신 {results[0]['round']}회차까지 저장됨")


if __name__ == "__main__":
    main()
