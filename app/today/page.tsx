// /today — 오늘의 운세. 일간(띠) 12그룹 기준 짧은 콘텐츠, 매일 갱신 콘셉트.
import type { Metadata } from "next";
import Card from "@/components/ui/Card";
import { todayGroups, lineForToday } from "@/lib/data/today";

export const metadata: Metadata = {
  title: "오늘의 운세 — 띠별 하루 운세",
  description: "띠별로 보는 오늘의 짧은 운세. 매일 갱신되는 무료 콘텐츠.",
};

// 매일 갱신: 하루 단위 재검증
export const revalidate = 86400;

export default function TodayPage() {
  const today = new Date();
  const dateLabel = `${today.getFullYear()}년 ${today.getMonth() + 1}월 ${today.getDate()}일`;

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-xl font-bold">오늘의 운세</h1>
        <p className="mt-1 text-sm text-sub">{dateLabel} · 띠별 하루 흐름</p>
      </section>

      <div className="grid gap-3 sm:grid-cols-2">
        {todayGroups.map((g) => (
          <Card key={g.slug} className="flex gap-3">
            <span className="text-2xl" aria-hidden>
              {g.emoji}
            </span>
            <div>
              <h2 className="font-bold">{g.name}</h2>
              <p className="mt-1 text-sm leading-relaxed text-text">
                {lineForToday(g, today)}
              </p>
            </div>
          </Card>
        ))}
      </div>

      <p className="text-center text-xs text-sub">
        정확한 개인 운세는 홈에서 생년월일시로 명식을 계산해 확인하세요.
      </p>
    </div>
  );
}
