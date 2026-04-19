import json
import re
import time
from pathlib import Path

import requests

OUT_FILE = Path("lotto_recent_year.json")
BASE_URL = "https://www.dhlottery.co.kr/lt645/result?drwNo={}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.dhlottery.co.kr/lt645/result",
}

def fetch_round(round_no: int):
    url = BASE_URL.format(round_no)
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    html = res.text

    # 당첨번호 6개 + 보너스 1개 추출
    nums = re.findall(r'<span class="ball(?: \w+)?">(\d+)</span>', html)
    if len(nums) < 7:
        return None

    nums = [int(x) for x in nums[:7]]

    # 날짜 추출
    m_date = re.search(r'(\d{4}-\d{2}-\d{2})\s*추첨', html)
    draw_date = m_date.group(1) if m_date else ""

    return {
        "round": round_no,
        "draw_date": draw_date,
        "numbers": nums[:6],
        "bonus": nums[6],
    }

def main():
    # 지금 네 화면 기준 최신 결과가 1220회였으니까 여기서 시작
    latest_round = 1220
    results = []

    for round_no in range(latest_round, latest_round - 10, -1):
        row = fetch_round(round_no)
        if row:
            results.append(row)
        time.sleep(0.1)

    if len(results) < 10:
        raise RuntimeError(f"10회차를 다 못 가져왔어. 현재 {len(results)}개")

    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"완료: {results[0]['round']}회 ~ {results[-1]['round']}회 저장됨")

if __name__ == "__main__":
    main()
