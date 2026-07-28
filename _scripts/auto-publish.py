#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự công bố bài cẩm nang tới hạn — chạy bởi GitHub Actions mỗi sáng 8:30 giờ VN.

Cách hoạt động:
  1. Quét cam-nang/*.html tìm thẻ <meta name="tnh-publish" content="YYYY-MM-DD">
  2. Bài nào tới hạn (ngày <= hôm nay, giờ VN) mà CHƯA có trong cam-nang/index.html
     → thêm thẻ card vào mục lục + thêm URL vào sitemap.xml
  3. In ra danh sách bài đã đăng (workflow dùng để đặt tên commit)

Không đụng gì tới bài chưa tới hạn — cứ để sẵn trong repo, đúng ngày mới lên mục lục.
"""
import re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "cam-nang" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
TZ_VN = datetime.timezone(datetime.timedelta(hours=7))
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def meta(html, name):
    m = re.search(r'<meta\s+name="%s"\s+content="([^"]*)"' % re.escape(name), html)
    return m.group(1) if m else None


def first_text(html, pattern):
    m = re.search(pattern, html, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else None


def main():
    today = datetime.datetime.now(TZ_VN).date()
    index_html = INDEX.read_text()
    sitemap = SITEMAP.read_text()
    published = []

    for path in sorted((ROOT / "cam-nang").glob("*.html")):
        if path.name == "index.html":
            continue
        html = path.read_text()
        raw_date = meta(html, "tnh-publish")
        if not raw_date:
            continue  # bài cũ chưa gắn lịch — bỏ qua, không tự đụng vào
        try:
            pub = datetime.date.fromisoformat(raw_date)
        except ValueError:
            print(f"!! {path.name}: ngày '{raw_date}' sai định dạng, bỏ qua", file=sys.stderr)
            continue
        if pub > today:
            print(f"   {path.name}: hẹn {pub} — chưa tới hạn")
            continue
        if f'href="/cam-nang/{path.name}"' in index_html:
            continue  # đã lên mục lục rồi

        title = first_text(html, r"<h1[^>]*>(.*?)</h1>") or path.stem
        desc = meta(html, "tnh-card-desc") or (meta(html, "description") or "")[:150]
        img = re.search(r'<img src="(/assets/[^"]+)"', html)
        img = img.group(1) if img else "/assets/100G-soi-dai.jpg"
        ngay = f"{THU[pub.weekday()]}, {pub.strftime('%d/%m/%Y')}"

        card = (
            f'<a class="card" href="/cam-nang/{path.name}">\n'
            f'      <img src="{img}" alt="{title}" loading="lazy">\n'
            f'      <div class="body">\n'
            f'        <h2>{title}</h2>\n'
            f'        <p>{desc}</p>\n'
            f'        <span class="date">{ngay}</span>\n'
            f'      </div>\n'
            f'    </a>'
        )
        # chèn sau thẻ card cuối cùng trong lưới
        last = index_html.rfind("</a>")
        if last == -1:
            print(f"!! Không tìm thấy chỗ chèn card trong index.html", file=sys.stderr)
            sys.exit(1)
        cut = last + len("</a>")
        index_html = index_html[:cut] + "\n    " + card + index_html[cut:]

        loc = f"https://thenesthouse.com.vn/cam-nang/{path.name}"
        if loc not in sitemap:
            sitemap = sitemap.replace(
                "</urlset>",
                f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>0.7</priority></url>\n</urlset>",
            )
        published.append(path.name)
        print(f"✓ ĐĂNG: {path.name} — {title}")

    if published:
        INDEX.write_text(index_html)
        SITEMAP.write_text(sitemap)
    print("PUBLISHED=" + ",".join(published))


if __name__ == "__main__":
    main()
