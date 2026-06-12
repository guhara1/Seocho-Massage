#!/usr/bin/env python3
"""META(title/h1/description) 도어웨이 패턴 검사.

지역·테마명(첫 토큰)을 마스킹한 뒤 동일 골격이 몇 번 반복되는지 집계한다.
빌드된 HTML(*/index.html)을 직접 읽으므로 build.py 실행 후 사용한다.
사용: python3 meta_check.py                      # 전체
      python3 meta_check.py seocho-gu/stations   # 특정 디렉터리/접두어만
"""
import re
import sys
from collections import Counter
from pathlib import Path

prefix = sys.argv[1] if len(sys.argv) > 1 else ""
metas = []
for p in sorted(Path(".").rglob("index.html")):
    rel = str(p.parent).lstrip("./")
    if rel.startswith((".git", "node_modules")) or not rel.startswith(prefix):
        continue
    raw = p.read_text(encoding="utf-8")
    if '<meta name="robots" content="noindex' in raw:
        continue  # noindex 페이지는 골격 검사 대상에서 제외
    t = re.search(r"<title>(.*?)</title>", raw, re.S)
    d = re.search(r'name="description" content="(.*?)"', raw)
    h = re.search(r"<h1>(.*?)</h1>", raw, re.S)
    if not (t and d and h):
        continue
    metas.append((rel or "/", t.group(1).strip(),
                  d.group(1).strip(), re.sub(r"<[^>]+>", " ", h.group(1)).strip()))


def mask(s):
    return re.sub(r"^[^\s—|,·]+", "〈X〉", s)


print(f"검사 대상: {len(metas)}페이지\n")
problems = 0
# H1은 플레이북이 정한 정형 패턴("○○역 인근 방문 관리 안내")이라 반복이 정상 —
# 정보로만 출력하고 실패 기준은 타이틀·디스크립션 골격에만 적용한다.
for label, idx, fatal in [("타이틀", 1, True), ("H1", 3, False)]:
    c = Counter(mask(m[idx]) for m in metas)
    dups = [(s, n) for s, n in c.most_common() if n >= 3]
    print(f"=== {label} 골격 3회 이상 반복 ===" + ("" if fatal else " (참고용)"))
    if dups:
        if fatal:
            problems += 1
        for s, n in dups:
            print(f"{n:4d}  {s}")
    else:
        print("  없음 ✓")
    print()

c = Counter(mask(m[2])[:22] for m in metas)
dups = [(s, n) for s, n in c.most_common() if n >= 3]
print("=== 디스크립션 시작 골격(22자) 3회 이상 반복 ===")
if dups:
    problems += 1
    for s, n in dups:
        print(f"{n:4d}  {s}")
else:
    print("  없음 ✓")

# 길이 검사
print("\n=== 길이 이상 ===")
bad = False
for rel, t, d, h in metas:
    tl = len(t)
    if not 12 <= tl <= 60:
        print(f"  타이틀 {tl}자: {rel} — {t}")
        bad = True
    if not 50 <= len(d) <= 160:
        print(f"  디스크립션 {len(d)}자: {rel}")
        bad = True
if not bad:
    print("  없음 ✓")
sys.exit(1 if problems else 0)
