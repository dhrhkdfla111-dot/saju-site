// OG 이미지 자동 생성 route — 공유용 사주 요약 카드(1200x630).
// 한자(간지)는 시스템 CJK 폰트를 임베드해 렌더하고, 안내문은 Latin으로 안전 표기.
import { ImageResponse } from "next/og";
import { readFileSync } from "node:fs";
import { toGan, toJi } from "@/lib/hanja";

export const runtime = "nodejs";

// 한자를 커버하는 CJK 폰트 로드 (빌드/서버 환경에 존재).
function loadCjkFont(): ArrayBuffer | null {
  const candidates = [
    "/etc/alternatives/fonts-japanese-gothic.ttf",
  ];
  for (const p of candidates) {
    try {
      const buf = readFileSync(p);
      return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
    } catch {
      /* 다음 후보 */
    }
  }
  return null;
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  // p = 연간,연지,월간,월지,일간,일지,시간,시지 (한글). 없으면 예시 명식.
  const raw = searchParams.get("p") ?? "을,해,기,묘,정,축,정,미";
  const chars = raw.split(",");
  const date = searchParams.get("d") ?? "";

  // 4주(연/월/일/시) 한자 변환
  const labels = ["연주", "월주", "일주", "시주"];
  const pillars = [0, 1, 2, 3].map((i) => ({
    label: labels[i],
    gan: toGan(chars[i * 2] ?? ""),
    ji: toJi(chars[i * 2 + 1] ?? ""),
  }));

  const font = loadCjkFont();

  return new ImageResponse(
    (
      <div
        style={{
          width: "1200px",
          height: "630px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          background: "linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%)",
          color: "white",
          fontFamily: "CJK, sans-serif",
        }}
      >
        <div style={{ fontSize: 34, opacity: 0.9, letterSpacing: 4 }}>SAJU</div>
        {date && (
          <div style={{ fontSize: 26, opacity: 0.8, marginTop: 8 }}>{date}</div>
        )}
        <div style={{ display: "flex", gap: 24, marginTop: 40 }}>
          {pillars.map((p) => (
            <div
              key={p.label}
              style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
            >
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  background: "rgba(255,255,255,0.15)",
                  borderRadius: 16,
                  padding: "16px 28px",
                }}
              >
                <span style={{ fontSize: 72, fontWeight: 700, lineHeight: 1.1 }}>
                  {p.gan}
                </span>
                <span style={{ fontSize: 72, fontWeight: 700, lineHeight: 1.1 }}>
                  {p.ji}
                </span>
              </div>
            </div>
          ))}
        </div>
        <div style={{ fontSize: 28, opacity: 0.85, marginTop: 44 }}>
          Free Saju Reading
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
      fonts: font
        ? [{ name: "CJK", data: font, style: "normal", weight: 700 }]
        : undefined,
    }
  );
}
