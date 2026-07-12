// 원국 명식표 — 연/월/일/시 4주의 천간·지지 8글자 + 십성/12운성.
import type { Pillar } from "@/lib/types";

// 오행별 색상(천간·지지 글자 배경) — 데이터 기반 톤, 은은하게.
const ohaengColor: Record<string, string> = {
  목: "#DCFCE7", // green-100
  화: "#FEE2E2", // red-100
  토: "#FEF3C7", // amber-100
  금: "#F3F4F6", // gray-100
  수: "#DBEAFE", // blue-100
};

// 천간/지지 → 오행 매핑 (표시용 축약)
const ganOhaeng: Record<string, keyof typeof ohaengColor> = {
  갑: "목", 을: "목", 병: "화", 정: "화", 무: "토",
  기: "토", 경: "금", 신: "금", 임: "수", 계: "수",
};
const jiOhaeng: Record<string, keyof typeof ohaengColor> = {
  자: "수", 축: "토", 인: "목", 묘: "목", 진: "토", 사: "화",
  오: "화", 미: "토", 신: "금", 유: "금", 술: "토", 해: "수",
};

function GlyphCell({ char, ohaeng }: { char: string; ohaeng?: string }) {
  return (
    <div
      className="flex h-14 items-center justify-center rounded-btn text-2xl font-bold"
      style={{ backgroundColor: ohaeng ? ohaengColor[ohaeng] : "var(--color-surface)" }}
    >
      {char}
    </div>
  );
}

export default function PillarTable({
  pillars,
  hourUnknown,
}: {
  pillars: Pillar[];
  hourUnknown: boolean;
}) {
  // 시주 제외 시 시주 칼럼을 흐리게 표시
  return (
    <div>
      <div className="grid grid-cols-4 gap-2">
        {pillars.map((p) => {
          const dimmed = hourUnknown && p.label === "시주";
          return (
            <div key={p.label} className={dimmed ? "opacity-30" : ""}>
              <div className="mb-1.5 text-center text-xs font-bold text-sub">
                {p.label}
                {p.label === "일주" && (
                  <span className="ml-1 text-primary">(나)</span>
                )}
              </div>
              <div className="space-y-2">
                <GlyphCell char={p.cheongan} ohaeng={ganOhaeng[p.cheongan]} />
                <GlyphCell char={p.jiji} ohaeng={jiOhaeng[p.jiji]} />
              </div>
              <div className="mt-1.5 space-y-0.5 text-center">
                <div className="text-[11px] text-sub">{p.sipseong}</div>
                <div className="text-[11px] text-sub">{p.unseong}</div>
              </div>
            </div>
          );
        })}
      </div>
      {hourUnknown && (
        <p className="mt-3 rounded-btn bg-surface px-3 py-2 text-xs text-sub">
          출생 시각 미입력 — <b className="text-text">시주 제외</b>, 연·월·일주만
          계산되었습니다.
        </p>
      )}
    </div>
  );
}
