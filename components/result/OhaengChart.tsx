// 오행 분포 시각화 — 목/화/토/금/수 비율을 가로 막대로 표현.
import type { OhaengDistribution } from "@/lib/types";

const meta: { key: keyof OhaengDistribution; label: string; color: string }[] = [
  { key: "목", label: "목 (木)", color: "#22C55E" },
  { key: "화", label: "화 (火)", color: "#EF4444" },
  { key: "토", label: "토 (土)", color: "#F59E0B" },
  { key: "금", label: "금 (金)", color: "#9CA3AF" },
  { key: "수", label: "수 (水)", color: "#3B82F6" },
];

export default function OhaengChart({ data }: { data: OhaengDistribution }) {
  const max = Math.max(...meta.map((m) => data[m.key]), 1);

  return (
    <div className="space-y-2.5">
      {meta.map((m) => {
        const val = data[m.key];
        return (
          <div key={m.key} className="flex items-center gap-3">
            <span className="w-14 shrink-0 text-sm font-bold text-text">
              {m.label}
            </span>
            <div className="h-3 flex-1 overflow-hidden rounded-full bg-surface">
              <div
                className="h-full rounded-full transition-all"
                style={{
                  width: `${(val / max) * 100}%`,
                  backgroundColor: m.color,
                }}
              />
            </div>
            <span className="w-9 shrink-0 text-right text-sm tabular-nums text-sub">
              {val}%
            </span>
          </div>
        );
      })}
    </div>
  );
}
