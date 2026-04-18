import urllib.request
import json
import os
import time

def get_lotto_data():
    try:
        # 동행복권 API 주소
        base_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
        
        # 1. 최신 회차 번호 설정 (2026년 기준 대략적인 최신 회차)
        # 만약 에러가 나면 이 숫자를 조금 낮춰보세요.
        latest_round = 1218 
        results = []

        print(f"Fetching data starting from round {latest_round}...")

        for i in range(10):
            target_round = latest_round - i
            url = f"{base_url}{target_round}"
            
            # requests 대신 파이썬 기본 라이브러리 urllib 사용 (에러 방지용)
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
                if data.get("returnValue") == "success":
                    results.append({
                        "round": data["drwNo"],
                        "draw_date": data["drwNoDate"],
                        "numbers": [
                            data["drwtNo1"], data["drwtNo2"], data["drwtNo3"],
                            data["drwtNo4"], data["drwtNo5"], data["drwtNo6"]
                        ],
                        "bonus": data["bnusNo"]
                    })
                    print(f"Success: Round {target_round}")
                
            # 서버 과부하 방지를 위한 아주 짧은 휴식
            time.sleep(0.2)

        # 2. 결과 저장
        if results:
            with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Done! Updated {len(results)} rounds.")
        else:
            print("No data found.")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    get_lotto_data()
