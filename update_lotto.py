import json
import re
import time
from pathlib import Path

import requests

INTRO_URL = "https://www.dhlottery.co.kr/lotto645/intro.do?method=main"
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
OUT_FILE = Path("lotto_recent_year.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.dhlottery.co.kr/",
}

def get_latest_result_round():
    res = requests.get(INTRO_URL, headers=HEADERS, timeout=15)
    res.raise_for_status()
    html = res.text

    rounds = re.findall(r"제\s*(\d+)\s*회", html)
    nums = sorted({int(x) for x in rounds}, reverse=True)

    if not nums:
        raise RuntimeError("회차를 찾지 못했어.")

    # 가장 큰 숫자는 예정 회차일 가능성이 크니까
    # 실제 당첨번호 API가 성공하는 가장 큰 회차를 찾음
    for n in nums:
        row = fetch_round(n)
        if row:
            return n
        time.sleep(0.05)

    raise RuntimeError("최신 결과 회차를 찾지 못했어.")

def fetch_round(round_no):
    try:
        res = requests.get(API_URL.format(round_no), headers=HEADERS, timeout=15)
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
    except Exception:
        return None

def main():
    latest_round = get_latest_result_round()
    results = []

    # 최근 10회차만 저장
    for round_no in range(latest_round, latest_round - 10, -1):
        row = fetch_round(round_no)
        if row:
            results.append(row)
        time.sleep(0.03)

    if not results:
        raise RuntimeError("최근 10회차를 가져오지 못했어.")

    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"완료: {results[0]['round']}회 ~ {results[-1]['round']}회 저장됨")

if __name__ == "__main__":
    main()
