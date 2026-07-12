// Claude 해석 생성용 프롬프트 빌더.
// 톤 가이드(필수)와 카테고리별 규칙을 시스템/유저 프롬프트에 반드시 포함한다.
import type { Category, Pillar } from "@/lib/types";

/** API로 넘어오는 사주 컴팩트 데이터 (toCompact 대응) */
export interface SajuCompact {
  pillars: Pick<Pillar, "label" | "cheongan" | "jiji" | "sipseong">[];
  ilgan?: string; // 일간 (없으면 일주 천간에서 유추)
  ohaeng?: Record<string, number>; // 오행 분포
  gender: string;
  hourUnknown?: boolean;
}

// 공통 톤 가이드 (모든 카테고리 공통 — 필수 반영)
const TONE_GUIDE = `[톤 가이드 — 반드시 지킬 것]
- 불안을 조장하는 단정적 표현 금지 ("망한다", "큰 사고 난다", "실패한다" 등 금지).
- 리스크는 반드시 "대비 가능한 정보"로 전환해 서술한다 (예: "이 시기엔 신중한 결정이 필요해요" O / "이 시기에 사고 난다" X).
- 전문용어(십성, 신살, 12운성, 오행 등)를 쓸 때는 반드시 괄호로 짧은 설명을 병기한다.
- 누구에게나 적용될 뻔한 문장은 금지. 반드시 이 사주의 구체적 조합(일간, 오행 균형 등)을 근거로 언급한다.
- 따뜻하고 담백한 존댓말. 2~4문단, 과장·이모지 없이.`;

// 건강 카테고리 추가 안전 규칙
const HEALTH_GUARD = `[건강 카테고리 특별 규칙]
- 질병명·진단명 절대 언급 금지.
- "체력 관리가 필요한 시기", "휴식과 규칙적인 생활이 도움이 되는 흐름" 같은 완곡한 표현만 사용.
- 의료 행위를 대체하지 않는 참고용 정보임을 자연스럽게 전제한다.`;

// 카테고리별 관점 규칙
const CATEGORY_RULES: Record<Category, string> = {
  이직: "직업·이직 관점. 시기 판단을 중심으로, 무모한 결정을 부추기지 말 것.",
  사랑: "애정·관계 관점. 성향과 궁합 포인트를 짚되 단정 짓지 말 것.",
  금전: "재물 관점. 리스크 관리 중심으로, 특정 투자를 권유하는 표현 금지.",
  건강: `건강 관점. ${HEALTH_GUARD}`,
  지인: "인간관계·지인 관점. 관계의 흐름과 갈등 시기 주의 정도로 서술.",
};

/** 사주 요약을 사람이 읽는 문자열로 */
function describeSaju(s: SajuCompact): string {
  const ilgan = s.ilgan ?? s.pillars.find((p) => p.label === "일주")?.cheongan ?? "";
  const pillarStr = s.pillars
    .map((p) => `${p.label} ${p.cheongan}${p.jiji}${p.sipseong ? `(${p.sipseong})` : ""}`)
    .join(", ");
  const ohaengStr = s.ohaeng
    ? Object.entries(s.ohaeng)
        .map(([k, v]) => `${k} ${v}%`)
        .join(", ")
    : "정보 없음";
  return [
    `- 일간(日干, 사주의 주체): ${ilgan}`,
    `- 원국: ${pillarStr}`,
    `- 오행 분포: ${ohaengStr}`,
    `- 성별: ${s.gender}`,
    s.hourUnknown ? "- 출생 시각 미상(시주 제외, 연·월·일주 기준)" : "",
  ]
    .filter(Boolean)
    .join("\n");
}

/** 시스템 프롬프트 (톤 가이드는 시스템에 고정) */
export const SYSTEM_PROMPT = `너는 전통 명리학에 정통한 상담가야. 데이터에 기반해 정갈하고 신뢰감 있게, 그러나 따뜻하게 사주를 풀이해.
${TONE_GUIDE}`;

/** 카테고리 심화 해석용 유저 프롬프트 */
export function buildCategoryPrompt(saju: SajuCompact, category: Category): string {
  return `아래 사주 데이터를 근거로 '${category}' 분야의 심화 해석을 작성해줘.

[사주 데이터]
${describeSaju(saju)}

[이 카테고리 규칙]
${CATEGORY_RULES[category]}

위 톤 가이드와 카테고리 규칙을 모두 지켜, 이 사주만의 구체적 근거(일간·오행 균형 등)를 들어 2~4문단으로 작성해줘. 서두·맺음의 상투적 인사말 없이 본문만.`;
}

/** 총평(성격/기질) 유저 프롬프트 */
export function buildSummaryPrompt(saju: SajuCompact): string {
  return `아래 사주 데이터를 근거로 성격과 기질에 대한 '총평'을 작성해줘.

[사주 데이터]
${describeSaju(saju)}

일간의 특성과 오행 균형을 근거로, 이 사람만의 기질을 2~3문단으로. 톤 가이드를 반드시 지키고 본문만 작성해줘.`;
}
