const fs = require("fs");

const FILE = "lotto_recent_year.json";
const MAX_LOOKAHEAD = 3; // 최신 회차 이후 몇 번 더 확인할지

async function fetchRound(round) {
  const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;

  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0",
      "Accept": "application/json, text/plain, */*"
    },
    cache: "no-store"
  });

  const text = await res.text();

  if (text.trim().startsWith("<!DOCTYPE") || text.trim().startsWith("<html")) {
    throw new Error(`회차 ${round}: JSON 대신 HTML 응답이 왔어.`);
  }

  const data = JSON.parse(text);

  if (data.returnValue !== "success") {
    return null;
  }

  return {
    round: Number(data.drwNo),
    draw_date: String(data.drwNoDate || ""),
    numbers: [
      Number(data.drwtNo1),
      Number(data.drwtNo2),
      Number(data.drwtNo3),
      Number(data.drwtNo4),
      Number(data.drwtNo5),
      Number(data.drwtNo6)
    ],
    bonus: Number(data.bnusNo)
  };
}

function isValidRow(row) {
  return (
    row &&
    Number.isInteger(row.round) &&
    row.round > 0 &&
    Array.isArray(row.numbers) &&
    row.numbers.length === 6 &&
    row.numbers.every(n => Number.isInteger(n) && n >= 1 && n <= 45) &&
    Number.isInteger(row.bonus) &&
    row.bonus >= 1 &&
    row.bonus <= 45
  );
}

function loadExisting() {
  if (!fs.existsSync(FILE)) return [];

  const raw = fs.readFileSync(FILE, "utf8").trim();
  if (!raw) return [];

  const json = JSON.parse(raw);
  if (!Array.isArray(json)) return [];

  return json.filter(isValidRow);
}

async function main() {
  const existing = loadExisting();
  const map = new Map(existing.map(row => [row.round, row]));

  let startRound = 1;
  if (existing.length) {
    startRound = Math.max(...existing.map(v => v.round)) + 1;
  }

  let missCount = 0;
  let round = startRound;

  while (missCount < MAX_LOOKAHEAD) {
    const row = await fetchRound(round);

    if (row) {
      map.set(row.round, row);
      missCount = 0;
    } else {
      missCount += 1;
    }

    round += 1;
  }

  const list = [...map.values()]
    .filter(isValidRow)
    .sort((a, b) => a.round - b.round);

  fs.writeFileSync(FILE, JSON.stringify(list, null, 2), "utf8");
  console.log(`업데이트 완료: ${list.length}개 회차 저장`);
  if (list.length) {
    console.log(`최신 회차: ${list[list.length - 1].round}`);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
