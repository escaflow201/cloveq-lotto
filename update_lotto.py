import urllib.request
import json
import time

def run():
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    results = []
    # 2026년 기준 안전한 회차
    start_round = 1218

    print("--- 신규 스크립트 실행 (urllib 버전) ---")
    for i in range(5): # 테스트를 위해 5개만 먼저 시도
        target = start_round - i
        try:
            req = urllib.request.Request(url + str(target), headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                if data.get("returnValue") == "success":
                    results.append({"round": data["drwNo"], "numbers": [data[f"drwtNo{n}"] for n in range(1,7)]})
                    print(f"{target}회 성공")
        except: pass
        time.sleep(0.5)

    with open("lotto_recent_year.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("--- 저장 완료 ---")

if __name__ == "__main__":
    run()
