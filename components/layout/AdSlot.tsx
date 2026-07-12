// 광고 슬롯 자리표시자.
// 정책: 상단 배너 1개 + 결과 페이지 하단 배너 1개, 본문 해석 텍스트 사이 삽입 금지.
// 애드센스 심사 통과 후 실제 코드 삽입 예정 — 지금은 위치만 잡아둔다.

interface AdSlotProps {
  slot: "top" | "result-bottom";
  className?: string;
}

const labels: Record<AdSlotProps["slot"], string> = {
  top: "상단 배너 광고 영역",
  "result-bottom": "결과 하단 배너 광고 영역",
};

export default function AdSlot({ slot, className = "" }: AdSlotProps) {
  return (
    <div
      data-ad-slot={slot}
      className={`flex min-h-[90px] items-center justify-center rounded-btn border border-dashed border-border bg-surface text-xs text-sub ${className}`.trim()}
      aria-label={labels[slot]}
    >
      {labels[slot]} (애드센스 심사 후 삽입)
    </div>
  );
}
