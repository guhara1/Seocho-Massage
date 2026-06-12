#!/usr/bin/env python3
"""콘텐츠 모듈 단독 검증 — content/__init__.py(전체 집계)를 거치지 않고
개별 모듈만 로드해 페이지별 본문 글자수·메타 길이를 확인한다.

사용: python3 check_content.py areas
      python3 check_content.py stations stations2 themes
"""
import html
import importlib.util
import re
import sys
import types
from pathlib import Path

ROOT = Path(__file__).parent
MIN, MAX = 2000, 2500

# content 패키지를 __init__ 실행 없이 등록한다.
pkg = types.ModuleType("content")
pkg.__path__ = [str(ROOT / "content")]
sys.modules["content"] = pkg


def load(name):
    full = f"content.{name}"
    if full in sys.modules:
        return sys.modules[full]
    spec = importlib.util.spec_from_file_location(full, ROOT / "content" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[full] = mod
    spec.loader.exec_module(mod)
    return mod


def text_length(body):
    t = re.sub(r'<section class="pricing">.*?</section>', " ", body, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return len(re.sub(r"\s+", " ", t).strip())


load("site")
load("pricing")

DEPS = {"main": [], "areas": [], "stations": [], "stations2": [],
        "themes": [], "info": [], "magazine": [], "about": []}

ok = True
for name in sys.argv[1:]:
    for dep in DEPS.get(name, []):
        load(dep)
    mod = load(name)
    pages = getattr(mod, "PAGES", None) or [getattr(mod, "PAGE")]
    for p in pages:
        chars = text_length(p["body"])
        dlen = len(p["desc"])
        flags = []
        if not p.get("noindex") and not (MIN <= chars <= MAX):
            flags.append("본문범위밖")
            ok = False
        if not (50 <= dlen <= 160):
            flags.append("desc길이")
            ok = False
        kw = len(re.findall("출장마사지", p["body"]))
        if kw > 5:
            flags.append(f"출장마사지 {kw}회")
            ok = False
        print(f"{(p['path'] or '/').ljust(46)} {str(chars).rjust(5)}자  desc {str(dlen).rjust(3)}  {' '.join(flags)}")

print("\nOK" if ok else "\n⚠ 위 항목을 수정하세요")
sys.exit(0 if ok else 1)
