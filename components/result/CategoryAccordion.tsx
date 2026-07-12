"use client";

// 분야별 심화 해석 — 버튼 5개(이직/사랑/금전/건강/지인).
// 변경: 결과 로딩 시 전체 사전 생성(X) → 사용자가 버튼을 클릭하는 순간에만
//       해당 카테고리 하나를 /api/interpret로 생성한다.
//   클릭 → (이미 받은 값 있으면 즉시 표시) → 없으면 API 호출 → 스피너 → 결과 표시
import { useState } from "react";
import Icon from "@/components/ui/Icon";
import type { SajuCompact } from "@/lib/prompt";
import type { Category } from "@/lib/types";

const categories: { key: Category; desc: string }[] = [
  { key: "이직", desc: "시기 판단 중심" },
  { key: "사랑", desc: "성향·궁합 포인트" },
  { key: "금전", desc: "리스크 관리 관점" },
  { key: "건강", desc: "체력 관리 안내" },
  { key: "지인", desc: "인간관계 흐름" },
];

type Status = "idle" | "loading" | "done" | "error";
interface CatState {
  status: Status;
  text?: string;
  error?: string;
}

export default function CategoryAccordion({ saju }: { saju: SajuCompact }) {
  const [open, setOpen] = useState<Category | null>(null);
  // 카테고리별 상태(클라이언트 캐시 역할 — 한 번 받은 해석은 다시 요청하지 않음)
  const [states, setStates] = useState<Record<string, CatState>>({});

  // 클릭 시점에만 호출. 이미 받은 값이 있으면 재요청하지 않는다.
  const fetchCategory = async (key: Category) => {
    setStates((s) => ({ ...s, [key]: { status: "loading" } }));
    try {
      const res = await fetch("/api/interpret", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ saju, category: key }),
      });
      const data = await res.json();
      if (!res.ok || !data.text) {
        throw new Error(data.error || "해석을 불러오지 못했어요.");
      }
      setStates((s) => ({ ...s, [key]: { status: "done", text: data.text } }));
    } catch (e) {
      setStates((s) => ({
        ...s,
        [key]: { status: "error", error: e instanceof Error ? e.message : "오류" },
      }));
    }
  };

  const toggle = (key: Category) => {
    setOpen((cur) => (cur === key ? null : key));
    // 펼치는 동작이고, 아직 요청 전(idle/error)일 때만 호출
    const st = states[key]?.status;
    if (open !== key && (st === undefined || st === "error")) {
      fetchCategory(key);
    }
  };

  return (
    <div className="space-y-2">
      {categories.map((c) => {
        const isOpen = open === c.key;
        const st = states[c.key] ?? { status: "idle" as Status };
        return (
          <div key={c.key} className="overflow-hidden rounded-btn border border-border">
            <button
              type="button"
              onClick={() => toggle(c.key)}
              aria-expanded={isOpen}
              className="flex w-full items-center justify-between px-4 py-3 text-left hover:bg-surface"
            >
              <span>
                <span className="font-bold text-text">{c.key}운</span>
                <span className="ml-2 text-xs text-sub">{c.desc}</span>
              </span>
              <span
                className={`text-sub transition-transform ${isOpen ? "rotate-180" : ""}`}
              >
                <Icon name="chevron-down" size={20} />
              </span>
            </button>

            {isOpen && (
              <div className="border-t border-border px-4 py-3">
                {st.status === "loading" && (
                  <div className="flex items-center gap-2 py-2 text-sm text-sub">
                    <Spinner /> 해석을 생성하고 있어요…
                  </div>
                )}
                {st.status === "done" && (
                  <p className="whitespace-pre-line text-sm leading-relaxed text-text">
                    {st.text}
                  </p>
                )}
                {st.status === "error" && (
                  <div className="py-1 text-sm">
                    <p className="text-red-600">{st.error}</p>
                    <button
                      type="button"
                      onClick={() => fetchCategory(c.key)}
                      className="mt-2 text-primary underline"
                    >
                      다시 시도
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// 간단한 로딩 스피너
function Spinner() {
  return (
    <svg className="h-4 w-4 animate-spin text-primary" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2.5" opacity="0.2" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
}
