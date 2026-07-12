// 전역 푸터 — 법적/안내 페이지 링크 + 면책 문구.
import Link from "next/link";

const links = [
  { href: "/about", label: "소개" },
  { href: "/guide", label: "이용안내" },
  { href: "/privacy", label: "개인정보처리방침" },
  { href: "/contact", label: "문의하기" },
];

export default function Footer() {
  return (
    <footer className="mt-12 border-t border-border bg-surface">
      <div className="mx-auto max-w-content px-4 py-8">
        <nav className="flex flex-wrap gap-x-5 gap-y-2">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="text-sm text-sub hover:text-primary"
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <p className="mt-4 text-xs leading-relaxed text-sub">
          본 사이트의 사주 결과는 통계·전통 명리학에 기반한 <b>참고용 정보</b>이며,
          의료·법률·재무 등 전문적 판단을 대체하지 않습니다.
        </p>
        <p className="mt-2 text-xs text-sub">
          © {new Date().getFullYear()} 사주풀이. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
