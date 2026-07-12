import type { Config } from "tailwindcss";

/**
 * 디자인 시스템 토큰(정확한 값 준수)을 Tailwind에 매핑.
 * 실제 값은 CSS 변수(globals.css)로 정의하고 여기서 참조한다.
 */
const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--color-primary)",
        text: "var(--color-text)",
        sub: "var(--color-sub)",
        background: "var(--color-background)",
        surface: "var(--color-surface)",
        border: "var(--color-border)",
      },
      borderRadius: {
        btn: "var(--radius-btn)", // 버튼 10px
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      fontWeight: {
        heading: "700",
      },
      maxWidth: {
        content: "720px", // 모바일 퍼스트 본문 폭
      },
    },
  },
  plugins: [],
};

export default config;
