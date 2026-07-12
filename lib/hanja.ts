// 천간·지지 한글 → 한자 매핑 (OG 이미지 등 한자 표기용).
export const ganHanja: Record<string, string> = {
  갑: "甲", 을: "乙", 병: "丙", 정: "丁", 무: "戊",
  기: "己", 경: "庚", 신: "辛", 임: "壬", 계: "癸",
};

export const jiHanja: Record<string, string> = {
  자: "子", 축: "丑", 인: "寅", 묘: "卯", 진: "辰", 사: "巳",
  오: "午", 미: "未", 신: "申", 유: "酉", 술: "戌", 해: "亥",
};

export const toGan = (c: string) => ganHanja[c] ?? c;
export const toJi = (c: string) => jiHanja[c] ?? c;
