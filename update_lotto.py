import requests
import json

def main():
    # 데이터 소스 (동행복권 차단을 피하기 위해 사용)
    url = "https://raw.githubusercontent.com/yous/lotto/master/data.json"
    
    try:
        response = requests.get(url, timeout=15)
        raw_data = response.json()
        
        # 최신 10개 회차 번호만 추출
        sorted_keys = sorted(raw_data.keys(), key=lambda x: int(x), reverse=True)[:10]
        
        new_results = []
        for key in sorted_keys:
            item = raw_data[key]
            
            # --- [이 부분이 핵심 변화!] ---
            # 원본에 sum, numbers_text가 있어도 무시하고 아래 4개만 딱 골라 담습니다.
            clean_item = {
                "round": int(key),
                "draw_date": item.get("date", ""),
                "numbers": item.get("numbers", []),
                "bonus": item.get("bonus", 0)
            }
            new_results.append(clean_item)
            # ----------------------------

        # 파일을 저장할 때 무조건 새로 씁니다.
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(new_results, f, ensure_ascii=False, indent=2)
            
        print("🎉 형식을 완전히 새로 고쳐서 저장했습니다!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
