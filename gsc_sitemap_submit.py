#!/usr/bin/env python3
"""구글 서치콘솔 API로 sitemap 제출 — 폐기된 sitemap ping의 공식 대체 수단.

구글 sitemap ping 엔드포인트(google.com/ping)는 2024년 1월 폐기되었다.
지금 구글에 sitemap 갱신을 알리는 공식 경로는 두 가지:
  1) robots.txt 의 Sitemap 라인 (이미 적용됨)
  2) Search Console Sitemaps API 로 제출 — 이 스크립트가 하는 일

Indexing API와 달리 페이지 유형 제한이 없는 정식 방법이므로 안심하고 자동화해도 된다.

설정 (google_indexing.py와 같은 서비스 계정을 공유):
  1. Google Cloud 프로젝트에서 "Google Search Console API" 활성화
  2. 서비스 계정 생성 → JSON 키 다운로드 → service_account.json 로 저장 (커밋 금지!)
  3. Search Console 속성(https://seocho-massage.pages.dev/)에
     서비스 계정 이메일을 '소유자' 권한으로 추가
  4. pip install google-auth requests

사용: python3 gsc_sitemap_submit.py
  속성 주소가 다르면 환경변수 GSC_SITE_URL 로 지정 (예: sc-domain:example.com)
"""
import os
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content.site import BASE_URL

SCOPES = ["https://www.googleapis.com/auth/webmasters"]
KEY_FILE = Path(__file__).with_name("service_account.json")

SITE_URL = os.environ.get("GSC_SITE_URL", BASE_URL.rstrip("/") + "/")
SITEMAP_URL = BASE_URL.rstrip("/") + "/sitemap.xml"


def main():
    if not KEY_FILE.exists():
        sys.exit("service_account.json 이 없습니다. 파일 상단 주석의 설정 절차를 먼저 진행하세요.")

    try:
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account
    except ImportError:
        sys.exit("pip install google-auth requests 후 다시 실행하세요.")

    creds = service_account.Credentials.from_service_account_file(
        str(KEY_FILE), scopes=SCOPES)
    session = AuthorizedSession(creds)

    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{urllib.parse.quote(SITE_URL, safe='')}/sitemaps/"
        f"{urllib.parse.quote(SITEMAP_URL, safe='')}"
    )
    res = session.put(endpoint)
    if res.status_code in (200, 204):
        print(f"서치콘솔 sitemap 제출 완료: {SITEMAP_URL} → {SITE_URL}")
    else:
        print(f"제출 실패 ({res.status_code}): {res.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
