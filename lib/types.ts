// 사주 계산/해석 관련 공통 타입 정의 (백엔드 연동 전 더미 데이터도 이 타입을 따른다)

export type Gender = "남" | "여";
export type CalendarType = "solar" | "lunar";

/** 홈 입력 폼에서 수집하는 값 */
export interface BirthInput {
  year: number;
  month: number;
  day: number;
  hour?: number; // 모름 시 생략 → 시주 제외
  minute?: number;
  gender: Gender;
  calendar: CalendarType;
  leap: boolean; // 음력 윤달 여부
}

/** 천간·지지 한 기둥(주) */
export interface Pillar {
  label: string; // 연주/월주/일주/시주
  cheongan: string; // 천간 (예: 을)
  jiji: string; // 지지 (예: 해)
  sipseong?: string; // 십성
  unseong?: string; // 12운성
}

/** 오행 분포 (목/화/토/금/수) */
export interface OhaengDistribution {
  목: number;
  화: number;
  토: number;
  금: number;
  수: number;
}

/** 대운 한 구간(10년) */
export interface Daeun {
  age: number; // 시작 나이
  cheongan: string;
  jiji: string;
  score: number; // 오행 균형 점수(단순화) — 차트용
}

/** 세운 한 해 */
export interface Seun {
  year: number;
  cheongan: string;
  jiji: string;
  score: number;
}

/** 사주 계산 결과 전체 (ssaju 출력 매핑) */
export interface SajuResult {
  input: BirthInput;
  hourUnknown: boolean; // 시주 제외 여부
  pillars: Pillar[]; // 원국 (연/월/일/시)
  ohaeng: OhaengDistribution;
  sipseong: string[]; // 십성 목록
  daeun: Daeun[];
  seun: Seun[];
  gongmang: string[]; // 공망
}

export type Category = "이직" | "사랑" | "금전" | "건강" | "지인";

/** 용어 사전 항목 */
export interface DictTerm {
  slug: string;
  term: string; // 용어명
  group: "천간" | "지지" | "십성" | "12운성" | "신살" | "기타";
  short: string; // 한 줄 요약
  body: string; // 상세 설명
}
