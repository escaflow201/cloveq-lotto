import requests
import json
import time
from datetime import datetime

def main():
    # 브라우저인 척 하는 위장 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    # 1. 오늘 날짜 기준으로 대략적인 최신 회차 계산 (1회차: 2002-12-07)
    base_date = datetime(2002, 12, 7)
    now = datetime.now()
    approx_latest = ((now - base_date).days // 7) + 1
    
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    results = []

    print(f"--- 데이터 수집 시작 (예상 최신: {approx_latest}회) ---")
    
    # 2. 예상 회차부터 아래로 내려가며 딱 10개만 수집
    current = approx_latest + 1
    found = 0
    
    while found < 10:
        try:
            resp = requests.get(url + str(current), headers=headers, timeout=10)
            data = resp.json()
            
            if data.get("returnValue") == "success":
                results.append({
                    "round": data["drwNo"],
                    "draw_date": data["drwNoDate"],
                    "numbers": [data[f"drwtNo{j}"] for j in range(1, 7)],
                    "bonus": data["bnusNo"]
                })
                print(f"✅ {current}회 성공")
                found += 1
            
            current -= 1
            # 서버가 차단하지 않도록 1.5초씩 아주 천천히 가져옵니다
            time.sleep(1.5)
            
            if current < 1: break
        except:
            current -= 1
            continue

    # 3. 결과가 있을 때만 파일 저장
    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"🎉 최신 {len(results)}개 업데이트 완료!")

if __name__ == "__main__":
    main()
