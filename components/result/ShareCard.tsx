"use client";

// 공유 카드 — 결과 요약을 담은 시각 카드 + 공유 버튼.
// Web Share API 지원 시 네이티브 공유, 미지원 시 링크 복사.
// OG 이미지 자동 생성(route)은 Phase 5(SEO)에서 연결.
import { useState } from "react";
import Icon from "@/components/ui/Icon";
import type { Pillar } from "@/lib/types";

export default function ShareCard({
  pillars,
  summaryLine,
}: {
  pillars: Pillar[];
  summaryLine: string;
}) {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const url = typeof window !== "undefined" ? window.location.href : "";
    const shareData = {
      title: "내 사주 결과",
      text: summaryLine,
      url,
    };
    if (navigator.share) {
      try {
        await navigator.share(shareData);
        return;
      } catch {
        /* 사용자가 취소 — 무시 */
      }
    }
    // 폴백: 링크 복사
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      /* 클립보드 미지원 */
    }
  };

  return (
    <div className="overflow-hidden rounded-xl border border-border">
      {/* 카드 프리뷰 (OG 이미지와 동일한 구성) */}
      <div className="bg-gradient-to-br from-primary to-[#1e40af] p-5 text-white">
        <div className="flex items-center gap-1.5 text-sm opacity-90">
          <Icon name="sparkles" size={16} /> 사주풀이
        </div>
        <div className="mt-3 flex justify-center gap-2">
          {pillars.map((p) => (
            <div key={p.label} className="text-center">
              <div className="flex flex-col overflow-hidden rounded-md bg-white/15">
                <span className="px-3 py-1.5 text-xl font-bold">{p.cheongan}</span>
                <span className="px-3 py-1.5 text-xl font-bold">{p.jiji}</span>
              </div>
              <div className="mt-1 text-[10px] opacity-80">{p.label}</div>
            </div>
          ))}
        </div>
        <p className="mt-3 text-center text-sm opacity-95">{summaryLine}</p>
      </div>

      {/* 공유 버튼 */}
      <div className="flex items-center justify-between px-4 py-3">
        <span className="text-sm text-sub">
          {copied ? "링크가 복사됐어요!" : "결과를 친구에게 공유해보세요"}
        </span>
        <button type="button" onClick={handleShare} className="btn-outline !py-2 !px-4">
          <Icon name="share" size={18} /> 공유
        </button>
      </div>
    </div>
  );
}
