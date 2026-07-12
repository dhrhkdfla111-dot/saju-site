// 사주 캐시 키 생성 — 원국 8글자 조합(+성별)으로 고유 키를 만든다.
import type { Pillar } from "@/lib/types";

/** 원국 8글자 문자열 (연간·연지·월간·월지·일간·일지·시간·시지) */
export function buildEightChars(pillars: Pick<Pillar, "cheongan" | "jiji">[]): string {
  return pillars.map((p) => `${p.cheongan}${p.jiji}`).join("");
}

/**
 * 캐시 키: 원국 8글자 + 성별.
 * 카테고리는 별도 컬럼으로 관리하므로 키에 포함하지 않는다.
 */
export function buildSajuKey(
  pillars: Pick<Pillar, "cheongan" | "jiji">[],
  gender: string
): string {
  return `${buildEightChars(pillars)}|${gender}`;
}
