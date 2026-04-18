import requests
import json

def main():
    # 동행복권 대신, 이미 정제된 데이터를 제공하는 신뢰할 수 있는 소스 사용
    # 이 소스는 깃허브 내 통신이라 차단당하지 않습니다.
    url = "https://raw.githubusercontent.com/yous/lotto/master/data.json"
    
    print("--- 최신 데이터 동기화 시작 ---")
    
    try:
        response = requests.get(url, timeout=10)
        all_data = response.json()
        
        # 회차 번호를 큰 순서대로 정렬해서 상위 10개만 추출
        sorted_rounds = sorted(all_data.keys(), key=lambda x: int(x), reverse=True)
        recent_10 = sorted_rounds[:10]
        
        results = []
        for r in recent_10:
            item = all_data[r]
            results.append({
                "round": int(r),
                "draw_date": item.get("date", ""),
                "numbers": item.get("numbers", []),
                "bonus": item.get("bonus", 0)
            })
            print(f"✅ {r}회차 가져오기 성공")

        # 파일 저장
        if results:
            with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print("🎉 모든 데이터가 최신으로 교체되었습니다!")
        else:
            print("⚠️ 가져올 데이터가 없습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
