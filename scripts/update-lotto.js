import fs from "fs";

const results = [];

for (let round = 1100; round <= 1200; round++) {
  try {
    const res = await fetch(`https://api.allorigins.win/raw?url=https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`);
    const data = await res.json();

    if (data.returnValue !== "success") continue;

    results.push({
      round: data.drwNo,
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
    console.log("에러:", round);
  }
}

if (results.length === 0) {
  throw new Error("데이터 못 가져옴");
}

fs.writeFileSync("lotto_recent_year.json", JSON.stringify(results, null, 2));
