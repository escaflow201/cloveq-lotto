import fs from "fs";

const FILE_PATH = "lotto_recent_year.json";

function readLocalJson() {
  try {
    const raw = fs.readFileSync(FILE_PATH, "utf8").trim();
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeLocalJsonSafe(data) {
  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("가져온 결과가 0개라서 기존 JSON을 덮어쓰지 않음");
  }

  fs.writeFileSync(FILE_PATH, JSON.stringify(data, null, 2), "utf8");
}

function normalizeRoundItem(json) {
  return {
    round: Number(json.drwNo),
    date: json.drwNoDate,
    numbers: [
      Number(json.drwtNo1),
      Number(json.drwtNo2),
      Number(json.drwtNo3),
      Number(json.drwtNo4),
      Number(json.drwtNo5),
      Number(json.drwtNo6)
    ].sort((a, b) => a - b),
    bonus: Number(json.bnusNo)
  };
}

async function fetchRound(round) {
  const url = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;

  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0",
      "Accept": "application/json, text/plain, */*"
    }
  });

  const text = await res.text();
  console.log(`조회한 다음 회차: ${round}`);
  console.log(`응답 상태 코드: ${res.status}`);
  console.log(`응답 앞부분: ${text.slice(0, 80)}`);

  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error("JSON 응답이 아니라서 파싱 실패");
  }

  if (json.returnValue !== "success") {
    throw new Error("해당 회차 데이터가 아직 없거나 조회 실패");
  }

  return normalizeRoundItem(json);
}

async function main() {
  const localData = readLocalJson();
  console.log(`기존 데이터 개수: ${localData.length}`);

  const lastRound =
    localData.length > 0
      ? Number(localData[localData.length - 1].round)
      : 0;

  const nextRound = lastRound + 1;

  console.log(`마지막 저장 회차: ${lastRound}`);
  console.log(`조회할 다음 회차: ${nextRound}`);

  try {
    const latest = await fetchRound(nextRound);

    const exists = localData.some(item => Number(item.round) === Number(latest.round));
    if (exists) {
      console.log(`이미 ${latest.round}회가 있어서 저장 안 함`);
      process.exit(0);
    }

    const merged = [...localData, latest];
    writeLocalJsonSafe(merged);

    console.log(`JSON 업데이트 완료: ${latest.round}회 추가`);
  } catch (err) {
    console.log(`업데이트 생략: ${err.message}`);
    console.log("기존 JSON 유지");
    process.exit(0);
  }
}

main().catch(err => {
  console.error("치명적 오류:", err.message);
  process.exit(1);
});
