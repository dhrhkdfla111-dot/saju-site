// 백엔드(ssaju) 연동 전 화면 확인용 더미 사주 데이터.
// 실제 계산 결과와 동일한 SajuResult 타입을 따른다. PART 2에서 실데이터로 교체.
import type { Category, SajuResult } from "@/lib/types";

export const dummySaju: SajuResult = {
  input: {
    year: 1995,
    month: 3,
    day: 12,
    hour: 14,
    minute: 20,
    gender: "여",
    calendar: "solar",
    leap: false,
  },
  hourUnknown: false,
  // 원국 8글자 (연/월/일/시)
  pillars: [
    { label: "연주", cheongan: "을", jiji: "해", sipseong: "편인", unseong: "사" },
    { label: "월주", cheongan: "기", jiji: "묘", sipseong: "편재", unseong: "병" },
    { label: "일주", cheongan: "정", jiji: "축", sipseong: "일간", unseong: "묘" },
    { label: "시주", cheongan: "정", jiji: "미", sipseong: "비견", unseong: "관대" },
  ],
  // 오행 분포 (백분율 합 100)
  ohaeng: { 목: 25, 화: 30, 토: 20, 금: 10, 수: 15 },
  sipseong: ["비견", "편재", "정재", "편관", "정인", "편인"],
  // 대운 (10년 단위) — score는 오행 균형 점수(단순화)
  daeun: [
    { age: 3, cheongan: "무", jiji: "인", score: 52 },
    { age: 13, cheongan: "정", jiji: "축", score: 60 },
    { age: 23, cheongan: "병", jiji: "자", score: 68 },
    { age: 33, cheongan: "을", jiji: "해", score: 74 },
    { age: 43, cheongan: "갑", jiji: "술", score: 65 },
    { age: 53, cheongan: "계", jiji: "유", score: 58 },
    { age: 63, cheongan: "임", jiji: "신", score: 55 },
    { age: 73, cheongan: "신", jiji: "미", score: 50 },
  ],
  // 세운 (최근 5년 + 향후 5년)
  seun: [
    { year: 2023, cheongan: "계", jiji: "묘", score: 62 },
    { year: 2024, cheongan: "갑", jiji: "진", score: 70 },
    { year: 2025, cheongan: "을", jiji: "사", score: 66 },
    { year: 2026, cheongan: "병", jiji: "오", score: 78 },
    { year: 2027, cheongan: "정", jiji: "미", score: 72 },
    { year: 2028, cheongan: "무", jiji: "신", score: 64 },
    { year: 2029, cheongan: "기", jiji: "유", score: 59 },
    { year: 2030, cheongan: "경", jiji: "술", score: 63 },
  ],
  gongmang: ["신", "유"],
};

// AI 총평/요약 더미 (톤 가이드 반영: 단정 금지, 근거 언급, 용어 괄호 설명)
export const dummyInterpretation = {
  summary:
    "일간이 정화(丁火, 촛불처럼 은근하고 지속적인 불)로, 겉으로 드러내기보다 안에서 꾸준히 데우는 기질이에요. 월지 묘목(卯木)이 일간을 생(生, 기운을 북돋움)해 주어 아이디어와 표현력이 풍부한 편입니다. 다만 화(火) 기운이 다소 강해, 한 번 몰입하면 페이스 조절이 필요한 시기가 올 수 있어요.",
  today: {
    총운: "새로운 제안에 마음이 열리는 날. 서두르기보다 하나씩 확인하며 결정하면 좋아요.",
    재물운: "예상치 못한 지출 가능성이 보이니, 큰 결제는 하루 미뤄 검토하는 편이 안정적이에요.",
    애정운: "말보다 행동으로 마음을 전할 때 진심이 잘 전달되는 흐름이에요.",
  },
};

// 분야별 심화 해석 더미 (카테고리별 톤 규칙 반영). PART 2에서 Claude API 결과로 교체.
export const dummyCategoryText: Record<Category, string> = {
  이직:
    "일간 정화(丁火)에 편재(偏財, 활동 무대를 넓히는 기운)가 함께 있어, 새로운 환경에서 오히려 감각이 살아나는 편이에요. 다가오는 병오년(丙午年)은 화 기운이 강해 의욕이 앞설 수 있으니, 이직은 준비를 갖춘 뒤 한 박자 늦춰 결정하면 더 안정적입니다. 조건 비교 리스트를 만들어 두는 걸 권해요.",
  사랑:
    "관계에서 표현을 아끼는 편이라, 상대가 마음을 늦게 알아챌 수 있어요(일간이 은근한 정화라 그렇습니다). 정재(正財)의 흐름이 들어오는 시기엔 안정적인 인연에 마음이 열리기 쉬우니, 조급함보다 꾸준함으로 다가가면 좋습니다. 단정 짓기보다 서로의 속도를 맞춰가는 게 핵심이에요.",
  금전:
    "재성(財星)이 뚜렷해 돈의 들고 남이 활발한 구조예요. 큰 흐름은 나쁘지 않지만, 화 기운이 강한 해엔 지출이 커지기 쉬우니 고정비를 먼저 점검하는 습관이 도움이 됩니다. 특정 투자를 권하기보다, 여유 자금 범위 안에서 분산해 관리하는 관점을 추천해요.",
  건강:
    "화 기운이 다소 강한 편이라, 과로가 누적되면 컨디션 기복으로 이어질 수 있어요. 특정 시기엔 특히 <b>체력 관리와 충분한 휴식</b>이 필요합니다. 규칙적인 수면과 수분 섭취처럼 기본을 지키는 것만으로도 흐름이 한결 편해져요. (진단이 아닌 참고용 안내입니다.)",
  지인:
    "사람을 끌어당기는 힘이 있어 인맥이 넓어지는 시기가 오는데, 그만큼 관계에 쓰는 에너지도 커질 수 있어요. 의견이 엇갈리기 쉬운 시기엔 한 발 물러서서 듣는 태도가 갈등을 줄여줍니다. 넓히기보다 깊이를 챙기는 쪽이 만족도가 높은 사주예요.",
};
