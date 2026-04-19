import requests
import json
from datetime import datetime

def update_lotto_recent_year():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 최신 회차 가져오기
    main_url = "https://dhlottery.co.kr/common.do?method=main"
    resp = requests.get(main_url, headers=headers)
    html = resp.text
    
    try:
        latest = int(html.split('id="lottoDrwNo">')[1].split('<')[0])
    except:
        print("최신 회차를 가져오는데 실패했습니다.")
        return False
    
    results = []
    print(f"최신 회차: {latest}회")
    print("최근 1년 데이터 수집 중...\n")
    
    # 최근 54회차 (1년 + 여유분)
    for i in range(54):
        drw_no = latest - i
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
        
        try:
            data = requests.get(url, headers=headers, timeout=10).json()
            
            if data.get('returnValue') == 'success':
                lotto = {
                    "회차": data['drwNo'],
                    "추첨일": data['drwNoDate'],
                    "번호": [data[f'drwtNo{i}'] for i in range(1, 7)],
                    "보너스": data['bnusNo'],
                    "1등_당첨금": data.get('firstWinamnt'),
                    "1등_당첨자수": data.get('firstPrzwnerCo'),
                    "총판매금액": data.get('totSellamnt')
                }
                results.append(lotto)
                print(f"{drw_no}회 저장 완료")
            else:
                break
        except:
            print(f"{drw_no}회 데이터 가져오기 실패")
            break
    
    # JSON 파일로 저장 (항상 같은 파일명으로 덮어쓰기)
    with open('lotto_recent_year.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 완료! 총 {len(results)}회차 데이터가 lotto_recent_year.json에 저장되었습니다.")
    return True

if __name__ == "__main__":
    update_lotto_recent_year()
