import urllib.request
import json
import time

def get_lotto_data():
    # 라이브러리 충돌을 원천 차단하기 위해 urllib만 사용
    url_template = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    
    # 2026년 4월 기준 안전한 최신 회차 번호
    start_round = 1218 
    results = []

    print(f"데이터 업데이트 시작: {start_round}회부터 역순으로 10개")

    for i in range(10):
        target = start_round - i
        full_url = url_template + str(target)
        
        try:
            # 💡 requests.get 대신 파이썬 내장 기능을 사용합니다.
            with urllib.request.urlopen(full_url, timeout=10) as response:
                raw_data = response.read().decode('utf-8')
                data = json.loads(raw_data)
                
                if data.get("returnValue") == "success":
                    results.append({
                        "round": data["drwNo"],
                        "draw_date": data["drwNoDate"],
                        "numbers": [data[f"drwtNo{n}"] for n in range(1, 7)],
                        "bonus": data["bnusNo"]
                    })
                    print(f"✅ {target}회차 로드 완료")
                else:
                    print(f"❌ {target}회차 데이터 없음")
            
            time.sleep(0.5) # 서버 매너 타임
        except Exception as e:
            print(f"⚠️ {target}회차 오류: {e}")

    # 파일 저장
    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("🎉 모든 작업 성공! 파일이 저장되었습니다.")
    else:
        print("❗ 저장할 데이터가 없습니다.")
        exit(1)

if __name__ == "__main__":
    get_lotto_data()
