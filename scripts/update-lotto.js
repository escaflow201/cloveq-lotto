import fs from "fs";

const filePath = "lotto_recent_year.json";

let data = [];
try {
  const raw = fs.readFileSync(filePath, "utf8").trim();
  data = raw ? JSON.parse(raw) : [];
} catch {
  data = [];
}

const lastRound = data.length > 0 ? data[data.length - 1].round : 0;
const nextRound = lastRound + 1;

console.log("마지막 저장 회차:", lastRound);
console.log("조회할 다음 회차:", nextRound);

const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${nextRound}`;

const res = await fetch(url, {
  headers: {
    "User-Agent": "Mozilla/5.0"
  }
});

const text = await res.text();
console.log("응답 앞부분:", text.slice(0, 80));

let json;
try {
  json = JSON.parse(text);
} catch {
  throw new Error("JSON 응답이 아니라서 파싱 실패");
}

if (json.returnValue !== "success") {
  console.log("아직 새 회차가 없거나 조회 실패");
  process.exit(0);
}

const exists = data.some(item => item.round === json.drwNo);
if (exists) {
  console.log("이미 저장된 회차라서 종료");
  process.exit(0);
}

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

fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf8");
console.log("JSON 업데이트 완료:", json.drwNo);
