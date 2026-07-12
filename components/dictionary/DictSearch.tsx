"use client";

// 용어 사전 검색/필터/정렬 (클라이언트). 소규모 데이터라 클라이언트에서 처리.
import Link from "next/link";
import { useMemo, useState } from "react";
import Icon from "@/components/ui/Icon";
import { dictGroups } from "@/lib/data/dictionary";
import type { DictTerm } from "@/lib/types";

type Sort = "가나다" | "그룹순";

export default function DictSearch({ terms }: { terms: DictTerm[] }) {
  const [q, setQ] = useState("");
  const [group, setGroup] = useState<(typeof dictGroups)[number]>("전체");
  const [sort, setSort] = useState<Sort>("가나다");

  const filtered = useMemo(() => {
    const kw = q.trim().toLowerCase();
    let list = terms.filter((t) => {
      const inGroup = group === "전체" || t.group === group;
      const inKw =
        !kw ||
        t.term.toLowerCase().includes(kw) ||
        t.short.toLowerCase().includes(kw) ||
        t.body.toLowerCase().includes(kw);
      return inGroup && inKw;
    });
    list = [...list].sort((a, b) =>
      sort === "가나다"
        ? a.term.localeCompare(b.term, "ko")
        : a.group.localeCompare(b.group, "ko") || a.term.localeCompare(b.term, "ko")
    );
    return list;
  }, [terms, q, group, sort]);

  return (
    <div className="space-y-4">
      {/* 검색창 */}
      <div className="flex items-center gap-2 rounded-btn border border-border bg-background px-3 focus-within:border-primary">
        <span className="text-sub">
          <Icon name="search" size={20} />
        </span>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="용어를 검색하세요 (예: 편재, 대운)"
          className="w-full bg-transparent py-2.5 text-text outline-none"
        />
      </div>

      {/* 필터(그룹) + 정렬 */}
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex flex-wrap gap-1.5">
          {dictGroups.map((g) => (
            <button
              key={g}
              type="button"
              onClick={() => setGroup(g)}
              className={`rounded-full border px-3 py-1 text-sm transition-colors ${
                group === g
                  ? "border-primary bg-primary text-white"
                  : "border-border text-sub hover:text-text"
              }`}
            >
              {g}
            </button>
          ))}
        </div>
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value as Sort)}
          className="ml-auto rounded-btn border border-border bg-background px-3 py-1.5 text-sm text-text outline-none focus:border-primary"
          aria-label="정렬"
        >
          <option value="가나다">가나다순</option>
          <option value="그룹순">그룹순</option>
        </select>
      </div>

      {/* 결과 개수 */}
      <p className="text-xs text-sub">{filtered.length}개 용어</p>

      {/* 결과 목록 */}
      {filtered.length === 0 ? (
        <p className="py-8 text-center text-sm text-sub">
          검색 결과가 없어요. 다른 키워드로 찾아보세요.
        </p>
      ) : (
        <ul className="space-y-2">
          {filtered.map((t) => (
            <li key={t.slug}>
              <Link
                href={`/dictionary/${t.slug}`}
                className="card flex items-center justify-between transition-colors hover:border-primary"
              >
                <span>
                  <span className="flex items-center gap-2">
                    <span className="font-bold text-text">{t.term}</span>
                    <span className="rounded-full bg-surface px-2 py-0.5 text-[11px] text-sub">
                      {t.group}
                    </span>
                  </span>
                  <span className="mt-0.5 block text-sm text-sub">{t.short}</span>
                </span>
                <span className="shrink-0 text-sub">
                  <Icon name="arrow-right" size={18} />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
