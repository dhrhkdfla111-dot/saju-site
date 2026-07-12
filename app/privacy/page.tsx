import type { Metadata } from "next";
import LegalPage, { LegalSection } from "@/components/layout/LegalPage";

export const metadata: Metadata = {
  title: "개인정보처리방침",
  description: "수집하는 정보와 이용 목적, 보관 및 광고(쿠키) 관련 안내.",
};

export default function PrivacyPage() {
  return (
    <LegalPage title="개인정보처리방침" subtitle="시행일: 2026-01-01">
      <LegalSection title="1. 수집하는 정보">
        <p>
          사주 계산을 위해 입력하는 생년월일시·성별·양력/음력 정보는 결과 계산
          목적으로만 사용되며, 별도 회원가입 없이 이용할 수 있습니다. 문의 시
          제공한 이메일 주소는 답변 목적에 한해 사용합니다.
        </p>
      </LegalSection>
      <LegalSection title="2. 이용 및 보관">
        <p>
          입력 정보는 해석 결과 생성 및 성능 향상을 위한 캐시 목적으로 처리될 수
          있으며, 개인을 식별하는 형태로 장기 저장하지 않습니다.
        </p>
      </LegalSection>
      <LegalSection title="3. 쿠키 및 광고">
        <p>
          본 사이트는 서비스 운영을 위해 쿠키를 사용할 수 있으며, 제휴 광고
          (예: Google AdSense)가 게재되는 경우 광고 사업자가 쿠키를 통해 관심
          기반 광고를 제공할 수 있습니다. 사용자는 브라우저 설정에서 쿠키를
          거부할 수 있습니다.
        </p>
      </LegalSection>
      <LegalSection title="4. 문의">
        <p>개인정보 관련 문의는 문의하기 페이지를 통해 접수해주세요.</p>
      </LegalSection>
    </LegalPage>
  );
}
