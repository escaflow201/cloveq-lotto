import requests
import json
import time
from datetime import datetime

def main():
    # 1. 사람인 척 위장 (차단 방지 핵심)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    # 2. 오늘 날짜 기준 대략적인 회차 계산 (1회차: 2002-12-07)
    base_date = datetime(2002, 12, 7)
    now = datetime.now()
    approx_latest = ((now - base_date).days // 7) + 1
    
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    results = []

    print(f"--- 최신 10개 회차 수집 시작 (예상: {approx_latest}회) ---")
    
    # 예상 회차보다 1~2개 높은 곳부터 아래로 내려가며 찾기
    current = approx_latest + 1
    found_count = 0
    
    while found_count < 10:
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
                found_count += 1
            
            current -= 1
            time.sleep(1.0) # 10개만 하니까 1초씩 넉넉히 쉽니다 (안전제일)
            
            # 너무 밑으로 내려가면 중단 (방어 코드)
            if current < 1: break
                
        except:
            current -= 1
            continue

    # 3. 파일 저장
    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"🎉 최신 {len(results)}개 업데이트 완료!")

if __name__ == "__main__":
    main()
