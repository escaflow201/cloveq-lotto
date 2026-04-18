
import fs from "fs";

const results = [];

for (let round = 1100; round <= 1200; round++) {
  try {
    const res = await fetch(`https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`, {
      headers: {
        "User-Agent": "Mozilla/5.0"
      }
    });

    const data = await res.json();

    if (data.returnValue !== "success") continue;

    results.push({
      round,
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

fs.writeFileSync("lotto_recent_year.json", JSON.stringify(results, null, 2));
