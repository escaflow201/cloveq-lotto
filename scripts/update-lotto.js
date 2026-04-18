const fs = require("fs");

const FILE = "lotto_recent_year.json";

async function fetchAllRounds() {
  const url = "https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do?srchLtEpsd=all";

  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0",
      "Accept": "application/json, text/plain, */*",
      "X-Requested-With": "XMLHttpRequest",
      "Referer": "https://www.dhlottery.co.kr/lt645/result"
    }
  });

  const text = await res.text();

  if (text.trim().startsWith("<!DOCTYPE") || text.trim().startsWith("<html")) {
    throw new Error("JSON 대신 HTML이 왔어.");
  }

  const json = JSON.parse(text);

  // 응답 구조에 따라 data 또는 data.list 둘 다 대응
  const rows = Array.isArray(json?.data)
    ? json.data
    : Array.isArray(json?.data?.list)
    ? json.data.list
    : [];

  if (!rows.length) {
    throw new Error("회차 데이터가 비어 있어.");
  }

  return rows;
}

function toAppRow(row) {
  return {
    round: Number(row.ltEpsd ?? row.drwNo ?? row.round),
    draw_date: String(row.ltRflYmd ?? row.drwNoDate ?? row.draw_date ?? ""),
    numbers: [
      Number(row.tm1WnNo ?? row.drwtNo1),
      Number(row.tm2WnNo ?? row.drwtNo2),
      Number(row.tm3WnNo ?? row.drwtNo3),
      Number(row.tm4WnNo ?? row.drwtNo4),
      Number(row.tm5WnNo ?? row.drwtNo5),
      Number(row.tm6WnNo ?? row.drwtNo6)
    ].filter(Number.isFinite),
    bonus: Number(row.bnusNo ?? row.bonus)
  };
}

async function main() {
  const rows = await fetchAllRounds();

  const list = rows
    .map(toAppRow)
    .filter(v => v.round && v.numbers.length === 6 && Number.isFinite(v.bonus))
    .sort((a, b) => a.round - b.round);

  fs.writeFileSync(FILE, JSON.stringify(list, null, 2), "utf8");
  console.log(`업데이트 완료: ${list.length}개`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
