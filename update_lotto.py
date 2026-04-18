import requests
import json
import time

def get_latest_round():
    # 최신 회차를 찾는 함수
    base_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    # 안전하게 1210회부터 시작해서 최신 회차까지 확인
    start_no = 1210 
    
    while True:
        resp = requests.get(base_url + str(start_no))
        data = resp.json()
        if data.get("returnValue") == "fail":
            return start_no - 1 # 실패 바로 전 회차가 최신
        start_no += 1
        time.sleep(0.1)

def main():
    latest = get_latest_round()
    print(f"확인된 최신 회차: {latest}")
    
    base_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    results = []

    # 최신 회차부터 역순으로 50개 가져오기
    for i in range(latest, latest - 50, -1):
        resp = requests.get(base_url + str(i))
        data = resp.json()
        
        if data.get("returnValue") == "success":
            results.append({
                "round": data["drwNo"],
                "draw_date": data["drwNoDate"],
                "numbers": [data[f"drwtNo{j}"] for j in range(1, 7)],
                "bonus": data["bnusNo"]
            })
            print(f"{i}회 데이터 로드 성공")
        time.sleep(0.2)

    with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("저장 완료!")

if __name__ == "__main__":
    main()
