import requests
import json
import time
from datetime import datetime

def get_latest_round():
    # 로또 시작일로부터 현재까지 몇 주가 지났는지 계산해서 대략적인 회차 계산
    # 1회차: 2002-12-07
    base_date = datetime(2002, 12, 7)
    now = datetime.now()
    diff_weeks = (now - base_date).days // 7
    return diff_weeks + 1

def main():
    # 사람이 브라우저로 접속하는 것처럼 속이는 설정 (매우 중요)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 1. 계산된 예상 최신 회차부터 시작
    approx_latest = get_latest_round()
    print(f"예상 최신 회차: {approx_latest}")
    
    base_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    results = []

    # 2. 최신 회차부터 역순으로 가져오기 (차단 방지를 위해 천천히)
    count = 0
    target = approx_latest + 2 # 혹시 모르니 예상보다 2회차 더 위부터 시도
    
    while count < 50: # 최근 50개만 가져오기
        try:
            resp = requests.get(base_url + str(target), headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("returnValue") == "success":
                    results.append({
                        "round": data["drwNo"],
                        "draw_date": data["drwNoDate"],
                        "numbers": [data[f"drwtNo{j}"] for j in range(1, 7)],
                        "bonus": data["bnusNo"]
                    })
                    print(f"✅ {target}회 완료")
                    count += 1
                elif data.get("returnValue") == "fail" and count == 0:
                    print(f"ℹ️ {target}회는 아직 추첨 전입니다.")
                else:
                    # 중간에 데이터가 비어있으면 종료 (너무 옛날 회차 등)
                    if count > 0: break
            
            target -= 1
            time.sleep(0.5) # 서버가 화내지 않게 0.5초씩 쉽니다.
        except Exception as e:
            print(f"⚠️ {target}회 시도 중 오류: {e}")
            target -= 1

    # 3. 파일 저장
    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"🎉 총 {len(results)}개의 회차 업데이트 완료!")

if __name__ == "__main__":
    main()
