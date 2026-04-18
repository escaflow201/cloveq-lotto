const fs = require("fs");

const FILE = "lotto_recent_year.json";

async function fetchRound(round) {
  const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;

  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0",
      "Accept": "application/json, text/plain, */*",
      "Referer": "https://www.dhlottery.co.kr/gameResult.do?method=byWin",
      "X-Requested-With": "XMLHttpRequest"
    }
  });

  const text = await res.text();

  if (text.trim().startsWith("<!DOCTYPE") || text.trim().startsWith("<html")) {
    throw new Error(`JSON 대신 HTML 응답이 왔어: ${text.slice(0, 120)}`);
  }

  const data = JSON.parse(text);

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

main().catch(err => {
  console.error(err);
  process.exit(1);
});
