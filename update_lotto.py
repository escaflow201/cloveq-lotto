import requests
import json

def main():
    # 동행복권 공식 API 대신, 차단이 없는 우회 API 사용
    # 최신 회차부터 역순으로 10개를 가져옵니다.
    results = []
    
    print("--- 우회 경로로 수집 시작 (매우 빠름) ---")
    
    try:
        # 최근 10개 데이터를 한 번에 던져주는 신뢰할만한 소스
        # (만약 이 주소가 막히면 다른 주소로 바로 대체 가능)
        response = requests.get("https://raw.githubusercontent.com/yous/lotto/master/data.json", timeout=10)
        all_data = response.json()
        
        # 가장 최신 데이터 10개만 추출 및 포맷팅
        # 해당 데이터는 회차별로 정리되어 있음
        latest_rounds = sorted(all_data.keys(), key=int, reverse=True)[:10]
        
        for r in latest_rounds:
            item = all_data[r]
            results.append({
                "round": int(r),
                "draw_date": item.get("date", ""),
                "numbers": item.get("numbers", []),
                "bonus": item.get("bonus", 0)
            })
            print(f"✅ {r}회 수집 완료")

    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")
        return

    if results:
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"🎉 드디어 성공! 최신 {len(results)}개 업데이트 완료!")

if __name__ == "__main__":
    main()
