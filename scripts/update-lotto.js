import fs from "fs";

const results = [];
const startRound = 1100;
const endRound = 1200;

for (let round = startRound; round <= endRound; round++) {
  const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;

  try {
    const res = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*"
      }
    });

    const text = await res.text();
    console.log(`round=${round}, status=${res.status}, body_start=${text.slice(0, 80)}`);

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      console.log(`JSON 파싱 실패: ${round}회`);
      continue;
    }

    if (data.returnValue !== "success") {
      console.log(`success 아님: ${round}회`, data);
      continue;
    }

    results.push({
      round: data.drwNo,
      date: data.drwNoDate,
      numbers: [
        data.drwtNo1,
        data.drwtNo2,
        data.drwtNo3,
        data.drwtNo4,
        data.drwtNo5,
        data.drwtNo6
      ],
      bonus: data.bnusNo
    });
  } catch (e) {
    console.log(`에러: ${round}회`, e.message);
  }
}

if (results.length === 0) {
  throw new Error("로또 데이터를 하나도 가져오지 못함");
}

fs.writeFileSync(
  "lotto_recent_year.json",
  JSON.stringify(results, null, 2),
  "utf8"
);

console.log(`${results.length}개 저장 완료`);
