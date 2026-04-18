import requests
import json
import os

def get_lotto_data(drwNo):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    response = requests.get(url)
    data = response.json()
    if data.get("returnValue") == "success":
        # 기존 JSON 형식에 맞게 변환
        nums = [data['drwtNo1'], data['drwtNo2'], data['drwtNo3'], data['drwtNo4'], data['drwtNo5'], data['drwtNo6']]
        return {
            "round": data['drwNo'],
            "draw_date": data['drwNoDate'],
            "numbers": nums,
            "bonus": data['bnusNo'],
            "numbers_text": ", ".join(map(str, nums)),
            "sum": sum(nums),
            "odd_count": len([n for n in nums if n % 2 != 0]),
            "source": "https://www.dhlottery.co.kr/"
        }
    return None

# 1. 최신 회차 번호 찾기 (동행복권은 에러가 날 때까지 회차를 올려보면 알 수 있음)
# 여기선 단순히 최신 1개를 먼저 가져와서 확인하는 로직을 씁니다.
start_round = 1100 # 안전하게 시작 지점 설정
latest_round = start_round
while True:
    res = requests.get(f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={latest_round + 1}").json()
    if res.get("returnValue") == "fail":
        break
    latest_round += 1

# 2. 최근 10개 회차 가져오기
lotto_list = []
for i in range(latest_round, latest_round - 10, -1):
    data = get_lotto_data(i)
    if data:
        lotto_list.append(data)

# 3. JSON 파일로 저장
with open('lotto_recent_year.json', 'w', encoding='utf-8') as f:
    json.dump(lotto_list, f, ensure_ascii=False, indent=2)

print(f"성공적으로 {latest_round}회차부터 10개의 데이터를 업데이트했습니다.")
