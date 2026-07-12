"use client";

// /contact — 문의하기. 백엔드 연동 전이므로 mailto 기반 폼으로 동작.
import { useState } from "react";
import Card from "@/components/ui/Card";
import Icon from "@/components/ui/Icon";

export default function ContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const subject = encodeURIComponent(`[사주풀이 문의] ${name || "이름 없음"}`);
    const body = encodeURIComponent(`${message}\n\n— ${name} (${email})`);
    // 백엔드 폼 처리 전: 메일 클라이언트로 연결
    window.location.href = `mailto:hello@saju.example.com?subject=${subject}&body=${body}`;
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-xl font-bold">문의하기</h1>
        <p className="mt-1 text-sm text-sub">
          서비스 개선 의견이나 오류 제보를 환영합니다.
        </p>
      </header>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="이름" value={name} onChange={setName} placeholder="홍길동" />
          <Input
            label="이메일"
            type="email"
            value={email}
            onChange={setEmail}
            placeholder="you@example.com"
          />
          <div>
            <label className="mb-1.5 block text-sm font-bold">문의 내용</label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={5}
              required
              placeholder="문의하실 내용을 적어주세요."
              className="w-full rounded-btn border border-border bg-background px-3 py-2.5 text-text outline-none focus:border-primary"
            />
          </div>
          <button type="submit" className="btn-primary w-full">
            <Icon name="arrow-right" size={18} /> 메일로 보내기
          </button>
        </form>
      </Card>
      <p className="text-center text-xs text-sub">
        폼 전송은 메일 클라이언트로 연결됩니다. (서버 접수는 백엔드 연동 시 추가)
      </p>
    </div>
  );
}

function Input({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  type?: string;
}) {
  return (
    <div>
      <label className="mb-1.5 block text-sm font-bold">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-btn border border-border bg-background px-3 py-2.5 text-text outline-none focus:border-primary"
      />
    </div>
  );
}
