import requests
import json

def get_latest_lotto_10():
    # 1. 메인 페이지에서 최신 회차 가져오기
    main_url = "https://dhlottery.co.kr/common.do?method=main"
    resp = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})
    
    # 최신 회차 파싱 (id="lottoDrwNo" 부분)
    html = resp.text
    latest = int(html.split('id="lottoDrwNo">')[1].split('<')[0])
    
    results = []
    print(f"최신 회차: {latest}회 (2026-04-18 기준)")
    
    # 최신 10회차 루프
    for drw_no in range(latest, latest - 10, -1):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
        data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        
        if data.get('returnValue') == 'success':
            lotto = {
                "회차": data['drwNo'],
                "추첨일": data['drwNoDate'],
                "번호": [data[f'drwtNo{i}'] for i in range(1,7)],
                "보너스": data['bnusNo'],
                "1등_당첨금": data.get('firstWinamnt'),
                "1등_당첨자수": data.get('firstPrzwnerCo')
            }
            results.append(lotto)
            print(f"{drw_no}회: {lotto['번호']} + {lotto['보너스']}")
    
    # JSON 파일로 저장
    with open('latest_lotto_10.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

# 실행
data = get_latest_lotto_10()
