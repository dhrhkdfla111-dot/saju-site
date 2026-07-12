import type { MetadataRoute } from "next";
import { dictTerms } from "@/lib/data/dictionary";

const BASE = "https://saju.example.com";

// sitemap.xml 자동 생성 — 정적 페이지 + 용어 사전 개별 페이지(SEO 우선).
export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  const staticPages: MetadataRoute.Sitemap = [
    { url: `${BASE}/`, priority: 1, changeFrequency: "daily", lastModified: now },
    { url: `${BASE}/today`, priority: 0.8, changeFrequency: "daily", lastModified: now },
    { url: `${BASE}/dictionary`, priority: 0.7, changeFrequency: "weekly", lastModified: now },
    { url: `${BASE}/about`, priority: 0.3, changeFrequency: "monthly", lastModified: now },
    { url: `${BASE}/guide`, priority: 0.3, changeFrequency: "monthly", lastModified: now },
    { url: `${BASE}/privacy`, priority: 0.2, changeFrequency: "yearly", lastModified: now },
    { url: `${BASE}/contact`, priority: 0.3, changeFrequency: "monthly", lastModified: now },
  ];

  const termPages: MetadataRoute.Sitemap = dictTerms.map((t) => ({
    url: `${BASE}/dictionary/${t.slug}`,
    lastModified: now,
    changeFrequency: "monthly",
    priority: 0.6,
  }));

  return [...staticPages, ...termPages];
}
