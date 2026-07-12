import type { Metadata } from "next";
import LegalPage, { LegalSection } from "@/components/layout/LegalPage";

export const metadata: Metadata = {
  title: "소개",
  description: "데이터 기반의 정갈한 사주풀이 서비스 소개.",
};

export default function AboutPage() {
  return (
    <LegalPage title="소개" subtitle="정갈하고 신뢰감 있는 사주풀이를 지향합니다.">
      <LegalSection title="우리가 만드는 것">
        <p>
          생년월일시를 입력하면 정확한 사주 명식을 계산하고, 이해하기 쉬운 언어로
          풀어 드리는 무료 서비스입니다. 화려한 미신이 아니라, 전통 명리학의
          체계를 데이터로 정리해 보여드리는 데 집중합니다.
        </p>
      </LegalSection>
      <LegalSection title="원칙">
        <p>· 불안을 조장하지 않고, 대비 가능한 정보로 전달합니다.</p>
        <p>· 어려운 전문용어는 짧은 설명을 함께 제공합니다.</p>
        <p>· 결과는 참고용이며, 선택은 언제나 사용자 본인의 몫입니다.</p>
      </LegalSection>
    </LegalPage>
  );
}
