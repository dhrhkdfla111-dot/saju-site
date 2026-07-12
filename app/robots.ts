import type { MetadataRoute } from "next";

const BASE = "https://saju.example.com";

// robots.txt 자동 생성. /result는 개인 입력 기반이라 색인 제외.
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/result", "/api/"],
    },
    sitemap: `${BASE}/sitemap.xml`,
  };
}
