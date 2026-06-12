#!/usr/bin/env python3
"""IndexNow 색인 통보 — 빙·네이버 등 IndexNow 참여 검색엔진에 URL을 즉시 알린다.

api.indexnow.org 한 곳에만 보내면 참여 엔진 전체(Bing, Naver, Yandex, Seznam 등)에
자동 전파된다. 구글은 IndexNow 미참여이므로 별도(GSC sitemap)로 처리한다.

사용:
  python3 indexnow_ping.py --all            # sitemap.xml의 모든 URL 통보
  python3 indexnow_ping.py /magazine/new/   # 특정 URL만 통보 (여러 개 가능)

표준 라이브러리만 사용 (의존성 없음).
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content.site import BASE_URL, INDEXNOW_KEY

HOST = BASE_URL.split("//", 1)[1].rstrip("/")
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    xml = Path(__file__).with_name("sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>(.*?)</loc>", xml)


def ping(urls):
    # IndexNow는 요청당 최대 10,000개 URL 허용
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        # 200 OK 또는 202 Accepted 면 정상 접수
        print(f"IndexNow 응답: {res.status} — {len(urls)}개 URL 통보 완료")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("사용법: indexnow_ping.py --all | <URL 경로>...")
    if args == ["--all"]:
        urls = sitemap_urls()
    else:
        urls = [u if u.startswith("http") else BASE_URL.rstrip("/") + u for u in args]
    ping(urls)


if __name__ == "__main__":
    main()
