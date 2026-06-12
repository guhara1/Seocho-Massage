# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "서초구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 서초구"
  }},
  "openingHours": "Mo-Su 00:00-24:00",
  "priceRange": "₩90,000 - ₩180,000"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "서초구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내 페이지에서 서초동, 잠원동, 반포동, 방배동, 양재동, 내곡동 대표 동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "강남역이나 고속터미널역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "서초1동과 서초2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "서초1동부터 서초4동까지는 서초동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다. 반포·방배·양재의 숫자 행정동도 같은 기준입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "테마별 관리는 어디에서 확인하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "스웨디시, 타이마사지, 홈케어 등 테마별 안내 페이지에서 특징과 추천 대상을 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 서초구 전지역</p>
    <h1>서초 출장마사지·홈타이<br>예약 안내</h1>
    <p class="hero-lead">샵을 찾아 나설 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>자택·오피스텔·호텔 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>6개</strong><span>대표 지역</span></li>
      <li><strong>21개</strong><span>역세권 안내</span></li>
      <li><strong>14개</strong><span>관리 테마</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>서초 출장마사지·홈타이 서비스 안내</h2>
<p>야근을 마친 강남대로 사무실, 출장길의 고속터미널 인근 호텔, 쉬고 싶은 반포 자택까지 서초구 어디에 계시든 전화 한 통으로 방문 관리를 예약하실 수 있습니다. 이 페이지는 서초 출장마사지와 홈타이 예약 정보를 한눈에 보여주는 허브입니다. 지역·역·테마별 상세 내용은 각 안내 페이지로 연결되며, {BRAND}는 상담부터 방문, 관리 종료까지 전 과정을 안내된 기준 안에서만 진행합니다.</p>
</section>

<section id="coverage">
<h2>서초구 전지역 방문 가능 안내</h2>
<p>서초구 지역 안내는 서초동, 잠원동, 반포동, 방배동, 양재동, 내곡동 여섯 개 대표 동을 중심으로 구성했습니다. 서초1동부터 서초4동, 반포본동과 반포1동부터 4동, 방배본동과 방배1동부터 4동, 양재1·2동처럼 숫자로 나뉜 행정동은 따로 페이지를 만들지 않고 각 대표 동 페이지에서 통합해 안내합니다. 생활권을 잘게 쪼개 비슷한 설명을 반복하기보다, 동 단위로 묶어 정확하게 설명하는 쪽이 이용자에게 도움이 되기 때문입니다.</p>
</section>

<section id="areas">
<h2>지역별 안내</h2>
<p>법조타운과 오피스가 모인 서초동, 한강변 아파트 단지의 잠원동, 터미널과 호텔이 있는 반포동, 조용한 주택가의 방배동, 기업 사옥이 모인 양재동, 청계산 자락의 내곡동 — 각 페이지에서 동별 특징과 방문 조건을 고유하게 설명합니다.</p>
<ul class="card-grid">
<li><a href="/seocho-gu/seocho-dong/">서초동</a></li>
<li><a href="/seocho-gu/jamwon-dong/">잠원동</a></li>
<li><a href="/seocho-gu/banpo-dong/">반포동</a></li>
<li><a href="/seocho-gu/bangbae-dong/">방배동</a></li>
<li><a href="/seocho-gu/yangjae-dong/">양재동</a></li>
<li><a href="/seocho-gu/naegok-dong/">내곡동</a></li>
</ul>
<p>서초구 전체 구조가 궁금하시면 <a href="/seocho-gu/">서초구 전체 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>지하철역 인근 안내</h2>
<p>서초구는 2·3·4·7·9호선과 신분당선까지 여섯 개 노선이 지나는 교통 요지입니다. 역별 안내는 주요 역세권을 기준으로 구성하며, 각 역 페이지에서 인근 생활권과 가까운 대표 동, 방문 형태, 예약 팁을 설명합니다. 출구별 페이지나 역과 테마를 조합한 페이지는 만들지 않으며, 환승역은 노선이 몇 개라도 페이지 하나로 운영합니다.</p>
<ul class="card-grid">
<li><a href="/seocho-gu/stations/gangnam-station/">강남역</a></li>
<li><a href="/seocho-gu/stations/gyodae-station/">교대역</a></li>
<li><a href="/seocho-gu/stations/seocho-station/">서초역</a></li>
<li><a href="/seocho-gu/stations/bangbae-station/">방배역</a></li>
<li><a href="/seocho-gu/stations/sadang-station/">사당역</a></li>
<li><a href="/seocho-gu/stations/jamwon-station/">잠원역</a></li>
<li><a href="/seocho-gu/stations/express-bus-terminal-station/">고속터미널역</a></li>
<li><a href="/seocho-gu/stations/nambu-bus-terminal-station/">남부터미널역</a></li>
<li><a href="/seocho-gu/stations/yangjae-station/">양재역</a></li>
<li><a href="/seocho-gu/stations/chongshin-univ-station/">총신대입구역</a></li>
<li><a href="/seocho-gu/stations/dongjak-station/">동작역</a></li>
<li><a href="/seocho-gu/stations/nonhyeon-station/">논현역</a></li>
<li><a href="/seocho-gu/stations/banpo-station/">반포역</a></li>
<li><a href="/seocho-gu/stations/naebang-station/">내방역</a></li>
<li><a href="/seocho-gu/stations/isu-station/">이수역</a></li>
<li><a href="/seocho-gu/stations/sinnonhyeon-station/">신논현역</a></li>
<li><a href="/seocho-gu/stations/sapyeong-station/">사평역</a></li>
<li><a href="/seocho-gu/stations/sinbanpo-station/">신반포역</a></li>
<li><a href="/seocho-gu/stations/gubanpo-station/">구반포역</a></li>
<li><a href="/seocho-gu/stations/yangjae-citizens-forest-station/">양재시민의숲역</a></li>
<li><a href="/seocho-gu/stations/cheonggyesan-station/">청계산입구역</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>관리 유형은 열네 가지 테마로 나누어 각각 독립 페이지에서 특징, 추천 대상, 받기 전 확인사항을 설명합니다. 지역 페이지와 역 페이지에서는 어울리는 테마로 연결만 해 드리며, 특정 역과 테마를 조합한 페이지는 운영하지 않습니다. 원하시는 관리 유형을 먼저 고른 뒤, 예약 전화에서 위치를 알려주시면 됩니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/lomilomi/">로미로미</a></li>
<li><a href="/themes/thai/">타이마사지</a></li>
<li><a href="/themes/chinese/">중국마사지</a></li>
<li><a href="/themes/aroma/">아로마테라피</a></li>
<li><a href="/themes/homecare/">홈케어</a></li>
<li><a href="/themes/hotel-style/">호텔식마사지</a></li>
<li><a href="/themes/foot/">발마사지</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/skincare/">스킨케어</a></li>
<li><a href="/themes/waxing/">왁싱</a></li>
<li><a href="/themes/couple/">커플 관리</a></li>
<li><a href="/themes/24hours/">24시간</a></li>
<li><a href="/themes/overnight/">수면 가능</a></li>
</ul>
</section>

<section id="course">
<h2>코스 선택 안내</h2>
<p>코스는 이용 목적과 그날의 컨디션으로 고르시는 것이 가장 정확합니다. 누적된 피로를 풀고 싶은 분, 향과 함께 깊은 휴식이 필요한 분, 운동이나 등산 뒤 근육 이완이 필요한 분, 호텔이나 숙소로 방문을 원하시는 분, 둘이 나란히 받고 싶은 커플까지 상황별 선택 기준을 <a href="/courses/">코스안내</a>에서 자세히 다룹니다.</p>
</section>

<section id="how">
<h2>예약 진행 방식</h2>
<p>예약은 다섯 단계로 진행됩니다. 희망 지역 또는 역 인근 위치 확인, 희망 시간 확인, 코스와 인원 확인, 방문 가능 여부 안내, 예약 확정 순서입니다. 서초구는 강남대로권, 반포·고속터미널권, 방배·사당권, 양재·내곡권으로 생활권이 나뉘어 있어 정확한 위치 확인이 중요합니다. 자세한 절차는 <a href="/reservation/">예약안내</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="check">
<h2>이용 전 확인사항</h2>
<p>원활한 방문을 위해 정확한 주소, 공동현관 출입 방법, 주차 가능 여부, 조용한 공간 확보 여부를 미리 확인해 주세요. 호텔이나 레지던스는 객실 호수와 로비 출입 안내를 함께 알려주시면 좋습니다. 준비사항 전체는 <a href="/guide/">이용가이드</a>에 정리되어 있습니다.</p>
</section>

<section id="safety">
<h2>위생 및 안전 안내</h2>
<p>건전하고 안전한 방문 관리를 위해 위생 기준, 예약 정보 확인, 개인정보 보호, 금지행위 기준을 명확히 운영합니다. 이용 전 서비스 범위와 유의사항을 확인해 주시고, 불법적이거나 무리한 요청은 어떤 경우에도 진행하지 않으며, 예약 정보는 방문 관리 목적 외에 사용하지 않습니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>서초구 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내 페이지에서 서초동, 잠원동, 반포동, 방배동, 양재동, 내곡동 대표 동 기준으로 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>강남역이나 고속터미널역 근처도 가능한가요?</h3>
<p>주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>서초1동과 서초2동은 왜 따로 없나요?</h3>
<p>서초1동부터 서초4동까지는 서초동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다. 반포·방배·양재의 숫자 행정동도 같은 기준입니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다.</p>
</div>
<div class="faq-item">
<h3>테마별 관리는 어디에서 확인하나요?</h3>
<p>스웨디시, 타이마사지, 홈케어 등 테마별 안내 페이지에서 특징과 추천 대상을 확인할 수 있습니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>서초구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "서초 출장마사지·홈타이 | 서초구 전지역 방문 마사지 예약 안내",
    "desc": "서초 출장마사지·홈타이 안내. 서초동·반포동·방배동·양재동과 주요 지하철역 인근 방문 관리, 테마별 코스, 예약 정보를 확인하세요.",
    "h1": "서초 출장마사지·홈타이 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
