#!/usr/bin/env python3
"""Tối ưu tốc độ trang thenesthouse.com.vn (CEO 12/10/2026, học từ herb.vn — Lighthouse 97 desktop).

Chạy lại an toàn (idempotent). Dùng:
  python3 _scripts/toi_uu_toc_do.py            # cả repo: font tự host + ảnh webp + width/height + ảnh đầu ưu tiên + robots
  python3 _scripts/toi_uu_toc_do.py --dry      # chỉ đếm, không ghi
  python3 _scripts/toi_uu_toc_do.py cam-nang/bai-moi.html   # chỉ vài file (web-seo chạy cho bài mới trước khi commit)

Làm gì với mỗi trang .html:
  1. Font: bỏ link Google Fonts (chặn hiển thị ~0,5–4 giây trên điện thoại) → font tự host /assets/fonts/fonts.css + preload 2 file chữ thường.
  2. Ảnh <img src="/assets/x.jpg|png"> → /assets/x.webp (rộng tối đa 1600px, nhẹ hơn ~60–80%); og:image + schema giữ .jpg cho Facebook/Zalo/Google.
  3. Thêm width/height cho <img> thiếu (chống nhảy trang khi ảnh tải — CLS) + 1 dòng CSS :where(img[height]){height:auto} (độ ưu tiên 0, không đè CSS sẵn có).
  4. Ảnh nội dung đầu tiên: bỏ loading=lazy, thêm fetchpriority=high (ảnh lớn nhất màn hình đầu tải trước).
  5. <meta name="robots" content="max-image-preview:large"> cho trang được index (Google Discover/ảnh lớn) — trang noindex vĩnh viễn bỏ qua.
Phần 2–3 cần Pillow (máy Mac có); auto-publish trên GitHub chỉ gọi toi_uu_html(..., img=False).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
GF_RE = re.compile(r'[ \t]*<link[^>]+href="https://fonts\.googleapis\.com/css2\?family=Playfair\+Display:wght@600;700;800&family=Be\+Vietnam\+Pro:wght@400;500;600;700&display=swap"[^>]*>\n?')
PRECONNECT_RE = re.compile(r'[ \t]*<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"(?: crossorigin)?>\n?')
FONT_LINK_RE = re.compile(r'<link rel="stylesheet" href="/assets/fonts/fonts\.css">')
FONT_STYLE_RE = re.compile(r'<style data-tnh="fonts">.*?</style>', re.S)


def font_tags():
    """Đợt 2 (CEO 12/10): nhúng @font-face thẳng vào HTML (bỏ 1 request chặn hiển thị ~150 ms); 2 file chữ thường vẫn preload."""
    css = (ASSETS / "fonts/fonts.css").read_text(encoding="utf-8")
    css = re.sub(r'/\*.*?\*/\s*', '', css, flags=re.S)          # bỏ chú thích
    css = re.sub(r'\s*\n\s*', '', css).replace(': ', ':').replace(' {', '{')
    return ('<link rel="preload" href="/assets/fonts/bvp-400-latin.woff2" as="font" type="font/woff2" crossorigin>'
            '<link rel="preload" href="/assets/fonts/bvp-400-vietnamese.woff2" as="font" type="font/woff2" crossorigin>'
            f'<style data-tnh="fonts">{css}</style>\n')


IMG_CSS = "<style>:where(img){max-width:100%}:where(img[height]){height:auto}</style>\n"
ROBOTS = '<meta name="robots" content="max-image-preview:large">\n'
IMG_RE = re.compile(r'<img\b[^>]*>', re.I)
MAXW = 1600
VARIANTS = (480, 960)   # đợt 2: ảnh theo cỡ màn hình — điện thoại lấy 480, máy tính 960, màn to lấy bản gốc
SIZES = "(max-width:640px) 100vw, 50vw"


def srcset_for(src, size):
    """'/assets/x.webp' rộng ≥700 → chuỗi srcset với bản 480/960 (tạo nếu chưa có). Không đủ điều kiện → None."""
    m = re.fullmatch(r'/assets/([^"?#]+)\.webp', src)
    if not m or not size or size[0] < 700:
        return None
    base = m.group(1)
    f = ASSETS / f"{base}.webp"
    if not f.exists():
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    parts = []
    for w in VARIANTS:
        if w >= size[0]:
            continue
        out = ASSETS / f"{base}-{w}.webp"
        if not out.exists() or out.stat().st_mtime < f.stat().st_mtime:
            with Image.open(f) as im:
                im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)
        parts.append(f"/assets/{base}-{w}.webp {w}w")
    if not parts:
        return None
    parts.append(f"{src} {size[0]}w")
    return ", ".join(parts)


def webp_for(src):
    """'/assets/x.jpg' → ('/assets/x.webp', (w,h)) — tạo file webp nếu chưa có. Không có Pillow/ảnh → None."""
    m = re.fullmatch(r'/assets/([^"?#]+)\.(jpe?g|png)', src, re.I)
    if not m:
        return None
    srcf = ASSETS / f"{m.group(1)}.{m.group(2)}"
    out = ASSETS / f"{m.group(1)}.webp"
    if not srcf.exists():
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    if not out.exists() or out.stat().st_mtime < srcf.stat().st_mtime:
        im = Image.open(srcf)
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=80, method=6)
    with Image.open(out) as w:
        return f"/assets/{m.group(1)}.webp", w.size


def dims_of(src):
    m = re.fullmatch(r'/assets/([^"?#]+\.(?:webp|jpe?g|png))', src, re.I)
    if not m or not (ASSETS / m.group(1)).exists():
        return None
    try:
        from PIL import Image
        with Image.open(ASSETS / m.group(1)) as im:
            return im.size
    except Exception:
        return None


def fix_img(tag, first):
    src_m = re.search(r'\bsrc="([^"]+)"', tag)
    if not src_m:
        return tag
    if src_m.group(1).startswith("assets/"):  # trang gốc index.html dùng đường dẫn tương đối
        tag = tag.replace(f'src="{src_m.group(1)}"', f'src="/{src_m.group(1)}"')
    src = re.search(r'\bsrc="([^"]+)"', tag).group(1)
    size = None
    r = webp_for(src)
    if r:
        new, size = r
        tag = tag.replace(f'src="{src}"', f'src="{new}"')
    cur = re.search(r'\bsrc="([^"]+)"', tag).group(1)
    if not re.search(r'\bwidth=', tag) and not re.search(r'\bheight=', tag):
        size = size or dims_of(cur)
        if size:
            tag = tag.replace("<img", f'<img width="{size[0]}" height="{size[1]}"', 1)
    if "srcset=" not in tag and "logo" not in cur:
        wm = re.search(r'\bwidth="(\d+)"', tag)
        hm = re.search(r'\bheight="(\d+)"', tag)
        sz = size or ((int(wm.group(1)), int(hm.group(1))) if wm and hm else dims_of(cur))
        ss = srcset_for(cur, sz)
        if ss:
            tag = tag.replace("<img", f'<img srcset="{ss}" sizes="{SIZES}"', 1)
    if first:
        tag = re.sub(r'\s+loading="lazy"', "", tag)
        if "fetchpriority" not in tag:
            tag = tag.replace("<img", '<img fetchpriority="high"', 1)
    return tag


def toi_uu_html(html, img=True):
    if GF_RE.search(html):
        html = GF_RE.sub(lambda _: font_tags(), html, count=1)
        html = PRECONNECT_RE.sub("", html)
    elif FONT_LINK_RE.search(html):                       # trang đã qua đợt 1 → nhúng thẳng
        html = FONT_LINK_RE.sub(lambda _: font_tags().split("crossorigin>", 2)[-1].rstrip("\n"), html, count=1)
    else:                                                  # chạy lại: cập nhật khối font nhúng nếu fonts.css đổi
        html = FONT_STYLE_RE.sub(lambda _: font_tags().split("crossorigin>", 2)[-1].rstrip("\n"), html, count=1)
    noindex_forever = re.search(r'<meta name="robots" content="[^"]*noindex[^"]*"(?![^>]*data-tnh)', html)
    if not noindex_forever and "max-image-preview" not in html:
        html = re.sub(r'(<meta name="viewport"[^>]*>\n?)', lambda m: m.group(1) + ROBOTS, html, count=1)
    if img:
        body_at = html.find("<body")
        head, body = html[:body_at], html[body_at:]
        seen = {"first": False}

        def rep(m):
            tag = m.group(0)
            src = (re.search(r'\bsrc="([^"]+)"', tag) or [None, ""])[1]
            first = not seen["first"] and src.lstrip("/").startswith("assets/") and "logo" not in src
            if first:
                seen["first"] = True
            return fix_img(tag, first)
        body = IMG_RE.sub(rep, body)
        html = head + body
        if 'height="' in body and ":where(img[height])" not in html:
            html = html.replace("</head>", IMG_CSS + "</head>", 1)
    return html


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    files = [ROOT / a for a in args] if args else [p for p in ROOT.rglob("*.html")
                                                   if not {".git", "_scripts", "node_modules"} & set(p.parts)]
    changed = 0
    for p in sorted(files):
        s = p.read_text(encoding="utf-8")
        n = toi_uu_html(s)
        if n != s:
            changed += 1
            if not dry:
                p.write_text(n, encoding="utf-8")
    print(f"{'(thử) ' if dry else ''}{changed}/{len(files)} trang thay đổi")


if __name__ == "__main__":
    main()
