#!/usr/bin/env python3
"""구글 Indexing API 통보 스크립트 (선택 사용).

⚠ 주의 — 정책 안내:
  구글 Indexing API는 공식적으로 채용공고(JobPosting)·라이브방송(BroadcastEvent)
  구조화 데이터 페이지에만 허용된다. 일반 페이지에 사용하는 것은 정책 위반으로,
  구글이 2023년 이후 오남용 계정을 제재한 사례가 있다. 일반 사이트의 정석 루트는
    1) Search Console에 sitemap.xml 등록 (가장 중요)
    2) 신규/수정 페이지는 Search Console URL 검사 → 색인 요청
  이다. 참고로 구글 sitemap ping 엔드포인트(google.com/ping)는 2024년 1월
  폐기되어 더 이상 동작하지 않는다 — robots.txt의 Sitemap 라인과 GSC 등록이 대체 수단.

그래도 사용하려면:
  1. Google Cloud 프로젝트에서 Indexing API 활성화
  2. 서비스 계정 생성 → JSON 키 다운로드 → service_account.json 로 저장 (커밋 금지!)
  3. Search Console 속성에 해당 서비스 계정 이메일을 '소유자'로 추가
  4. pip install google-auth
  5. python3 google_indexing.py /magazine/new-post/

사용: python3 google_indexing.py <URL 경로>... 또는 --all (sitemap 전체)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content.site import BASE_URL

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
KEY_FILE = Path(__file__).with_name("service_account.json")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("사용법: google_indexing.py --all | <URL 경로>...")
    if not KEY_FILE.exists():
        sys.exit("service_account.json 이 없습니다. 파일 상단 주석의 설정 절차를 먼저 진행하세요.")

    try:
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account
    except ImportError:
        sys.exit("pip install google-auth 후 다시 실행하세요.")

    creds = service_account.Credentials.from_service_account_file(
        str(KEY_FILE), scopes=SCOPES)
    session = AuthorizedSession(creds)

    if args == ["--all"]:
        xml = Path(__file__).with_name("sitemap.xml").read_text(encoding="utf-8")
        urls = re.findall(r"<loc>(.*?)</loc>", xml)
    else:
        urls = [u if u.startswith("http") else BASE_URL.rstrip("/") + u for u in args]

    for url in urls:
        res = session.post(ENDPOINT, json={"url": url, "type": "URL_UPDATED"})
        print(f"{res.status_code}  {url}")
        if res.status_code == 429:
            print("일일 할당량(기본 200건/일) 초과 — 내일 다시 시도하세요.")
            break


if __name__ == "__main__":
    main()
