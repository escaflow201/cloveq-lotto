import requests
import json
from datetime import datetime

def main():
    # 1. 오늘 날짜 기준으로 최신 회차 계산
    base_date = datetime(2002, 12, 7)
    now = datetime.now()
    latest_no = ((now - base_date).days // 7) + 1
    
    # 2. 동행복권 대신 사용할 데이터 소스 (훨씬 빠르고 차단이 적음)
    url = "https://open.lottolyzer.com/surveys/south-korea/6-slash-45-lotto/latest"
    results = []

    print(f"--- 최신 회차 데이터 수집 시작 ---")
    
    try:
        # 이 주소는 한 번에 최신 데이터를 다 줍니다.
        resp = requests.get("https://open.lottolyzer.com/surveys/south-korea/6-slash-45-lotto/list?page=1&per-page=10", timeout=10)
        data = resp.json()
        
        for item in data:
            results.append({
                "round": int(item["draw_no"]),
                "draw_date": item["draw_date"],
                "numbers": [int(n) for n in item["numbers"].split(",")],
                "bonus": int(item["bonus_no"])
            })
            print(f"✅ {item['draw_no']}회 로드 성공")

    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")
        # 만약 위 사이트가 안되면 기존 방식으로 딱 1개만 시도
        return

    # 3. 파일 저장
    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"🎉 최신 {len(results)}개 업데이트 완료!")

if __name__ == "__main__":
    main()
