import requests
import json
import os

def get_lotto_data():
    try:
        # 최근 10회차 정도의 데이터를 가져오기 위해 범위를 설정 (최신 회차부터 역순)
        # 실제 로또 API 등을 활용하거나 lottolyzer 등의 데이터를 파싱하는 로직
        # 여기서는 안정적인 동행복권 API 예시를 활용합니다.
        
        # 1. 먼저 최신 회차가 몇 회인지 알아내야 함 (이 과정은 생략하고 1100회부터 확인하는 식이나 
        # 마지막 저장된 데이터 + 1부터 시도하는 것이 효율적임)
        
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
        
        results = []
        
        # 예시로 최근 10개만 가져오기 (실제로는 더 정교하게 짤 수 있음)
        # 테스트를 위해 현재 가장 최신인 1160회대부터 시도
        curr_round = 1168 # 기준점 (필요시 수정)
        
        for i in range(10):
            target = curr_round - i
            resp = requests.get(f"{url}{target}", timeout=10)
            data = resp.json()
            
            if data.get("returnValue") == "success":
                results.append({
                    "round": data["drwNo"],
                    "draw_date": data["drwNoDate"],
                    "numbers": [
                        data["drwtNo1"], data["drwtNo2"], data["drwtNo3"],
                        data["drwtNo4"], data["drwtNo5"], data["drwtNo6"]
                    ],
                    "bonus": data["bnusNo"]
                })
        
        # 파일 저장
        with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully updated {len(results)} rounds.")

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    get_lotto_data()
