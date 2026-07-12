import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import AdSlot from "@/components/layout/AdSlot";

// SEO: 페이지별로 확장할 기본 메타. 각 페이지에서 title/description을 덮어쓴다.
export const metadata: Metadata = {
  metadataBase: new URL("https://saju.example.com"),
  title: {
    default: "무료 사주풀이 — 정확한 명식 계산과 AI 해석",
    template: "%s | 사주풀이",
  },
  description:
    "생년월일시를 입력하면 정확한 사주 명식을 계산하고 개인화된 해석을 제공하는 무료 사주풀이 사이트. 오행 분포, 대운·세운, 분야별 심화 해석까지.",
  keywords: ["사주", "사주풀이", "무료사주", "만세력", "오늘의 운세", "명리학"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      {/* Inter 폰트: 외부 요청 없이 시스템 폴백 우선, 필요 시 next/font로 교체 가능 */}
      <body>
        <Header />
        {/* 광고 정책: 상단 배너 1개 */}
        <div className="mx-auto max-w-content px-4 pt-4">
          <AdSlot slot="top" />
        </div>
        <main className="mx-auto max-w-content px-4 py-6">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
