// 홈 (/) — 생년월일시 입력 폼을 첫 화면에 노출. 하단에 오늘의운세/신년운세 링크.
import Link from "next/link";
import BirthInputForm from "@/components/home/BirthInputForm";
import Card from "@/components/ui/Card";
import Icon from "@/components/ui/Icon";

export const metadata = {
  title: "무료 사주풀이 — 생년월일시로 보는 정확한 명식",
  description:
    "생년월일시를 입력하면 사주 명식을 정확히 계산하고 오행·대운·세운과 개인화된 해석을 무료로 확인하세요.",
};

export default function HomePage() {
  return (
    <div className="space-y-6">
      {/* 히어로 + 입력 폼 (첫 화면 노출) */}
      <section className="text-center">
        <h1 className="text-2xl font-bold sm:text-3xl">
          정확한 명식, 신뢰할 수 있는 해석
        </h1>
        <p className="mx-auto mt-2 max-w-md text-sub">
          생년월일시만 입력하면 사주 명식을 계산하고 개인화된 해석을
          보여드려요. 가입 없이 무료.
        </p>
      </section>

      <Card>
        <BirthInputForm />
      </Card>

      {/* 하단 바로가기 */}
      <section className="grid grid-cols-2 gap-3">
        <QuickLink href="/today" icon="sun" title="오늘의 운세" desc="일간별 매일 갱신" />
        <QuickLink
          href="/dictionary"
          icon="book"
          title="사주 용어 사전"
          desc="천간·지지·십성 풀이"
        />
      </section>
    </div>
  );
}

function QuickLink({
  href,
  icon,
  title,
  desc,
}: {
  href: string;
  icon: "sun" | "book";
  title: string;
  desc: string;
}) {
  return (
    <Link
      href={href}
      className="card flex items-center gap-3 transition-colors hover:border-primary"
    >
      <span className="text-primary">
        <Icon name={icon} />
      </span>
      <span>
        <span className="block font-bold">{title}</span>
        <span className="block text-xs text-sub">{desc}</span>
      </span>
    </Link>
  );
}
