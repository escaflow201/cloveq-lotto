import requests
import json

def main():
    # 데이터 소스
    url = "https://raw.githubusercontent.com/yous/lotto/master/data.json"
    
    try:
        response = requests.get(url, timeout=15)
        raw_data = response.json()
        
        # 최신 10개만 추출
        sorted_keys = sorted(raw_data.keys(), key=lambda x: int(x), reverse=True)[:10]
        
        new_results = []
        for key in sorted_keys:
            # 원본 데이터가 아무리 복잡해도 아래 4개만 딱 골라 담습니다.
            clean_item = {
                "round": int(key),
                "draw_date": raw_data[key].get("date", ""),
                "numbers": raw_data[key].get("numbers", []),
                "bonus": raw_data[key].get("bonus", 0)
            }
            new_results.append(clean_item)

        # 파일 쓰기 (기존 내용을 싹 지우고 새로 작성)
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(new_results, f, ensure_ascii=False, indent=2)
            
        print("🎉 [성공] 권한 승인 확인! 데이터 형식을 깔끔하게 교체했습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
