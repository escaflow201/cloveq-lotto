const fs = require("fs");

const FILE = "lotto_recent_year.json";

async function fetchRound(round) {
  const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;
  const res = await fetch(url);
  const data = await res.json();
  if (data.returnValue !== "success") return null;

  return {
    drwNo: data.drwNo,
    drwNoDate: data.drwNoDate,
    numbers: [
      data.drwtNo1,
      data.drwtNo2,
      data.drwtNo3,
      data.drwtNo4,
      data.drwtNo5,
      data.drwtNo6
    ],
    bonus: data.bnusNo
  };
}

async function main() {
  let list = [];
  if (fs.existsSync(FILE)) {
    list = JSON.parse(fs.readFileSync(FILE, "utf8"));
  }

  const lastRound = list.length ? Math.max(...list.map(v => v.drwNo)) : 1;

  let nextRound = lastRound + 1;

  while (true) {
    const row = await fetchRound(nextRound);
    if (!row) break;
    list.push(row);
    nextRound++;
  }

  list.sort((a, b) => a.drwNo - b.drwNo);
  fs.writeFileSync(FILE, JSON.stringify(list, null, 2), "utf8");

  console.log("업데이트 완료");
}

main();
