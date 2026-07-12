-- 해석 결과 캐시 테이블.
-- Supabase 대시보드 → SQL Editor에 붙여넣어 1회 실행하세요.

create table if not exists public.interpretations (
  id                  bigint generated always as identity primary key,
  saju_key            text        not null,   -- 원국 8글자 + 성별
  category            text        not null,   -- 이직/사랑/금전/건강/지인/총평
  interpretation_text text        not null,
  created_at          timestamptz not null default now(),
  unique (saju_key, category)
);

-- 조회 성능용 인덱스
create index if not exists interpretations_key_cat_idx
  on public.interpretations (saju_key, category);

-- service_role 키로만 접근하므로 RLS는 켜두고 별도 정책은 두지 않는다
-- (service_role은 RLS를 우회함). 클라이언트(anon)는 접근 불가.
alter table public.interpretations enable row level security;
