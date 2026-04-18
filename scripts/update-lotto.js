const fs = require("fs");

const FILE = "lotto_recent_year.json";

async function fetchAllRounds() {
  const url = "https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do?srchLtEpsd=all";

  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
      "Accept": "application/json, text/plain, */*",
      "X-Requested-With": "XMLHttpRequest",
      "Referer": "https://www.dhlottery.co.kr/lt645/result"
    }
  });

  const text = await res.text();

  if (text.trim().startsWith("<!DOCTYPE") || text.trim().startsWith("<html")) {
    throw new Error(`JSON 대신 HTML 응답이 왔어: ${text.slice(0, 200)}`);
  }

  const json = JSON.parse(text);

if (!json || !Array.isArray(json.data)) {
  throw new Error("응답 구조 이상");
}

  return json.data;
}

function convertRow(row) {
  return {
    drwNo: Number(row.ltEpsd),
    drwNoDate: row.ltRflYmd,
    numbers: [
      Number(row.tm1WnNo),
      Number(row.tm2WnNo),
      Number(row.tm3WnNo),
      Number(row.tm4WnNo),
      Number(row.tm5WnNo),
      Number(row.tm6WnNo)
    ],
    bonus: Number(row.bnusNo)
  };
}

async function main() {
  const rows = await fetchAllRounds();

  const list = rows
    .map(convertRow)
    .filter(v =>
      Number.isFinite(v.drwNo) &&
      v.numbers.every(Number.isFinite) &&
      Number.isFinite(v.bonus)
    )
    .sort((a, b) => a.drwNo - b.drwNo);

  fs.writeFileSync(FILE, JSON.stringify(list, null, 2), "utf8");
  console.log(`업데이트 완료: ${list.length}개 회차 저장`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
