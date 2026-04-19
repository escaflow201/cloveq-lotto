import json
import time
import requests
from pathlib import Path

API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
OUT_FILE = Path("lotto_recent_year.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.dhlottery.co.kr/"
}

def fetch_round(round_no: int):
    url = API_URL.format(round_no)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

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
        "bonus": data["bnusNo"]
    }

def find_latest_round(start_guess=1300):
    # 높은 회차부터 내려오면서 최초 success 찾기
    for n in range(start_guess, 1, -1):
        try:
            row = fetch_round(n)
            if row:
                return n
        except Exception:
            pass
        time.sleep(0.2)
    raise RuntimeError("최신 회차를 찾지 못함")

def main():
    latest = find_latest_round()
    results = []

    for n in range(latest, max(latest - 51, 0), -1):  # 최근 52회
        try:
            row = fetch_round(n)
            if row:
                results.append(row)
        except Exception as e:
            print(f"{n}회차 실패: {e}")
        time.sleep(0.2)

    if not results:
        raise RuntimeError("저장할 데이터가 없음")

    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"완료: 최신 {results[0]['round']}회차까지 저장")

if __name__ == "__main__":
    main()
