const fs = require("fs");
const fetch = require("node-fetch");

const FILE_PATH = "lotto_recent_year.json";

async function fetchLotto() {
  const results = [];

  for (let round = 1100; round <= 1300; round++) {
    try {
      const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;
      const res = await fetch(url);
      const data = await res.json();

      if (data.returnValue !== "success") continue;

      const numbers = [
        data.drwtNo1,
        data.drwtNo2,
        data.drwtNo3,
        data.drwtNo4,
        data.drwtNo5,
        data.drwtNo6,
      ];

      results.push({
        round: data.drwNo,
        draw_date: data.drwNoDate,
        numbers: numbers,
        bonus: data.bnusNo,
        numbers_text: numbers.join(", "),
        sum: numbers.reduce((a, b) => a + b, 0),
        odd_count: numbers.filter(n => n % 2 !== 0).length,
      });

    } catch (e) {
      console.log("에러:", round);
    }
  }

  return results;
}

async function run() {
  const newData = await fetchLotto();

  // 🔥 핵심: 데이터 없으면 절대 덮어쓰기 금지
  if (!Array.isArray(newData) || newData.length === 0) {
    console.log("❌ 데이터 0개 → 기존 JSON 보호 (저장 안함)");
    return;
  }

  // 기존 데이터 읽기
  let oldData = [];
  if (fs.existsSync(FILE_PATH)) {
    try {
      oldData = JSON.parse(fs.readFileSync(FILE_PATH, "utf8"));
    } catch (e) {
      console.log("기존 파일 깨짐 → 무시");
    }
  }

  // 중복 제거 (round 기준)
  const merged = [...oldData];

  newData.forEach(item => {
    if (!merged.find(x => x.round === item.round)) {
      merged.push(item);
    }
  });

  // 최신순 정렬
  merged.sort((a, b) => b.round - a.round);

  fs.writeFileSync(FILE_PATH, JSON.stringify(merged, null, 2), "utf8");

  console.log("✅ 업데이트 완료:", merged.length, "개");
}

run();
