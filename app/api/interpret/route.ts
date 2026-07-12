// POST /api/interpret
// 1) 원국 데이터 + category 수신
// 2) Supabase interpretations 테이블에서 (saju_key, category) 캐시 조회
// 3) 있으면 즉시 반환
// 4) 없으면 Claude API로 해석 생성 → 저장 → 반환
//
// Claude 호출은 서버(이 라우트)에서만. 키는 클라이언트에 노출되지 않는다.
import { NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { getSupabase } from "@/lib/supabase";
import { buildSajuKey } from "@/lib/saju/key";
import {
  SYSTEM_PROMPT,
  buildCategoryPrompt,
  buildSummaryPrompt,
  type SajuCompact,
} from "@/lib/prompt";
import type { Category } from "@/lib/types";

export const runtime = "nodejs";

// 해석 생성 모델 — 캐싱 전제의 대량 생성이라 비용 효율적인 Haiku 사용.
const MODEL = "claude-haiku-4-5-20251001";
const CATEGORIES: Category[] = ["이직", "사랑", "금전", "건강", "지인"];

interface InterpretBody {
  saju: SajuCompact;
  category: Category | "총평";
}

export async function POST(req: Request) {
  let body: InterpretBody;
  try {
    body = (await req.json()) as InterpretBody;
  } catch {
    return NextResponse.json({ error: "잘못된 요청 형식입니다." }, { status: 400 });
  }

  const { saju, category } = body;

  // 입력 검증
  if (!saju?.pillars?.length || !category) {
    return NextResponse.json(
      { error: "saju(원국 데이터)와 category가 필요합니다." },
      { status: 400 }
    );
  }
  if (category !== "총평" && !CATEGORIES.includes(category)) {
    return NextResponse.json({ error: "알 수 없는 category입니다." }, { status: 400 });
  }

  const sajuKey = buildSajuKey(saju.pillars, saju.gender ?? "");
  const supabase = getSupabase();

  // 2~3) 캐시 조회
  if (supabase) {
    const { data, error } = await supabase
      .from("interpretations")
      .select("interpretation_text")
      .eq("saju_key", sajuKey)
      .eq("category", category)
      .maybeSingle();
    // 테이블 미생성 등 오류는 캐시 없이 계속 진행(그레이스풀)
    if (!error && data?.interpretation_text) {
      return NextResponse.json({ text: data.interpretation_text, cached: true });
    }
  }

  // 4) Claude 호출
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "서버에 ANTHROPIC_API_KEY가 설정되지 않았습니다." },
      { status: 500 }
    );
  }

  const client = new Anthropic({ apiKey });
  const prompt =
    category === "총평"
      ? buildSummaryPrompt(saju)
      : buildCategoryPrompt(saju, category);

  let text: string;
  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 1200,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: prompt }],
    });
    // 안전: 거부 등 비정상 응답 처리
    if (message.stop_reason === "refusal") {
      return NextResponse.json(
        { error: "해석 생성이 거부되었습니다. 잠시 후 다시 시도해주세요." },
        { status: 422 }
      );
    }
    text = message.content
      .filter((b): b is Anthropic.TextBlock => b.type === "text")
      .map((b) => b.text)
      .join("\n")
      .trim();
  } catch (e) {
    // 서버 로그에 실제 원인을 남긴다(클라이언트에는 일반 메시지만 반환).
    const detail = e instanceof Anthropic.APIError ? `${e.status} ${e.message}` : String(e);
    console.error("[/api/interpret] Claude 호출 실패:", detail);
    const status =
      e instanceof Anthropic.APIError && typeof e.status === "number" ? e.status : 500;
    return NextResponse.json(
      { error: "해석 생성 중 오류가 발생했습니다." },
      { status: status >= 500 ? 502 : status }
    );
  }

  if (!text) {
    return NextResponse.json({ error: "빈 해석이 반환되었습니다." }, { status: 502 });
  }

  // 저장(캐시). 실패해도 응답은 정상 반환.
  if (supabase) {
    await supabase
      .from("interpretations")
      .upsert(
        { saju_key: sajuKey, category, interpretation_text: text },
        { onConflict: "saju_key,category" }
      );
  }

  return NextResponse.json({ text, cached: false });
}
