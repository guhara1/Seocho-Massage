# 간다GO — 서초 출장마사지·홈타이 안내 사이트

서울 서초구 전지역 방문 관리(출장마사지·홈타이) 안내 정적 사이트.
구글·네이버 검색 가이드라인을 준수하는 구조(도어웨이·중복·얇은 콘텐츠 방지)로 설계되었다.
전체 제작 규칙은 [PLAYBOOK.md](PLAYBOOK.md) 참조.

- 상호: **간다GO** / 예약전화: **0508-202-4719**
- 페이지 구성: 메인 1 + 서초 출장마사지 안내 1 + 지역(허브+대표 동 6) + 지하철역(허브+역 21)
  + 테마(허브+14) + 코스·예약·가이드·후기·고객센터·약관 + 매거진(허브+6) + 운영자 소개

## 구조 원칙 (절대 규칙)

```
숫자 행정동 페이지 금지 — 서초1~4동→서초동, 반포본동·반포1~4동→반포동,
  방배본동·방배1~4동→방배동, 양재1·2동→양재동으로 통합
역 1개당 페이지 1개 — 환승역도 URL 하나, 출구별 페이지 금지
지역+역+테마 조합 페이지 금지 (강남역 스웨디시 ❌)
색인 페이지 본문 2,000~2,500자 (공통 요금 블록 제외 측정)
2,000자 미만은 빌드가 자동 noindex 처리
지역명·역명만 바꾼 복붙 페이지 금지 / 푸터 지역명 대량 나열 금지
건전 방문 관리 기준 — 불법·성매매 암시 문구 금지
```

## URL 구조

```
/                                메인 (서초 출장마사지·홈타이 예약 안내)
/massage/                        서초 출장마사지 종합 안내 (하위는 앵커)
/seocho-gu/                      지역 허브
/seocho-gu/{dong}-dong/          대표 동 6곳 (seocho, jamwon, banpo, bangbae, yangjae, naegok)
/seocho-gu/stations/             역 허브
/seocho-gu/stations/{station}/   역 21곳 (gangnam-station …)
/themes/{theme}/                 테마 14종
/courses/ /reservation/ /guide/ /reviews/ /support/(+privacy, terms)
/magazine/ /magazine/{slug}/     정보성 아티클 (Article JSON-LD + RSS)
/about/                          운영자 소개 (E-E-A-T)
```

## 빌드

```bash
python3 build.py          # 전체 HTML + sitemap.xml + rss.xml + robots.txt 생성
                          # 페이지별 글자수·색인 여부 리포트 출력 (⚠ 0건이어야 함)
python3 check_content.py areas stations stations2 themes info magazine about main
                          # 콘텐츠 모듈 단독 검증 (글자수·desc 길이·키워드 빈도)
python3 meta_check.py     # title/desc 도어웨이 골격 반복 검사
```

## 배포 전 체크리스트

- [ ] `content/site.py` 의 `BASE_URL` 을 실제 도메인으로 변경 후 **재빌드** (현재 placeholder)
- [ ] `python3 build.py` 경고(⚠) 0건 확인
- [ ] Search Console 등록 + sitemap.xml 제출, 네이버 서치어드바이저 등록 + RSS 제출
- [ ] IndexNow: 빌드가 생성하는 `<INDEXNOW_KEY>.txt` 가 루트에 배포되는지 확인
  (push 시 `.github/workflows/indexnow.yml` 이 자동 통보)
- [ ] 모바일 실기기 확인 (햄버거 메뉴, 전화 FAB, 요금 카드 1열)

## 콘텐츠 수정

페이지 정의는 모두 `content/` 파이썬 모듈에 있다 (생성된 HTML을 직접 고치지 말 것).

```
content/site.py        도메인·상호·전화·메뉴(NAV)·IndexNow 키
content/main.py        메인 (LocalBusiness/FAQPage JSON-LD + 히어로)
content/areas.py       지역 허브 + 대표 동 6
content/stations.py    역 허브 + 역 10  /  stations2.py  역 11
content/themes.py      테마 허브 + 14
content/info.py        massage·courses·reservation·guide·reviews·support·약관 2종
content/magazine.py    매거진 허브 + 아티클 6 (RSS 피드 소스)
content/about.py       운영자 소개
content/pricing.py     공용 요금 블록 (지역·역·메인 28페이지 삽입, 글자수 측정 제외)
```

요금 변경 시 `pricing.py` + `/courses/#price` 표 + 메인 JSON-LD `priceRange` 세 곳을 함께 맞출 것.
