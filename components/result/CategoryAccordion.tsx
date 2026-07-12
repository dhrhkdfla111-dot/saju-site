"use client";

// 분야별 심화 해석 — 버튼 5개(이직/사랑/금전/건강/지인), 클릭 시 아코디언 펼침.
// 백엔드 연동 전이므로 "백그라운드 준비 → 즉시 표시 / 미완료 시 스피너" 흐름을 시뮬레이션.
// PART 2에서 실제 /api/interpret 병렬 프리페치로 교체.
import { useEffect, useRef, useState } from "react";
import Icon from "@/components/ui/Icon";
import { dummyCategoryText } from "@/lib/dummy/saju";
import type { Category } from "@/lib/types";

const categories: { key: Category; desc: string }[] = [
  { key: "이직", desc: "시기 판단 중심" },
  { key: "사랑", desc: "성향·궁합 포인트" },
  { key: "금전", desc: "리스크 관리 관점" },
  { key: "건강", desc: "체력 관리 안내" },
  { key: "지인", desc: "인간관계 흐름" },
];

export default function CategoryAccordion() {
  const [open, setOpen] = useState<Category | null>(null);
  // 각 카테고리 해석의 준비 상태 (백그라운드 프리페치 시뮬레이션)
  const [ready, setReady] = useState<Record<string, boolean>>({});
  const started = useRef(false);

  // 결과 페이지 진입 시 5개 해석을 백그라운드에서 순차 준비(병렬 프리페치 흉내)
  useEffect(() => {
    if (started.current) return;
    started.current = true;
    categories.forEach((c, i) => {
      // 실제로는 fetch('/api/interpret'). 여기선 지연으로 준비 완료를 흉내낸다.
      const t = setTimeout(
        () => setReady((r) => ({ ...r, [c.key]: true })),
        700 + i * 500
      );
      return () => clearTimeout(t);
    });
  }, []);

  const toggle = (key: Category) => setOpen((cur) => (cur === key ? null : key));

  return (
    <div className="space-y-2">
      {categories.map((c) => {
        const isOpen = open === c.key;
        const isReady = ready[c.key];
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
                {isReady ? (
                  <p
                    className="text-sm leading-relaxed text-text"
                    // 건강 카테고리 등 일부 <b> 강조 포함
                    dangerouslySetInnerHTML={{ __html: dummyCategoryText[c.key] }}
                  />
                ) : (
                  <div className="flex items-center gap-2 py-2 text-sm text-sub">
                    <Spinner /> 해석을 준비하고 있어요…
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

// 간단한 로딩 스피너 (라인 아이콘 톤)
function Spinner() {
  return (
    <svg
      className="h-4 w-4 animate-spin text-primary"
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2.5" opacity="0.2" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
}
