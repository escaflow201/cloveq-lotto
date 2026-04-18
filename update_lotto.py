import requests
import json
import time
from datetime import datetime

def get_approx_latest():
    # 1회차(2002-12-07)부터 오늘까지 몇 주 지났는지 계산 (서버 부하 방지)
    base_date = datetime(2002, 12, 7)
    now = datetime.now()
    return ((now - base_date).days // 7) + 1

def main():
    # 브라우저인 척 위장하여 차단 회피
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    
    latest_calc = get_approx_latest()
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    results = []

    print(f"계산된 최신 회차 근처({latest_calc})부터 50개를 가져옵니다.")

    # 최신 회차부터 역순으로 50개만 시도
    count = 0
    # 아직 추첨 안 된 회차를 대비해 +1부터 시작
    for i in range(latest_calc + 1, latest_calc - 60, -1):
        if count >= 50: break
        
        try:
            resp = requests.get(url + str(i), headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("returnValue") == "success":
                    results.append({
                        "round": data["drwNo"],
                        "draw_date": data["drwNoDate"],
                        "numbers": [data[f"drwtNo{j}"] for j in range(1, 7)],
                        "bonus": data["bnusNo"]
                    })
                    print(f"✅ {i}회 로드 성공")
                    count += 1
            # 서버가 힘들어하지 않게 중간중간 쉽니다
            time.sleep(0.5)
        except:
            continue

    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("🎉 업데이트 완료!")

if __name__ == "__main__":
    main()
