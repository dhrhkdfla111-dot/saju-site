import type { Metadata } from "next";
import LegalPage, { LegalSection } from "@/components/layout/LegalPage";

export const metadata: Metadata = {
  title: "이용안내 · 이용약관",
  description: "서비스 이용 방법과 이용약관, 사주 결과의 참고용 면책 안내.",
};

export default function GuidePage() {
  return (
    <LegalPage title="이용안내 · 이용약관" subtitle="서비스 이용 전 확인해주세요.">
      <LegalSection title="이용 방법">
        <p>
          1. 홈에서 생년월일시와 성별, 양력/음력을 입력합니다. 출생 시각을 모르면
          비워두어도 되며, 이 경우 연·월·일주만 계산됩니다.
        </p>
        <p>2. 명식과 오행, 대운·세운, 분야별 심화 해석을 확인합니다.</p>
        <p>3. 결과 카드를 저장하거나 공유할 수 있습니다.</p>
      </LegalSection>

      <LegalSection title="면책 조항 (중요)">
        <p>
          본 사이트가 제공하는 사주 명식과 해석은 <b className="text-text">전통 명리학과
          통계에 기반한 참고용 정보</b>입니다. 특정 결과를 보증하지 않으며, 의료·법률·
          재무·투자 등 전문적 판단이나 자격 있는 전문가의 상담을 대체하지 않습니다.
        </p>
        <p>
          사용자는 본 서비스의 정보를 바탕으로 내린 결정과 그 결과에 대해 스스로
          책임을 지며, 운영자는 이에 대해 법적 책임을 지지 않습니다.
        </p>
      </LegalSection>

      <LegalSection title="저작권">
        <p>
          사이트의 콘텐츠와 디자인에 대한 권리는 운영자에게 있으며, 무단 복제·배포를
          금합니다.
        </p>
      </LegalSection>
    </LegalPage>
  );
}
