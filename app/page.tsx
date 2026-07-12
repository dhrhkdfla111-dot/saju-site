// 홈 (/) — Phase 2에서 생년월일시 입력 폼으로 확장 예정. 현재는 스캐폴딩 확인용.
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <section className="text-center">
        <h1 className="text-2xl font-bold sm:text-3xl">
          정확한 명식, 신뢰할 수 있는 해석
        </h1>
        <p className="mt-2 text-sub">
          생년월일시만 입력하면 사주 명식을 계산하고 개인화된 해석을 보여드려요.
        </p>
      </section>

      <Card title="입력 폼 (준비 중)" desc="Phase 2에서 구현됩니다.">
        <Button href="/result" variant="primary">
          결과 미리보기
        </Button>
      </Card>
    </div>
  );
}
