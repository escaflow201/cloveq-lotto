import fs from "fs";

const filePath = "lotto_recent_year.json";

let data = [];
try {
  data = JSON.parse(fs.readFileSync(filePath, "utf8"));
} catch {}

const lastRound = data.length > 0 ? data[data.length - 1].round : 1100;
const nextRound = lastRound + 1;

console.log("다음 회차:", nextRound);

const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${nextRound}`;

try {
  const res = await fetch(url, {
    headers: { "User-Agent": "Mozilla/5.0" }
  });

  const text = await res.text();

  if (!text.includes("drwtNo1")) {
    throw new Error("아직 추첨 안됨");
  }

  const json = JSON.parse(text);

  data.push({
    round: json.drwNo,
    date: json.drwNoDate,
    numbers: [
      json.drwtNo1,
      json.drwtNo2,
      json.drwtNo3,
      json.drwtNo4,
      json.drwtNo5,
      json.drwtNo6
    ],
    bonus: json.bnusNo
  });

  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  console.log("추가 완료");

} catch (e) {
  console.log("추첨 아직 안됨 or 실패");
}
