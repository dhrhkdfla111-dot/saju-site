// 공통 카드 컨테이너 — Surface/Border 토큰 기반.
import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  desc?: string;
}

export default function Card({ children, className = "", title, desc }: CardProps) {
  return (
    <section className={`card ${className}`.trim()}>
      {title && (
        <header className="mb-3">
          <h2 className="text-lg font-bold">{title}</h2>
          {desc && <p className="mt-1 text-sm text-sub">{desc}</p>}
        </header>
      )}
      {children}
    </section>
  );
}
