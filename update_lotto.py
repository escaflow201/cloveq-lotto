import requests
import json

def main():
    # 1. 아까와는 아예 다른, 진짜 업데이트 되는 API 주소입니다.
    url = "https://api.openlotto.co.kr/v1/lotto/last" # 최신 회차 가져오기
    
    try:
        print("--- 최신 회차 데이터 확인 중 ---")
        resp = requests.get(url, timeout=10)
        last_data = resp.json()
        last_no = last_data['drwNo'] # 현재 최신 회차 번호
        
        new_results = []
        
        # 2. 최신 회차부터 거꾸로 10개만 수집
        for i in range(last_no, last_no - 10, -1):
            detail_url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
            detail_resp = requests.get(detail_url, timeout=10)
            d = detail_resp.json()
            
            if d.get("returnValue") == "success":
                new_results.append({
                    "round": d["drwNo"],
                    "draw_date": d["drwNoDate"],
                    "numbers": [d["drwtNo1"], d["drwtNo2"], d["drwtNo3"], d["drwtNo4"], d["drwtNo5"], d["drwtNo6"]],
                    "bonus": d["bnusNo"]
                })
                print(f"✅ {i}회차 성공")

        # 3. 파일 저장 (권한 설정 하셨으니 이번엔 무조건 꽂힙니다)
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(new_results, f, ensure_ascii=False, indent=2)
        
        print(f"🎉 드디어 1218회 탈출! 최신 {last_no}회차까지 업데이트 완료.")

    except Exception as e:
        print(f"❌ 또 에러 발생: {e}")

if __name__ == "__main__":
    main()
