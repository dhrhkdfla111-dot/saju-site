// Supabase 서버 전용 클라이언트 (service_role 키 사용 — 절대 클라이언트에 노출 금지).
// 해석 캐시 테이블(interpretations) 접근에만 사용한다.
import { createClient, type SupabaseClient } from "@supabase/supabase-js";

let cached: SupabaseClient | null = null;

/**
 * 환경변수가 설정된 경우에만 클라이언트를 생성해 반환.
 * 미설정 시 null → 호출부에서 캐시 없이 동작(그레이스풀 폴백).
 */
export function getSupabase(): SupabaseClient | null {
  if (cached) return cached;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !serviceKey) return null;
  cached = createClient(url, serviceKey, {
    auth: { persistSession: false },
  });
  return cached;
}
