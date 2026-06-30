#!/usr/bin/env python3
"""간다GO — 서초 출장마사지·홈타이 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 저장소 루트에 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import json
import os
import re
import sys
from datetime import date, datetime, timezone, timedelta
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.info import AGG_RATING_COUNT, AGG_RATING_VALUE
from content.site import (BASE_URL, BRAND, INDEXNOW_KEY, NAV, PHONE, PHONE_DISPLAY)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000
KST = timezone(timedelta(hours=9))
TODAY = date.today().isoformat()
BASE = BASE_URL.rstrip("/")
PRICE_LOW, PRICE_HIGH, PRICE_COUNT = "90000", "180000", "3"


# ── 내부링크 강화용 데이터 ──────────────────────────────────────────────
def _nav_children(top_href):
    for _label, href, children in NAV:
        if href == top_href:
            return [(c_label, c_href) for c_label, c_href in children
                    if "#" not in c_href and c_href != top_href]
    return []


AREA_LINKS = _nav_children("/seocho-gu/")          # 대표 동 6곳
STATION_LINKS = _nav_children("/seocho-gu/stations/")  # 역 21곳
THEME_LINKS = _nav_children("/themes/")            # 테마 14개

# 지역(동) 롱테일 주제 — 메인·관련링크 공용
AREA_LONGTAIL = {
    "/seocho-gu/seocho-dong/": "서초동 법조타운·강남대로 심야 출장마사지",
    "/seocho-gu/jamwon-dong/": "잠원동 한강변 운동 후 회복 홈타이",
    "/seocho-gu/banpo-dong/": "반포동 고속터미널·호텔 출장 홈타이",
    "/seocho-gu/bangbae-dong/": "방배동 주택가 정기 방문 마사지",
    "/seocho-gu/yangjae-dong/": "양재동 기업 사옥·야근 후 출장마사지",
    "/seocho-gu/naegok-dong/": "내곡동 청계산 등산 후 회복 마사지",
}
AREA_SUB = {
    "/seocho-gu/seocho-dong/": "야근·법원 인근 호텔 방문 조건",
    "/seocho-gu/jamwon-dong/": "러닝·라이딩 후 하체 회복 안내",
    "/seocho-gu/banpo-dong/": "터미널·호텔 객실 방문 안내",
    "/seocho-gu/bangbae-dong/": "단독·빌라 정기 방문 안내",
    "/seocho-gu/yangjae-dong/": "사옥·출장 숙소 야간 방문",
    "/seocho-gu/naegok-dong/": "신축 단지·산행 회복 안내",
}


def render_related(path):
    """지역·역·테마 상세 페이지 하단에 들어가는 롱테일 교차링크 블록.
    번호 매겨진 본문 섹션과 구분하기 위해 <nav>로 출력한다."""
    p = "/" + path

    # 대표 동 지역 페이지 — 롱테일 카드 강조
    is_dong = path.startswith("seocho-gu/") and "/stations/" not in path \
        and path != "seocho-gu/" and p in AREA_LONGTAIL
    if is_dong:
        cards = "".join(
            f'<a href="{href}"><strong>{AREA_LONGTAIL[href]}</strong>'
            f'<span>{AREA_SUB[href]}</span></a>'
            for _label, href in AREA_LINKS if href != p
        )
        return (
            '<nav class="related" aria-label="서초구 다른 지역 안내">'
            '<p class="related-title">서초구 다른 지역도 함께 보세요</p>'
            f'<div class="longtail-grid">{cards}</div>'
            '<p class="related-more">'
            '<a href="/seocho-gu/">서초구 전체 지역 안내</a>'
            ' · <a href="/seocho-gu/stations/">지하철역별 안내</a>'
            ' · <a href="/themes/">테마별 관리 안내</a></p></nav>'
        )

    # 역 상세 페이지 — 인접 역 메시 + 지역 롱테일
    if "/stations/" in path and path != "seocho-gu/stations/":
        sibs = [(l, h) for l, h in STATION_LINKS if h != p]
        idx = next((i for i, (l, h) in enumerate(STATION_LINKS) if h == p), 0)
        rotated = sibs[idx:] + sibs[:idx]
        cells = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in rotated)
        area_more = " · ".join(
            f'<a href="{h}">{AREA_LONGTAIL[h].split()[0]}</a>' for _l, h in AREA_LINKS
        )
        return (
            '<nav class="related" aria-label="가까운 역·지역 안내">'
            '<p class="related-title">가까운 역·지역 안내 더 보기</p>'
            f'<ul class="card-grid">{cells}</ul>'
            f'<p class="related-more">지역으로 찾기: {area_more}'
            ' · <a href="/seocho-gu/">전체 지역</a></p></nav>'
        )

    # 테마 상세 페이지 — 다른 테마 메시 + 지역 롱테일
    if path.startswith("themes/") and path != "themes/":
        sibs = [(l, h) for l, h in THEME_LINKS if h != p]
        idx = next((i for i, (l, h) in enumerate(THEME_LINKS) if h == p), 0)
        rotated = sibs[idx:] + sibs[:idx]
        cells = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in rotated)
        area_more = " · ".join(
            f'<a href="{h}">{AREA_LONGTAIL[h].split()[0]}</a>' for _l, h in AREA_LINKS
        )
        return (
            '<nav class="related" aria-label="다른 테마·지역 안내">'
            '<p class="related-title">다른 테마·지역 안내</p>'
            f'<ul class="card-grid">{cells}</ul>'
            f'<p class="related-more">지역별 안내: {area_more}'
            ' · <a href="/themes/">전체 테마</a></p></nav>'
        )

    return ""


def inject_related(body, path):
    """관련 링크 블록을 본문 끝 CTA 앞에 삽입한다."""
    block = render_related(path)
    if not block:
        return body
    marker = '<section class="cta">'
    i = body.rfind(marker)
    if i != -1:
        return body[:i] + block + "\n" + body[i:]
    return body + "\n" + block


# ── 구조화 데이터(JSON-LD) ─────────────────────────────────────────────
def _clean(text):
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def extract_faqs(body):
    pairs = re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', body, flags=re.S
    )
    return [(_clean(q), _clean(a)) for q, a in pairs]


def _org_node():
    return {
        "@type": "HealthAndBeautyBusiness",
        "@id": f"{BASE}/#org",
        "name": BRAND,
        "url": f"{BASE}/",
        "telephone": PHONE,
        "image": f"{BASE}/assets/og-image.png",
        "logo": f"{BASE}/assets/icon-512.png",
        "priceRange": "₩90,000 - ₩180,000",
        "openingHours": "Mo-Su 00:00-24:00",
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 서초구"},
        "address": {"@type": "PostalAddress", "addressLocality": "서초구",
                    "addressRegion": "서울특별시", "addressCountry": "KR"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": AGG_RATING_VALUE,
            "reviewCount": AGG_RATING_COUNT,
            "bestRating": "5",
            "worstRating": "1",
        },
    }


def _website_node():
    return {
        "@type": "WebSite",
        "@id": f"{BASE}/#website",
        "url": f"{BASE}/",
        "name": BRAND,
        "inLanguage": "ko",
        "publisher": {"@id": f"{BASE}/#org"},
    }


def is_service_page(path):
    return (path.startswith("seocho-gu/") or path.startswith("themes/")
            or path in ("massage/", "courses/"))


def build_jsonld(page, canonical, body):
    path = page["path"]
    crumbs = page.get("breadcrumb") or []
    graph = [_org_node(), _website_node()]

    # 빵부스러기(BreadcrumbList) — 하위 경로가 있는 페이지
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"}]
        for n, (label, href) in enumerate(crumbs, start=2):
            item = f"{BASE}{href}" if href else canonical
            items.append({"@type": "ListItem", "position": n,
                          "name": _clean(label), "item": item})
        graph.append({"@type": "BreadcrumbList",
                      "@id": canonical + "#breadcrumb", "itemListElement": items})

    # FAQ — 본문에 faq-item이 있으면 자동 수집
    faqs = extract_faqs(body)
    if faqs:
        graph.append({
            "@type": "FAQPage", "@id": canonical + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    # Service — 지역·역·테마·출장마사지·코스 페이지
    if is_service_page(path):
        graph.append({
            "@type": "Service", "@id": canonical + "#service",
            "name": _clean(page["h1"]),
            "serviceType": "출장마사지·홈타이 방문 관리",
            "provider": {"@id": f"{BASE}/#org"},
            "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 서초구"},
            "url": canonical,
            "offers": {"@type": "AggregateOffer", "priceCurrency": "KRW",
                       "lowPrice": PRICE_LOW, "highPrice": PRICE_HIGH,
                       "offerCount": PRICE_COUNT},
        })

    data = {"@context": "https://schema.org", "@graph": graph}
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path
    # 구조화 데이터(JSON-LD) 자동 주입 + 페이지 고유 스키마(extra_head) 유지
    extra_head = build_jsonld(page, canonical, body) + extra_head
    # 롱테일 교차링크 블록 삽입
    body = inject_related(body, path)
    naver_verify = (
        '<meta name="naver-site-verification" content="9c20cdc0db9c377a61bc188e5bd1494bd8234667">\n'
        if path == ""
        else ""
    )

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{naver_verify}{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 매거진 RSS" href="{BASE_URL.rstrip('/')}/rss.xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">G</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 서초구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">서초구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 서울특별시 서초구 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/massage/">서초 출장마사지</a></li>
        <li><a href="/seocho-gu/">지역별 안내</a></li>
        <li><a href="/seocho-gu/stations/">지하철역별 안내</a></li>
        <li><a href="/themes/">테마별 안내</a></li>
        <li><a href="/courses/">코스안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/guide/">이용가이드</a></li>
        <li><a href="/magazine/">매거진</a></li>
        <li><a href="/reviews/">이용 후기</a></li>
        <li><a href="/support/">고객센터</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


NOT_FOUND = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>페이지를 찾을 수 없습니다 | {BRAND}</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<main class="site-main">
  <div class="container" style="text-align:center; padding-top:80px;">
    <h1>페이지를 찾을 수 없습니다</h1>
    <p>주소가 바뀌었거나 존재하지 않는 페이지입니다.<br>아래 메뉴에서 원하시는 안내를 찾아보세요.</p>
    <ul class="card-grid" style="max-width:640px; margin:30px auto;">
      <li><a href="/">홈</a></li>
      <li><a href="/seocho-gu/">지역별 안내</a></li>
      <li><a href="/seocho-gu/stations/">지하철역별 안내</a></li>
      <li><a href="/themes/">테마별 안내</a></li>
      <li><a href="/reservation/">예약안내</a></li>
      <li><a href="/support/">고객센터</a></li>
    </ul>
    <p><a class="cta-phone" href="tel:{PHONE}" style="display:inline-block;background:#c9a96a;color:#15120b;font-weight:800;padding:12px 32px;border-radius:30px;">예약문의 {PHONE_DISPLAY}</a></p>
  </div>
</main>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []

    for page in PAGES:
        path = page["path"]  # "" 또는 "seocho-gu/banpo-dong/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            sitemap_urls.append(BASE_URL.rstrip("/") + "/" + path)
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # 404.html
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(NOT_FOUND)

    # sitemap.xml (lastmod·changefreq·priority 포함 — 색인 우선순위 신호)
    def _sm_hint(u):
        rel = u[len(BASE):].strip("/")          # "" 또는 "seocho-gu/banpo-dong"
        if rel == "":
            return "daily", "1.0"
        depth = rel.count("/")
        if depth == 0 or rel in ("seocho-gu/stations",):
            return "weekly", "0.8"               # 허브 페이지
        return "weekly", "0.6"                   # 상세 페이지

    rows = []
    for u in sitemap_urls:
        freq, pri = _sm_hint(u)
        rows.append(
            f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{pri}</priority></url>"
        )
    urls = "\n".join(rows)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 매거진 아티클 피드 (네이버 서치어드바이저 RSS 제출용)
    items = []
    for page in PAGES:
        path = page["path"]
        if not path.startswith("magazine/") or path == "magazine/":
            continue
        m = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', page.get("extra_head", ""))
        pub = datetime.fromisoformat(m.group(1)).replace(hour=9, tzinfo=KST) if m \
            else datetime.now(KST)
        link = BASE_URL.rstrip("/") + "/" + path
        items.append((pub, (
            "  <item>\n"
            f"    <title>{escape(page['h1'])}</title>\n"
            f"    <link>{link}</link>\n"
            f"    <guid isPermaLink=\"true\">{link}</guid>\n"
            f"    <description>{escape(page['desc'])}</description>\n"
            f"    <pubDate>{pub.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>\n"
            "  </item>"
        )))
    items.sort(key=lambda x: x[0], reverse=True)
    now_rfc = datetime.now(KST).strftime("%a, %d %b %Y %H:%M:%S %z")
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "<channel>\n"
            f"  <title>{escape(BRAND)} 매거진</title>\n"
            f"  <link>{BASE_URL.rstrip('/')}/magazine/</link>\n"
            "  <description>서초 방문 관리 이용 가이드와 휴식·컨디션 관리 정보</description>\n"
            "  <language>ko</language>\n"
            f"  <lastBuildDate>{now_rfc}</lastBuildDate>\n"
            f'  <atom:link href="{BASE_URL.rstrip("/")}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            + "\n".join(it for _, it in items)
            + "\n</channel>\n</rss>\n"
        )

    # robots.txt — 주요 검색봇 전체 허용 + sitemap (색인 속도 우선)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: Googlebot\nAllow: /\n\n"        # 구글
            "User-agent: Yeti\nAllow: /\n\n"             # 네이버
            "User-agent: Daumoa\nAllow: /\n\n"           # 다음(카카오)
            "User-agent: Bingbot\nAllow: /\n\n"          # 빙
            f"Sitemap: {BASE_URL.rstrip('/')}/sitemap.xml\n"
        )

    # IndexNow 키 파일 (소유 증명 — 키 이름의 txt 파일에 키 값)
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
