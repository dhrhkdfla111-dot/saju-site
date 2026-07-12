"use client";

// 전역 헤더 — 로고 + 주요 네비게이션. 모바일 퍼스트(햄버거 토글).
import Link from "next/link";
import { useState } from "react";
import Icon from "@/components/ui/Icon";

const nav = [
  { href: "/", label: "홈" },
  { href: "/today", label: "오늘의 운세" },
  { href: "/dictionary", label: "용어 사전" },
  { href: "/guide", label: "이용안내" },
];

export default function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur">
      <div className="mx-auto flex max-w-content items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-2 font-bold text-text">
          <Icon name="sparkles" size={22} className="text-primary" />
          <span className="text-lg">사주풀이</span>
        </Link>

        {/* 데스크탑 네비 */}
        <nav className="hidden gap-6 md:flex">
          {nav.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              className="text-sm font-medium text-sub hover:text-primary"
            >
              {n.label}
            </Link>
          ))}
        </nav>

        {/* 모바일 토글 */}
        <button
          className="btn-ghost !p-2 md:hidden"
          onClick={() => setOpen((v) => !v)}
          aria-label="메뉴 열기"
          aria-expanded={open}
        >
          <Icon name="menu" />
        </button>
      </div>

      {open && (
        <nav className="border-t border-border md:hidden">
          <div className="mx-auto flex max-w-content flex-col px-4 py-2">
            {nav.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                className="py-2 text-sm font-medium text-sub hover:text-primary"
                onClick={() => setOpen(false)}
              >
                {n.label}
              </Link>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
}
