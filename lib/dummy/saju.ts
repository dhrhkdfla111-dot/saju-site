// 백엔드(ssaju) 연동 전 화면 확인용 더미 사주 데이터.
// 실제 계산 결과와 동일한 SajuResult 타입을 따른다. PART 2에서 실데이터로 교체.
import type { SajuResult } from "@/lib/types";

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
