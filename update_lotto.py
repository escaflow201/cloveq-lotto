import requests
import json
import re

def update_lotto_recent_year():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 1. 메인 페이지에서 최신 회차 가져오기 (더 안정적인 방법)
    main_url = "https://dhlottery.co.kr/common.do?method=main"
    resp = requests.get(main_url, headers=headers, timeout=15)
    html = resp.text
    
    # 정규식으로 최신 회차 추출 (id="lottoDrwNo" 패턴)
    match = re.search(r'id="lottoDrwNo">(\d+)', html)
    if not match:
        print("❌ 최신 회차를 찾을 수 없습니다. HTML 구조가 변경되었을 수 있습니다.")
        # 디버깅용: HTML 일부 저장
        with open('debug_main.html', 'w', encoding='utf-8') as f:
            f.write(html[:2000])
        return False
    
    latest = int(match.group(1))
    print(f"✅ 현재 최신 회차: {latest}회")
    
    results = []
    for i in range(54):  # 최근 1년 + 여유
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
                    "1등_당첨자수": data.get('firstPrzwnerCo')
                }
                results.append(lotto)
                print(f"{drw_no}회 저장 완료")
            else:
                print(f"{drw_no}회 데이터 없음")
                break
        except Exception as e:
            print(f"{drw_no}회 오류: {e}")
            break
    
    # JSON 저장
    with open('lotto_recent_year.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 완료! 총 {len(results)}회차 데이터가 lotto_recent_year.json에 저장되었습니다.")
    return True

if __name__ == "__main__":
    update_lotto_recent_year()
