// /dictionary/[term] — 용어별 상세 페이지 (SEO용, 각 용어당 1페이지).
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Icon from "@/components/ui/Icon";
import { dictTerms, getTerm } from "@/lib/data/dictionary";

// 정적 생성: 모든 용어 페이지를 빌드 타임에 생성 (색인 최적화)
export function generateStaticParams() {
  return dictTerms.map((t) => ({ term: t.slug }));
}

// 페이지별 동적 메타 태그
export function generateMetadata({
  params,
}: {
  params: { term: string };
}): Metadata {
  const t = getTerm(params.term);
  if (!t) return { title: "용어를 찾을 수 없습니다" };
  return {
    title: `${t.term} — 사주 용어 사전`,
    description: `${t.term}: ${t.short} ${t.body.slice(0, 60)}`,
  };
}

export default function TermPage({ params }: { params: { term: string } }) {
  const t = getTerm(params.term);
  if (!t) notFound();

  // 같은 그룹 관련 용어 추천
  const related = dictTerms
    .filter((x) => x.group === t.group && x.slug !== t.slug)
    .slice(0, 4);

  return (
    <article className="space-y-6">
      <nav className="text-sm text-sub">
        <Link href="/dictionary" className="hover:text-primary">
          용어 사전
        </Link>{" "}
        / <span>{t.group}</span>
      </nav>

      <header>
        <span className="rounded-full bg-surface px-2.5 py-1 text-xs text-sub">
          {t.group}
        </span>
        <h1 className="mt-2 text-2xl font-bold">{t.term}</h1>
        <p className="mt-1 text-sub">{t.short}</p>
      </header>

      <div className="card">
        <p className="leading-relaxed text-text">{t.body}</p>
      </div>

      {related.length > 0 && (
        <section>
          <h2 className="mb-2 text-sm font-bold text-sub">관련 용어</h2>
          <div className="flex flex-wrap gap-2">
            {related.map((r) => (
              <Link
                key={r.slug}
                href={`/dictionary/${r.slug}`}
                className="flex items-center gap-1 rounded-full border border-border px-3 py-1.5 text-sm text-text hover:border-primary"
              >
                {r.term}
                <Icon name="arrow-right" size={14} />
              </Link>
            ))}
          </div>
        </section>
      )}
    </article>
  );
}
