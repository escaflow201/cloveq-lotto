import urllib.request
import json
import time
import os

def get_lotto_data():
    # URL 직접 입력 (라이브러리 참조 없이)
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    
    # 2026년 기준 안전한 최신 회차
    current_round = 1218 
    results = []

    print("--- 데이터 업데이트 시작 ---")

    for i in range(10):
        target = current_round - i
        try:
            # 파이썬 표준 라이브러리만 사용 (requests 절대 안 씀)
            req = urllib.request.Request(url + str(target), headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_body = response.read().decode('utf-8')
                data = json.loads(res_body)
                
                if data.get("returnValue") == "success":
                    results.append({
                        "round": data["drwNo"],
                        "draw_date": data["drwNoDate"],
                        "numbers": [data[f"drwtNo{n}"] for n in range(1, 7)],
                        "bonus": data["bnusNo"]
                    })
                    print(f"✅ {target}회 성공")
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ {target}회 실패: {e}")

    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("--- 모든 작업 완료 ---")
    else:
        print("저장할 데이터가 없습니다.")

if __name__ == "__main__":
    get_lotto_data()
