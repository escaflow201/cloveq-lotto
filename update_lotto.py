import requests
import json

# 최근 회차 찾기
def get_latest_round():
    for i in range(1300, 1000, -1):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        res = requests.get(url)
        data = res.json()

        if data.get("returnValue") == "success":
            return i
    return None

# 최근 10회 가져오기
def get_latest_10():
    latest = get_latest_round()
    result = []

    for i in range(latest, latest-10, -1):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        res = requests.get(url)
        data = res.json()

        if data.get("returnValue") == "success":
            result.append({
                "round": i,
                "numbers": [
                    data["drwtNo1"],
                    data["drwtNo2"],
                    data["drwtNo3"],
                    data["drwtNo4"],
                    data["drwtNo5"],
                    data["drwtNo6"]
                ],
                "bonus": data["bnusNo"]
            })

    return result

# 저장
data = get_latest_10()

with open("lotto_recent.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("완료")
