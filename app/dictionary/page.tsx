// /dictionary — 사주 용어 사전 목록 + 검색/필터/정렬(클라이언트).
import type { Metadata } from "next";
import DictSearch from "@/components/dictionary/DictSearch";
import { dictTerms } from "@/lib/data/dictionary";

export const metadata: Metadata = {
  title: "사주 용어 사전 — 천간·지지·십성 풀이",
  description:
    "천간, 지지, 십성, 12운성, 신살 등 사주 용어를 쉽게 풀이한 사전. 키워드 검색과 분류 필터로 빠르게 찾아보세요.",
};

export default function DictionaryPage() {
  return (
    <div className="space-y-5">
      <section>
        <h1 className="text-xl font-bold">사주 용어 사전</h1>
        <p className="mt-1 text-sm text-sub">
          어려운 명리 용어를 한 줄로 쉽게. 궁금한 용어를 검색해보세요.
        </p>
      </section>
      <DictSearch terms={dictTerms} />
    </div>
  );
}
