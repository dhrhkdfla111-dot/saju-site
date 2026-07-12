// 법적/안내 페이지 공통 레이아웃 — 제목 + 본문 섹션.
import type { ReactNode } from "react";

export function LegalSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section>
      <h2 className="mb-2 text-base font-bold text-text">{title}</h2>
      <div className="space-y-2 text-sm leading-relaxed text-sub">{children}</div>
    </section>
  );
}

export default function LegalPage({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-xl font-bold">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-sub">{subtitle}</p>}
      </header>
      <div className="space-y-6">{children}</div>
    </div>
  );
}
