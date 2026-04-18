import requests
import json

def main():
    # 1. 동행복권 직접 접속 대신, 차단 없는 고속 데이터 소스 사용
    # (이미 전 세계 개발자들이 최신 로또 번호를 공유하는 오픈 API입니다)
    url = "https://raw.githubusercontent.com/yous/lotto/master/data.json"
    
    try:
        print("--- 최신 데이터 소스 연결 중... ---")
        response = requests.get(url, timeout=15)
        raw_data = response.json()
        
        # 2. 회차 번호를 큰 순서대로 정렬 (1220, 1219, 1218...)
        sorted_keys = sorted(raw_data.keys(), key=lambda x: int(x), reverse=True)
        latest_keys = sorted_keys[:10]  # 최신 10개
        
        new_results = []
        for key in latest_keys:
            item = raw_data[key]
            # 사용자님이 원하는 깔끔한 4개 항목만 추출
            new_results.append({
                "round": int(key),
                "draw_date": item.get("date", ""),
                "numbers": item.get("numbers", []),
                "bonus": item.get("bonus", 0)
            })
            print(f"✅ {key}회차 데이터 재구성 완료")

        # 3. 데이터가 있을 때만 파일 덮어쓰기
        if new_results and new_results[0]['round'] > 1218:
            with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
                json.dump(new_results, f, ensure_ascii=False, indent=2)
            print(f"🎉 성공: {new_results[0]['round']}회차까지 업데이트 완료!")
        else:
            print("⚠️ 최신 데이터를 찾지 못했습니다. 1218회보다 높은 회차가 없습니다.")

    except Exception as e:
        print(f"❌ 치명적 오류 발생: {e}")

if __name__ == "__main__":
    main()
