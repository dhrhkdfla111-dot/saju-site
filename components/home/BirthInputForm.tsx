"use client";

// 홈 생년월일시 입력 폼.
// - 연/월/일 필수, 시/분 선택(모름 시 시주 제외 안내)
// - 성별, 양/음력, 윤달(음력 선택 시) 토글
// - 제출 시 /result 로 쿼리 전달 (백엔드 연동 전이라 파라미터만 넘김)
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import Icon from "@/components/ui/Icon";
import type { CalendarType, Gender } from "@/lib/types";

const nowYear = new Date().getFullYear();

export default function BirthInputForm() {
  const router = useRouter();

  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [day, setDay] = useState("");
  const [hour, setHour] = useState("");
  const [minute, setMinute] = useState("");
  const [hourUnknown, setHourUnknown] = useState(false);
  const [gender, setGender] = useState<Gender>("여");
  const [calendar, setCalendar] = useState<CalendarType>("solar");
  const [leap, setLeap] = useState(false);
  const [error, setError] = useState("");

  const showHourNotice = hourUnknown || hour === "";

  // 필수값(연/월/일) 검증
  const validate = (): string => {
    const y = Number(year);
    const m = Number(month);
    const d = Number(day);
    if (!year || !month || !day) return "생년월일(연·월·일)을 모두 입력해주세요.";
    if (y < 1900 || y > nowYear) return `연도는 1900~${nowYear} 사이여야 해요.`;
    if (m < 1 || m > 12) return "월은 1~12 사이여야 해요.";
    if (d < 1 || d > 31) return "일은 1~31 사이여야 해요.";
    if (!hourUnknown && hour !== "") {
      const h = Number(hour);
      if (h < 0 || h > 23) return "시는 0~23 사이여야 해요.";
    }
    return "";
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const err = validate();
    if (err) {
      setError(err);
      return;
    }
    setError("");

    const params = new URLSearchParams({
      year,
      month,
      day,
      gender,
      calendar,
      leap: String(calendar === "lunar" && leap),
    });
    if (!hourUnknown && hour !== "") {
      params.set("hour", hour);
      if (minute !== "") params.set("minute", minute);
    }
    router.push(`/result?${params.toString()}`);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* 생년월일 */}
      <Field label="생년월일" required>
        <div className="grid grid-cols-3 gap-2">
          <NumInput value={year} onChange={setYear} placeholder="1995" suffix="년" min={1900} max={nowYear} />
          <NumInput value={month} onChange={setMonth} placeholder="3" suffix="월" min={1} max={12} />
          <NumInput value={day} onChange={setDay} placeholder="12" suffix="일" min={1} max={31} />
        </div>
      </Field>

      {/* 출생 시각 (선택) */}
      <Field label="출생 시각" hint="모르면 비워두세요">
        <div className="grid grid-cols-2 gap-2">
          <NumInput
            value={hour}
            onChange={setHour}
            placeholder="14"
            suffix="시"
            min={0}
            max={23}
            disabled={hourUnknown}
          />
          <NumInput
            value={minute}
            onChange={setMinute}
            placeholder="20"
            suffix="분"
            min={0}
            max={59}
            disabled={hourUnknown}
          />
        </div>
        <label className="mt-2 flex items-center gap-2 text-sm text-sub">
          <input
            type="checkbox"
            checked={hourUnknown}
            onChange={(e) => setHourUnknown(e.target.checked)}
            className="h-4 w-4 accent-[color:var(--color-primary)]"
          />
          태어난 시각을 몰라요
        </label>
        {showHourNotice && (
          <p className="mt-2 rounded-btn bg-surface px-3 py-2 text-xs text-sub">
            ⏱ 시주 제외, <b className="text-text">연·월·일주만 계산</b>됩니다.
          </p>
        )}
      </Field>

      {/* 성별 / 양음력 토글 */}
      <div className="grid grid-cols-2 gap-4">
        <Field label="성별">
          <SegToggle
            options={["여", "남"]}
            value={gender}
            onChange={(v) => setGender(v as Gender)}
          />
        </Field>
        <Field label="달력">
          <SegToggle
            options={[
              { value: "solar", label: "양력" },
              { value: "lunar", label: "음력" },
            ]}
            value={calendar}
            onChange={(v) => setCalendar(v as CalendarType)}
          />
        </Field>
      </div>

      {/* 윤달 (음력일 때만) */}
      {calendar === "lunar" && (
        <label className="flex items-center gap-2 text-sm text-sub">
          <input
            type="checkbox"
            checked={leap}
            onChange={(e) => setLeap(e.target.checked)}
            className="h-4 w-4 accent-[color:var(--color-primary)]"
          />
          윤달로 태어났어요
        </label>
      )}

      {error && (
        <p className="rounded-btn bg-red-50 px-3 py-2 text-sm text-red-600">{error}</p>
      )}

      <button type="submit" className="btn-primary w-full">
        <Icon name="sparkles" size={18} /> 내 사주 보기
      </button>
    </form>
  );
}

/* ---------- 하위 UI 조각 ---------- */

function Field({
  label,
  required,
  hint,
  children,
}: {
  label: string;
  required?: boolean;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <div className="mb-1.5 flex items-baseline justify-between">
        <label className="text-sm font-bold text-text">
          {label}
          {required && <span className="ml-0.5 text-primary">*</span>}
        </label>
        {hint && <span className="text-xs text-sub">{hint}</span>}
      </div>
      {children}
    </div>
  );
}

function NumInput({
  value,
  onChange,
  placeholder,
  suffix,
  min,
  max,
  disabled,
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  suffix?: string;
  min?: number;
  max?: number;
  disabled?: boolean;
}) {
  return (
    <div
      className={`flex items-center rounded-btn border border-border bg-background px-3 focus-within:border-primary ${
        disabled ? "opacity-50" : ""
      }`}
    >
      <input
        type="number"
        inputMode="numeric"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        min={min}
        max={max}
        disabled={disabled}
        className="w-full bg-transparent py-2.5 text-text outline-none [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none"
      />
      {suffix && <span className="ml-1 text-sm text-sub">{suffix}</span>}
    </div>
  );
}

type Opt = string | { value: string; label: string };

function SegToggle({
  options,
  value,
  onChange,
}: {
  options: Opt[];
  value: string;
  onChange: (v: string) => void;
}) {
  const norm = useMemo(
    () =>
      options.map((o) =>
        typeof o === "string" ? { value: o, label: o } : o
      ),
    [options]
  );
  return (
    <div className="grid grid-cols-2 gap-1 rounded-btn border border-border bg-surface p-1">
      {norm.map((o) => (
        <button
          key={o.value}
          type="button"
          onClick={() => onChange(o.value)}
          className={`rounded-[7px] py-2 text-sm font-bold transition-colors ${
            value === o.value
              ? "bg-primary text-white"
              : "text-sub hover:text-text"
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}
