// /result — 사주 결과 페이지.
// 현재는 더미 데이터 기반(백엔드 연동 전). 쿼리로 받은 입력값은 헤더 표시에 사용.
import type { Metadata } from "next";
import PillarTable from "@/components/result/PillarTable";
import OhaengChart from "@/components/result/OhaengChart";
import DaeunSeunChart from "@/components/result/DaeunSeunChart";
import CategoryAccordion from "@/components/result/CategoryAccordion";
import ShareCard from "@/components/result/ShareCard";
import Card from "@/components/ui/Card";
import AdSlot from "@/components/layout/AdSlot";
import { dummySaju, dummyInterpretation } from "@/lib/dummy/saju";

type SearchParams = { [k: string]: string | undefined };

// 동적 메타 + OG 이미지 연결 (공유 카드용)
export function generateMetadata({
  searchParams,
}: {
  searchParams: SearchParams;
}): Metadata {
  const { year, month, day } = searchParams;
  const dateLabel =
    year && month && day ? `${year}.${month}.${day}` : "";
  // 명식 8글자(더미) → OG route 파라미터
  const p = dummySaju.pillars
    .flatMap((pi) => [pi.cheongan, pi.jiji])
    .join(",");
  const ogUrl = `/api/og?p=${encodeURIComponent(p)}${
    dateLabel ? `&d=${encodeURIComponent(dateLabel)}` : ""
  }`;
  return {
    title: "사주 결과 — 명식·오행·해석",
    description: "원국 명식과 오행 분포, 개인화된 사주 해석 결과를 확인하세요.",
    openGraph: {
      title: "내 사주 결과",
      description: "정화(丁火) 일간 · 명식과 오행, 대운·세운 해석",
      images: [{ url: ogUrl, width: 1200, height: 630 }],
    },
    twitter: { card: "summary_large_image", images: [ogUrl] },
  };
}

export default function ResultPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  // 입력 요약 (쿼리 우선, 없으면 더미)
  const s = dummySaju;
  const year = searchParams.year ?? String(s.input.year);
  const month = searchParams.month ?? String(s.input.month);
  const day = searchParams.day ?? String(s.input.day);
  const gender = searchParams.gender ?? s.input.gender;
  const calendar = searchParams.calendar === "lunar" ? "음력" : "양력";
  const hourUnknown = searchParams.hour === undefined;
  const time =
    searchParams.hour !== undefined
      ? `${searchParams.hour}시${searchParams.minute ? ` ${searchParams.minute}분` : ""}`
      : "시각 미상";

  // /api/interpret로 넘길 사주 컴팩트(원국+오행+성별). 클릭 시 카테고리 생성에 사용.
  const sajuCompact = {
    pillars: s.pillars.map((p) => ({
      label: p.label,
      cheongan: p.cheongan,
      jiji: p.jiji,
      sipseong: p.sipseong,
    })),
    ilgan: s.pillars.find((p) => p.label === "일주")?.cheongan,
    ohaeng: Object.fromEntries(Object.entries(s.ohaeng)) as Record<string, number>,
    gender,
    hourUnknown,
  };

  return (
    <div className="space-y-6">
      {/* 입력 요약 헤더 */}
      <section>
        <h1 className="text-xl font-bold">사주 결과</h1>
        <p className="mt-1 text-sm text-sub">
          {calendar} {year}년 {month}월 {day}일 · {time} · {gender}
        </p>
      </section>

      {/* 1) 총평 (성격/기질) — 최상단 */}
      <Card title="총평" desc="성격과 기질">
        <p className="text-[15px] leading-relaxed text-text">
          {dummyInterpretation.summary}
        </p>
      </Card>

      {/* 2) 오늘의 총운/재물운/애정운 요약 */}
      <Card title="오늘의 운세 요약">
        <dl className="space-y-3">
          {Object.entries(dummyInterpretation.today).map(([k, v]) => (
            <div key={k}>
              <dt className="text-sm font-bold text-primary">{k}</dt>
              <dd className="mt-0.5 text-sm leading-relaxed text-text">{v}</dd>
            </div>
          ))}
        </dl>
      </Card>

      {/* 3) 원국 명식표 */}
      <Card title="원국 명식" desc="연·월·일·시 사주 여덟 글자">
        <PillarTable pillars={s.pillars} hourUnknown={hourUnknown} />
      </Card>

      {/* 4) 오행 분포 */}
      <Card title="오행 분포" desc="목·화·토·금·수 균형">
        <OhaengChart data={s.ohaeng} />
      </Card>

      {/* 5) 십성 & 공망 */}
      <div className="grid gap-6 sm:grid-cols-2">
        <Card title="십성">
          <div className="flex flex-wrap gap-2">
            {s.sipseong.map((t) => (
              <span
                key={t}
                className="rounded-full bg-surface px-3 py-1 text-sm text-text"
              >
                {t}
              </span>
            ))}
          </div>
        </Card>
        <Card title="공망" desc="비어 있는 기운">
          <div className="flex flex-wrap gap-2">
            {s.gongmang.map((t) => (
              <span
                key={t}
                className="rounded-full border border-border px-3 py-1 text-sm text-sub"
              >
                {t}
              </span>
            ))}
          </div>
        </Card>
      </div>

      {/* 6) 대운/세운 차트 ("인생 곡선") */}
      <Card title="대운·세운 흐름" desc="시기별 기운의 변화">
        <DaeunSeunChart daeun={s.daeun} seun={s.seun} />
      </Card>

      {/* 7) 분야별 심화 해석 (5종 아코디언) — 클릭 시 해당 카테고리만 생성 */}
      <Card title="분야별 심화 해석" desc="궁금한 분야를 눌러보세요">
        <CategoryAccordion saju={sajuCompact} />
      </Card>

      {/* 8) 공유 카드 */}
      <ShareCard
        pillars={s.pillars}
        summaryLine="정화(丁火) 일간 · 꾸준함이 강점인 사주"
      />

      {/* 광고 정책: 결과 페이지 하단 배너 1개 */}
      <AdSlot slot="result-bottom" />
    </div>
  );
}
