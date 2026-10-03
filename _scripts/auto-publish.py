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

Cổng duyệt bài (thêm 10/2026, app "Duyệt bài"): nếu bài có
<meta name="tnh-approved" content="pending"> (hoặc "false") thì dù đã tới hạn
vẫn KHÔNG đăng — chờ duyệt xong (app sửa content thành "true") mới đăng.
Bài không có thẻ này (bài cũ trước khi có app) coi như đã duyệt, đăng bình
thường — giữ tương thích ngược, không làm gãy pipeline cũ.

Thêm 02/10/2026 (SEO):
  - Bài có lịch đăng nhưng CHƯA lên mục lục → gắn NOINDEX_TAG (Google không lập chỉ mục bản nháp
    dù mở được bằng link để duyệt qua Telegram). Lúc đăng → gỡ thẻ, bài được index bình thường.
  - Mọi trang .html thiếu mã GA4 → tự gắn GTAG ngay sau <head> (bài mới không cần nhớ gắn tay).
"""
import re, sys, json, html as htmllib, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "cam-nang" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
TZ_VN = datetime.timezone(datetime.timedelta(hours=7))
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

GA_ID = "G-R4S6DMJPX3"  # GA4 property thenesthouse.com.vn (tạo 02/10/2026)
GTAG = (
    f'<!-- Google tag (gtag.js) -->\n'
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
    f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
    f"gtag('js',new Date());gtag('config','{GA_ID}');</script>\n"
)
NOINDEX_TAG = '<meta name="robots" content="noindex" data-tnh="cho-dang">\n'
# Đo lượt bấm Zalo / gọi điện / gian hàng sàn → sự kiện GA4, nhập sang Google Ads làm chuyển đổi (thêm 02/10/2026)
TRACK_FILE = ROOT / "_scripts" / "track-click.html"
TRACK = TRACK_FILE.read_text().strip() if TRACK_FILE.exists() else ""


def ensure_gtag():
    """Gắn GA4 + đoạn đo lượt bấm cho mọi trang thiếu. Trả về số trang vừa sửa."""
    n = 0
    for path in ROOT.rglob("*.html"):
        if any(part.startswith((".", "_")) for part in path.relative_to(ROOT).parts):
            continue
        html = orig = path.read_text()
        if GA_ID not in html and "<head>" in html:
            html = (html.replace("<head>\n", "<head>\n" + GTAG, 1) if "<head>\n" in html
                    else html.replace("<head>", "<head>\n" + GTAG, 1))
        if TRACK and "click_zalo" not in html and "</body>" in html:
            html = html.replace("</body>", TRACK + "\n</body>", 1)
        if html != orig:
            path.write_text(html)
            n += 1
    return n


def geo_fix_post(path, html):
    """Chuẩn GEO cho bài sắp đăng: dateModified (= ngày "Cập nhật dd/mm/yyyy" hiển thị) + og:site_name/og:locale + người kiểm duyệt."""
    new = html
    m = re.search(r"Cập nhật (\d{2})/(\d{2})/(\d{4})", new)
    if m and '"dateModified"' not in new:
        iso = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
        new = re.sub(r'("datePublished"\s*:\s*"[^"]+")', rf'\1, "dateModified": "{iso}"', new, count=1)
    # người kiểm duyệt (CEO chốt 02/10/2026): author = tổ chức, editor = Nguyễn Anh Tú
    new = new.replace("Cẩm nang yến sào · The Nest House · Cập nhật",
                      "Cẩm nang yến sào · Kiểm duyệt: <strong>Nguyễn Anh Tú</strong>, nhà sáng lập The Nest House · Cập nhật", 1)
    if '"editor"' not in new:
        new = new.replace('"author": {"@type": "Organization", "name": "The Nest House"}',
                          '"author": {"@type": "Organization", "name": "The Nest House", "@id": "https://thenesthouse.com.vn/#organization"}, '
                          '"editor": {"@type": "Person", "@id": "https://thenesthouse.com.vn/#nguyen-anh-tu", "name": "Nguyễn Anh Tú", '
                          '"jobTitle": "Nhà sáng lập", "worksFor": {"@id": "https://thenesthouse.com.vn/#organization"}}', 1)
    add = ""
    if 'property="og:site_name"' not in new:
        add += '<meta property="og:site_name" content="The Nest House">\n'
    if 'property="og:locale"' not in new:
        add += '<meta property="og:locale" content="vi_VN">\n'
    ogs = list(re.finditer(r'<meta property="og:[^>]*>\n?', new))
    if add and ogs:
        new = new[:ogs[-1].end()] + add + new[ogs[-1].end():]
    if new != html:
        path.write_text(new)
    return new


def sync_itemlist(index_html):
    """Dựng lại ItemList JSON-LD của /cam-nang/ từ các thẻ card (đúng thứ tự trên trang)."""
    items = [{"@type": "ListItem", "position": i + 1, "url": "https://thenesthouse.com.vn" + href,
              "name": htmllib.unescape(t)}
             for i, (href, t) in enumerate(re.findall(r'<a class="card" href="(/cam-nang/[^"]+)">.*?<h2>(.*?)</h2>',
                                                      index_html, re.S))]
    ld = ('<script type="application/ld+json">' + json.dumps(
        {"@context": "https://schema.org", "@type": "ItemList", "@id": "https://thenesthouse.com.vn/cam-nang/#danh-sach",
         "name": "Cẩm nang yến sào The Nest House", "itemListElement": items}, ensure_ascii=False) + "</script>")
    old = re.search(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "ItemList".*?</script>',
                    index_html, re.S)
    return index_html.replace(old.group(0), ld) if old else index_html.replace("</head>", ld + "\n</head>", 1)


def activate_planned_links(index_html):
    """Link nội bộ đặt sẵn tới bài CHƯA đăng: <li hidden data-tnh-cho="/cam-nang/x.html">Tên</li>
    → bật thành <li><a href=…>Tên</a></li> khi bài x đã lên mục lục. Trả về số link vừa bật."""
    n = 0
    pat = re.compile(r'<li hidden data-tnh-cho="(/cam-nang/[^"]+)">(.*?)</li>', re.S)
    for path in (ROOT / "cam-nang").glob("*.html"):
        html = path.read_text()
        if "data-tnh-cho" not in html:
            continue
        def rep(m):
            nonlocal n
            if f'href="{m.group(1)}"' in index_html:
                n += 1
                return f'<li><a href="{m.group(1)}">{m.group(2)}</a></li>'
            return m.group(0)
        new = pat.sub(rep, html)
        # khối "Đọc thêm" từng toàn link ẩn → hiện tiêu đề khi đã có ít nhất 1 link bật
        if "data-tnh-cho-khoi" in new:
            new = re.sub(r'<strong data-tnh-cho-khoi hidden>(Đọc thêm:</strong><ul>(?:(?!</ul>).)*?<li><a )',
                         r"<strong>\1", new, flags=re.S)
        if new != html:
            path.write_text(new)
    return n


def set_noindex(path, html, on):
    """Bật/tắt thẻ noindex chờ đăng. Chỉ đụng thẻ do script này gắn (data-tnh="cho-dang")."""
    has = 'data-tnh="cho-dang"' in html
    if on and not has:
        html = html.replace("</title>\n", "</title>\n" + NOINDEX_TAG, 1) if "</title>\n" in html \
            else html.replace("</head>", NOINDEX_TAG + "</head>", 1)
    elif not on and has:
        html = re.sub(r'<meta name="robots" content="noindex" data-tnh="cho-dang">\n?', "", html)
    else:
        return html
    path.write_text(html)
    return html


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
        if f'href="/cam-nang/{path.name}"' in index_html:
            set_noindex(path, html, False)  # đã lên mục lục → chắc chắn được index
            continue
        if pub > today:
            set_noindex(path, html, True)
            print(f"   {path.name}: hẹn {pub} — chưa tới hạn")
            continue
        approved = meta(html, "tnh-approved")
        if approved in ("pending", "false"):
            set_noindex(path, html, True)
            print(f"   {path.name}: tới hạn nhưng CHƯA DUYỆT — chờ duyệt trong app")
            continue
        html = set_noindex(path, html, False)  # tới hạn + đã duyệt → gỡ noindex rồi đăng
        html = geo_fix_post(path, html)

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
        # chèn sau thẻ card cuối cùng trong lưới — CHỈ tìm trong vùng trước <footer>,
        # vì footer cũng chứa thẻ <a> (rfind toàn file từng chèn nhầm card vào trong footer)
        pos_footer = index_html.find("<footer")
        if pos_footer == -1:
            print("!! Không tìm thấy <footer> để giới hạn vùng chèn", file=sys.stderr)
            sys.exit(1)
        last = index_html.rfind("</a>", 0, pos_footer)
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
        INDEX.write_text(sync_itemlist(index_html))
        SITEMAP.write_text(sitemap)
    k = activate_planned_links(INDEX.read_text())
    if k:
        print(f"✓ Bật {k} link nội bộ đặt sẵn")
    n = ensure_gtag()
    if n:
        print(f"✓ Gắn GA4 cho {n} trang")
    print("PUBLISHED=" + ",".join(published))


if __name__ == "__main__":
    main()
