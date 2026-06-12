# 전체 페이지 목록 집계
# (콘텐츠 모듈 작성 중에는 개별 모듈 단위로 검증할 수 있도록 import 실패를 허용하지 않는다.
#  모든 모듈이 준비된 뒤 아래 집계가 활성화된다.)
from . import main, areas, stations, stations2, themes, info, magazine, about

PAGES = (
    [main.PAGE]
    + areas.PAGES
    + stations.PAGES
    + stations2.PAGES
    + themes.PAGES
    + info.PAGES
    + magazine.PAGES
    + [about.PAGE]
)
