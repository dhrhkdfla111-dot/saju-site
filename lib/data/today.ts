// 오늘의 운세 — 일간 12개 그룹(실제 명리는 10천간이나, 콘텐츠 편의상 대표 12지 동물 그룹으로 구성).
// 매일 갱신 콘셉트: 백엔드 연동 전이므로 날짜 시드로 더미 문구를 선택한다.

export interface TodayGroup {
  slug: string;
  emoji: string;
  name: string; // 그룹명(띠)
  lines: string[]; // 회전 문구 풀
}

export const todayGroups: TodayGroup[] = [
  { slug: "rat", emoji: "🐭", name: "쥐띠", lines: ["새로운 정보에 귀가 밝아지는 하루. 메모하는 습관이 도움이 돼요.", "작은 지출을 점검하기 좋은 날이에요."] },
  { slug: "ox", emoji: "🐮", name: "소띠", lines: ["꾸준함이 빛을 보는 흐름. 서두르지 않아도 괜찮아요.", "믿을 만한 사람과의 대화에서 실마리를 얻어요."] },
  { slug: "tiger", emoji: "🐯", name: "호랑이띠", lines: ["추진력이 살아나는 날. 다만 한 박자 늦춰 결정하면 더 안정적이에요.", "운동이나 산책으로 컨디션을 챙겨보세요."] },
  { slug: "rabbit", emoji: "🐰", name: "토끼띠", lines: ["표현력이 좋은 하루. 마음을 말로 전하기 좋은 흐름이에요.", "예상 밖 제안이 들어올 수 있어요."] },
  { slug: "dragon", emoji: "🐲", name: "용띠", lines: ["큰 그림을 그리기 좋은 날. 세부는 내일 다듬어도 돼요.", "주변의 신뢰가 힘이 되는 흐름이에요."] },
  { slug: "snake", emoji: "🐍", name: "뱀띠", lines: ["직관이 예리해지는 하루. 첫 느낌을 메모해 두세요.", "휴식과 집중의 균형이 중요해요."] },
  { slug: "horse", emoji: "🐴", name: "말띠", lines: ["활동 반경이 넓어지는 날. 무리한 일정은 조율이 필요해요.", "새로운 인연이 스칠 수 있어요."] },
  { slug: "goat", emoji: "🐑", name: "양띠", lines: ["부드러운 조율이 통하는 하루. 갈등은 한 발 물러서면 풀려요.", "취향에 맞는 소비가 기분을 살려줘요."] },
  { slug: "monkey", emoji: "🐵", name: "원숭이띠", lines: ["아이디어가 반짝이는 날. 기록해 두면 나중에 쓰임이 있어요.", "협업에서 좋은 시너지가 나요."] },
  { slug: "rooster", emoji: "🐔", name: "닭띠", lines: ["꼼꼼함이 강점이 되는 하루. 마무리 점검에 유리해요.", "건강 신호에 귀 기울이면 좋아요."] },
  { slug: "dog", emoji: "🐶", name: "개띠", lines: ["신뢰가 두터워지는 흐름. 약속을 지키는 것이 큰 자산이 돼요.", "가까운 사람과의 시간이 힘이 돼요."] },
  { slug: "pig", emoji: "🐷", name: "돼지띠", lines: ["여유가 생기는 하루. 베푼 만큼 돌아오는 흐름이에요.", "재물의 들고 남을 정리하기 좋아요."] },
];

// 날짜를 시드로 오늘의 문구 하나를 고정 선택 (같은 날엔 동일 결과)
export function lineForToday(g: TodayGroup, date = new Date()): string {
  const seed = date.getFullYear() * 1000 + (date.getMonth() + 1) * 50 + date.getDate();
  return g.lines[seed % g.lines.length];
}
