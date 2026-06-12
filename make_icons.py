#!/usr/bin/env python3
"""브랜드 아이콘·OG 이미지 생성 (Pillow 필요: pip install pillow).

노원 템플릿과 동일한 다크 네이비 + 골드 디자인에 'G' 모노그램을 적용한다.
한 번 생성해 저장소에 커밋해 두는 용도이며, 빌드마다 실행할 필요는 없다.
"""
from PIL import Image, ImageDraw, ImageFont

NAVY = (10, 17, 32)
NAVY_LIGHT = (16, 26, 47)
GOLD = (200, 162, 94)
CREAM = (233, 215, 171)
GREY = (170, 180, 198)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def monogram(size: int) -> Image.Image:
    """원형 골드 링 + G 모노그램."""
    s = size * 4  # 4x 슈퍼샘플링
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    m = s * 0.02
    d.ellipse([m, m, s - m, s - m], fill=NAVY)
    ring_w = int(s * 0.035)
    d.ellipse([m + ring_w, m + ring_w, s - m - ring_w, s - m - ring_w],
              outline=GOLD, width=ring_w)
    inner = int(s * 0.085)
    d.ellipse([inner, inner, s - inner, s - inner],
              outline=GOLD + (90,), width=max(2, int(s * 0.008)))
    font = ImageFont.truetype(SERIF_BOLD, int(s * 0.5))
    bbox = d.textbbox((0, 0), "G", font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((s - w) / 2 - bbox[0], (s - h) / 2 - bbox[1]), "G",
           font=font, fill=CREAM)
    return im.resize((size, size), Image.LANCZOS)


def spaced(text: str, n: int = 2) -> str:
    return (" " * n).join(text)


def og_image() -> Image.Image:
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    # 상단 은은한 라디얼 글로우
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for r, a in [(560, 26), (440, 20), (330, 14)]:
        gd.ellipse([W / 2 - r, -r * 0.9, W / 2 + r, r * 1.1], fill=a)
    im.paste(Image.new("RGB", (W, H), NAVY_LIGHT), (0, 0), glow)
    # 상단·하단 골드 바
    d.rectangle([0, 0, W, 10], fill=GOLD)
    d.rectangle([0, H - 10, W, H], fill=GOLD)
    # 모노그램
    mg = monogram(220)
    im.paste(mg, (int(W / 2 - 110), 78), mg)
    # 브랜드 타이포
    f_brand = ImageFont.truetype(SERIF_BOLD, 92)
    f_sub = ImageFont.truetype(SANS, 30)
    f_phone = ImageFont.truetype(SANS, 32)

    def center(text, font, y, fill):
        bbox = d.textbbox((0, 0), text, font=font)
        d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], y), text, font=font, fill=fill)

    center("GANDA GO", f_brand, 340, CREAM)
    center(spaced("PREMIUM VISITING SPA"), f_sub, 480, GOLD)
    d.line([W / 2 - 160, 545, W / 2 + 160, 545], fill=(60, 70, 92), width=2)
    center("0 5 0 8 - 2 0 2 - 4 7 1 9", f_phone, 562, GREY)
    return im


def main():
    og_image().save("assets/og-image.png")
    for size, name in [(16, "assets/favicon-16.png"), (32, "assets/favicon-32.png"),
                       (180, "assets/apple-touch-icon.png"),
                       (192, "assets/icon-192.png"), (512, "assets/icon-512.png")]:
        monogram(size).save(name)
    monogram(48).save("favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)])
    print("아이콘·OG 이미지 생성 완료")


if __name__ == "__main__":
    main()
