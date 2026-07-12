"use client";

// 대운/세운 시각화 — recharts 라인 차트 ("인생 곡선" 컨셉).
// Y축은 오행 균형 점수(단순화)이며, ssaju 실데이터 연동 시 산출 로직으로 교체 예정.
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
  ReferenceLine,
} from "recharts";
import { useState } from "react";
import type { Daeun, Seun } from "@/lib/types";

type Mode = "daeun" | "seun";

export default function DaeunSeunChart({
  daeun,
  seun,
  currentYear = new Date().getFullYear(),
}: {
  daeun: Daeun[];
  seun: Seun[];
  currentYear?: number;
}) {
  const [mode, setMode] = useState<Mode>("daeun");

  // 차트 데이터 정규화 (x축 라벨 통일)
  const data =
    mode === "daeun"
      ? daeun.map((d) => ({
          x: `${d.age}세`,
          score: d.score,
          gan: `${d.cheongan}${d.jiji}`,
        }))
      : seun.map((s) => ({
          x: `${s.year}`,
          score: s.score,
          gan: `${s.cheongan}${s.jiji}`,
          isNow: s.year === currentYear,
        }));

  const nowLabel =
    mode === "seun" ? String(currentYear) : undefined;

  return (
    <div>
      {/* 대운/세운 전환 토글 */}
      <div className="mb-4 inline-flex gap-1 rounded-btn border border-border bg-surface p-1">
        {(["daeun", "seun"] as Mode[]).map((m) => (
          <button
            key={m}
            type="button"
            onClick={() => setMode(m)}
            className={`rounded-[7px] px-4 py-1.5 text-sm font-bold transition-colors ${
              mode === m ? "bg-primary text-white" : "text-sub hover:text-text"
            }`}
          >
            {m === "daeun" ? "대운 (10년)" : "세운 (연도)"}
          </button>
        ))}
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
            <XAxis
              dataKey="x"
              tick={{ fontSize: 11, fill: "#6B7280" }}
              tickLine={false}
              axisLine={{ stroke: "#E5E7EB" }}
            />
            <YAxis
              domain={[0, 100]}
              tick={{ fontSize: 11, fill: "#6B7280" }}
              tickLine={false}
              axisLine={false}
              width={34}
            />
            {nowLabel && (
              <ReferenceLine
                x={nowLabel}
                stroke="#3B82F6"
                strokeDasharray="4 4"
                label={{ value: "올해", fontSize: 11, fill: "#3B82F6", position: "top" }}
              />
            )}
            <Tooltip content={<ChartTooltip />} />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#3B82F6"
              strokeWidth={2.5}
              dot={{ r: 3, fill: "#3B82F6" }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-2 text-center text-xs text-sub">
        Y축은 시기별 오행 균형 점수(높을수록 안정)이며, 참고용 지표예요.
      </p>
    </div>
  );
}

// 커스텀 툴팁 — 간지와 점수 표시
function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  const p = payload[0].payload;
  return (
    <div className="rounded-btn border border-border bg-background px-3 py-2 text-xs shadow-sm">
      <div className="font-bold text-text">
        {label} · {p.gan}
      </div>
      <div className="text-sub">균형 점수 {p.score}</div>
    </div>
  );
}
