// 공통 버튼 — 디자인 토큰(radius 10px / padding 12px 20px / weight 700) 기반.
import Link from "next/link";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "outline" | "ghost";

const variantClass: Record<Variant, string> = {
  primary: "btn-primary",
  outline: "btn-outline",
  ghost: "btn-ghost",
};

interface BaseProps {
  variant?: Variant;
  className?: string;
  children: ReactNode;
}

/** href가 있으면 링크, 없으면 버튼으로 렌더 */
export default function Button({
  variant = "primary",
  className = "",
  children,
  href,
  ...rest
}: BaseProps &
  ButtonHTMLAttributes<HTMLButtonElement> & { href?: string }) {
  const cls = `${variantClass[variant]} ${className}`.trim();
  if (href) {
    return (
      <Link href={href} className={cls}>
        {children}
      </Link>
    );
  }
  return (
    <button className={cls} {...rest}>
      {children}
    </button>
  );
}
