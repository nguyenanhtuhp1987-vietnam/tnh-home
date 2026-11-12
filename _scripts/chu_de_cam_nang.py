#!/usr/bin/env python3
"""Dựng MẪU chủ đề cho /cam-nang/ (CEO chốt 3 chủ đề 12/11/2026): ô chủ đề trên /cam-nang/ + trang chủ đề «Yến cho người thương».

Chạy trên một nhánh riêng của tnh-home (KHÔNG push main):
  python3 chu_de_cam_nang.py <thư-mục-tnh-home> [--bang]   # --bang: chỉ in bảng 79 bài → chủ đề/nhãn
Chỉ đọc mục lục hiện có (cam-nang/index.html) để lấy ảnh · tiêu đề · mô tả; không sửa bài nào.
"""
import html
import re
import sys
from pathlib import Path

CHU_DE = {
    "chung-yen": ("Chưng yến tại nhà", "Công thức, mẹo hay và nguyên liệu chưng cùng"),
    "hieu-dung-ve-yen": ("Hiểu đúng về yến", "Tác dụng, chọn loại, mua và bảo quản yến sào"),
    "yen-cho-nguoi-thuong": ("Yến cho người thương", "Cho bé, bố mẹ, bà bầu… và quà biếu theo dịp"),
}

# slug → (chủ đề, nhãn)
MAP = {}
def gan(cd, nhan, slugs):
    for s in slugs.split():
        assert s not in MAP, s
        MAP[s] = (cd, nhan)

gan("chung-yen", "Công thức", "cach-chung-yen-sao yen-chung-duong-phen cach-chung-yen-tao-do-ky-tu cac-mon-yen-chung cach-chung-yen-hat-sen cach-chung-yen-hat-chia cach-che-bien-yen-sao cach-chung-1-tai-yen chung-yen-voi-duong-gi chung-yen-voi-mat-ong yen-sao-va-dong-trung-ha-thao 1-lang-yen-chung-duoc-bao-nhieu-lan")
gan("chung-yen", "Mẹo & lỗi", "loi-sai-khi-chung-yen chung-yen-bao-lau chung-yen-bi-tan yen-chung-bi-hu chung-yen-co-day-nap-khong cach-giam-mui-tanh-yen-sao yen-chung-tuoi-de-duoc-bao-lau yen-tuoi-la-gi")
gan("chung-yen", "Sơ chế & dụng cụ", "cach-ngam-yen-kho-truoc-khi-chung cach-so-che-yen-tho noi-chung-yen hu-chung-yen chung-yen-bang-noi-nau-cham")
gan("chung-yen", "Cho bé", "cach-chung-yen-cho-be")

gan("hieu-dung-ve-yen", "Các loại yến", "to-yen-tho yen-sao-la-gi yen-tinh-che-la-gi chan-yen-yen-vun-la-gi cac-loai-yen-sao-nen-chon-loai-nao yen-tuoi-yen-tinh-che-yen-chung-san nuoc-yen-sao yen-sao-cao-cap cach-chon-size-yen-sao-phu-hop yen-chung-san-loai-nao-tot so-sanh-yen-chung-san-va-tu-chung")
gan("hieu-dung-ve-yen", "Tác dụng & liều dùng", "tac-dung-cua-yen-sao cach-su-dung-yen-sao thoi-diem-an-yen-sao-tot-nhat nhung-ai-can-luu-y-khi-an-yen-sao loi-ich-an-yen-sao-lau-dai tac-hai-cua-yen-sao gia-tri-dinh-duong-to-yen to-yen-co-tot-khong cach-dung-yen-chung-san")
gan("hieu-dung-ve-yen", "Thật – giả", "phan-biet-yen-sao-that-gia to-yen-gia-lam-tu-gi")
gan("hieu-dung-ve-yen", "Mua & tin cậy", "gia-yen-sao mua-yen-sao-o-dau-uy-tin mua-yen-sao-dip-11-11-o-dau yen-sao-khanh-hoa yen-sao-the-nest-house the-nest-house-co-uy-tin-khong-7-dieu-kiem-duoc")
gan("hieu-dung-ve-yen", "Bảo quản & đổi trả", "cach-bao-quan-yen-sao yen-sao-co-han-dung-bao-lau nhan-hang-thay-to-yen-vo-rung-soi-co-doi-duoc-khong")

gan("yen-cho-nguoi-thuong", "Bé & mẹ", "yen-sao-cho-be yen-sao-cho-ba-bau yen-sao-cho-phu-nu-sau-sinh")
gan("yen-cho-nguoi-thuong", "Người lớn tuổi & ốm dậy", "yen-sao-cho-nguoi-cao-tuoi yen-sao-cho-nguoi-moi-om-day yen-sao-cho-nguoi-suc-de-khang-kem yen-sao-cho-nguoi-tieu-duong")
gan("yen-cho-nguoi-thuong", "Đi làm & tập luyện", "yen-sao-cho-dan-van-phong yen-sao-cho-nguoi-tap-gym yen-sao-mua-thi-cho-si-tu yen-sao-cho-nam-gioi yen-sao-va-lan-da yen-sao-va-can-nang yen-sao-va-giac-ngu")
gan("yen-cho-nguoi-thuong", "Quà Tết & doanh nghiệp", "qua-tet-yen-sao qua-bieu-doi-tac-yen-sao qua-bieu-sep-dip-tet-duoi-1-trieu set-qua-tang-suc-khoe")
gan("yen-cho-nguoi-thuong", "Quà theo dịp", "qua-20-10-yen-sao qua-20-11-tang-thay-co-lon-tuoi qua-tan-gia-yen-sao-sang-khong-pho-truong banh-trung-thu-yen-sao")

NHAN_THU_TU = {
    "chung-yen": ["Công thức", "Mẹo & lỗi", "Sơ chế & dụng cụ", "Nguyên liệu & dinh dưỡng", "Cho bé"],
    "hieu-dung-ve-yen": ["Các loại yến", "Tác dụng & liều dùng", "Thật – giả", "Mua & tin cậy", "Bảo quản & đổi trả"],
    "yen-cho-nguoi-thuong": ["Bé & mẹ", "Người lớn tuổi & ốm dậy", "Đi làm & tập luyện", "Quà Tết & doanh nghiệp", "Quà theo dịp"],
}
NEN_DOC = {
    "chung-yen": ["cach-chung-yen-sao", "loi-sai-khi-chung-yen", "cach-chung-yen-tao-do-ky-tu", "cach-ngam-yen-kho-truoc-khi-chung"],
    "hieu-dung-ve-yen": ["cac-loai-yen-sao-nen-chon-loai-nao", "phan-biet-yen-sao-that-gia", "tac-dung-cua-yen-sao", "cach-bao-quan-yen-sao"],
    "yen-cho-nguoi-thuong": ["yen-sao-cho-be", "qua-tet-yen-sao", "yen-sao-cho-nguoi-cao-tuoi", "qua-bieu-doi-tac-yen-sao"],
}
META = {
    "chung-yen": ("Chưng yến tại nhà: công thức, mẹo và lỗi hay gặp | The Nest House",
                  "Công thức chưng yến đường phèn, táo đỏ, hạt sen, hạt chia; mẹo giảm tanh, lỗi hay gặp, cách ngâm tổ yến và chọn nồi, hũ chưng.",
                  "Chưng yến không khó, chỉ cần đúng bước. Các bài dưới đây xếp theo việc anh/chị đang làm: <b>công thức</b>, <b>mẹo và lỗi hay gặp</b>, <b>sơ chế và dụng cụ</b>, kèm cách chưng cho bé."),
    "hieu-dung-ve-yen": ("Hiểu đúng về yến sào: loại yến, tác dụng, mua và bảo quản | The Nest House",
                         "Phân biệt yến thô, tinh chế, rút lông; tác dụng và liều dùng; cách mua, nhận biết thật giả, đọc hạn dùng và bảo quản yến sào.",
                         "Trước khi mua và dùng yến, anh/chị nên biết rõ mình đang cầm loại nào. Các bài dưới đây giải thích <b>các loại yến</b>, <b>tác dụng và liều dùng</b>, cách <b>mua và kiểm hàng</b>, <b>bảo quản</b> — nói đúng, có giới hạn."),
    "yen-cho-nguoi-thuong": ("Yến sào cho người thân và quà biếu theo dịp | The Nest House",
                             "Bài viết về yến sào cho bé, bà bầu, sau sinh, bố mẹ lớn tuổi, người đi làm và quà biếu theo dịp. Chọn theo người dùng, kèm sản phẩm phù hợp.",
                             "Mỗi người trong nhà cần một cách dùng khác nhau: bé tập ăn, mẹ sau sinh, bố mẹ lớn tuổi, người đi làm bận rộn. Các bài dưới đây xếp theo <b>người dùng</b>, thêm phần quà biếu theo dịp để anh/chị chọn nhanh."),
}
SAN_PHAM = {
    "chung-yen": [
        ("Yến tinh chế sợi ngắn", "Dùng đều, chưng cho cả nhà, ngâm nhanh", "/yen-sao/tinh-che/soi-ngan/"),
        ("Yến tinh chế sợi dài", "Sợi nở đẹp, rõ miếng, hợp chưng đãi khách", "/yen-sao/tinh-che/soi-dai/"),
    ],
    "hieu-dung-ve-yen": [
        ("Tất cả sản phẩm", "Yến thô, tinh chế, rút lông, yến chưng sẵn, set quà", "/yen-sao/"),
        ("Yến tinh chế sợi dài", "Loại được hỏi nhiều nhất, có tem chống hàng giả", "/yen-sao/tinh-che/soi-dai/"),
    ],
    "yen-cho-nguoi-thuong": [
        ("Set quà biếu", "Hộp quà sẵn, có túi, hợp biếu bố mẹ, sếp, đối tác", "/yen-sao/set-qua-bieu/"),
        ("Yến chưng sẵn 70ml", "Mở nắp dùng ngay, tiện cho bé, người lớn tuổi, người bận", "/yen-sao/yen-chung/yen-chung-30/"),
    ],
}


def doc_the(idx):
    out = {}
    for m in re.finditer(r'<a class="card" href="/cam-nang/([^"]+)\.html">(.*?)</a>', idx, re.S):
        slug, body = m.group(1), m.group(2)
        img = re.search(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', body)
        h2 = re.search(r"<h2>(.*?)</h2>", body, re.S)
        p = re.search(r"<p>(.*?)</p>", body, re.S)
        d = re.search(r'<span class="date">(.*?)</span>', body)
        out[slug] = dict(img=img.group(1) if img else "", alt=img.group(2) if img else "", h2=h2.group(1) if h2 else slug,
                         p=p.group(1) if p else "", date=d.group(1) if d else "")
    return out


def them_bai_moi(repo, cards):
    """Bài ngoài bảng MAP: đọc thẻ <meta name="tnh-chu-de" content="chu-de|Nhãn"> trong chính bài (web-seo gắn khi viết)."""
    for slug in cards:
        if slug in MAP:
            continue
        f = repo / "cam-nang" / f"{slug}.html"
        m = re.search(r'<meta name="tnh-chu-de" content="([^"|]+)\|([^"]+)">', f.read_text(encoding="utf-8")) if f.exists() else None
        if not m:
            continue
        cd, nhan = m.group(1).strip(), m.group(2).strip()
        if cd in CHU_DE and nhan in NHAN_THU_TU.get(cd, []):
            MAP[slug] = (cd, nhan)
        else:
            print(f"!! {slug}: tnh-chu-de «{cd}|{nhan}» không hợp lệ", file=sys.stderr)


def the_html(slug, c, nhan):
    return (f'<a class="card" href="/cam-nang/{slug}.html" data-nhan="{html.escape(nhan)}">\n'
            f'      <img src="{c["img"]}" alt="{c["alt"]}" loading="lazy">\n      <div class="body">\n'
            f'        <span class="cd-tag">{html.escape(nhan)}</span>\n        <h2>{c["h2"]}</h2>\n        <p>{c["p"]}</p>\n'
            f'        <span class="date">{c["date"]}</span>\n      </div>\n    </a>')


CSS = """
.cd-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:34px 0 6px}
@media(max-width:760px){.cd-tiles{grid-template-columns:1fr}}
.cd-tile{display:block;border:1px solid #e8e0cc;border-radius:16px;padding:22px 22px 18px;background:linear-gradient(170deg,#fffdf6,#fff);transition:.25s}
.cd-tile:hover{box-shadow:0 14px 34px rgba(14,59,51,.14);transform:translateY(-3px);border-color:var(--gold)}
.cd-tile b{display:block;font-family:var(--serif);font-size:1.25rem;line-height:1.3;margin-bottom:6px}
.cd-tile span{display:block;font-size:.88rem;color:#4a5f59}
.cd-tile em{display:block;margin-top:12px;font-style:normal;font-size:.82rem;color:var(--gold-text);font-weight:600}
.cd-h2{font-family:var(--serif);font-size:1.3rem;padding:26px 0 0}
.cd-tag{font-size:.72rem;font-weight:600;color:var(--gold-text);letter-spacing:.02em}
.crumb{font-size:.82rem;color:#6b7a75;padding:16px 0 0}.crumb a{color:var(--gold-text)}
.cd-chips{display:flex;flex-wrap:wrap;gap:10px;padding:26px 0 4px}
.cd-chip{border:1px solid var(--gold);background:#fff;color:var(--forest);border-radius:999px;padding:8px 16px;font:600 .85rem var(--sans);cursor:pointer}
.cd-chip.on{background:var(--forest);border-color:var(--forest);color:#fff}
.cd-intro{max-width:760px;margin:0 auto;padding:6px 0;color:#2f4a43}
.cd-pick{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;padding:12px 0 0}
@media(max-width:700px){.cd-pick{grid-template-columns:1fr}}
.cd-pick a{display:block;border-left:3px solid var(--gold);background:var(--cream);border-radius:10px;padding:12px 16px;font-size:.92rem;font-weight:600}
.cd-sp{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:30px 0 10px}
@media(max-width:700px){.cd-sp{grid-template-columns:1fr}}
.cd-sp a{display:block;border:1px solid var(--gold);border-radius:14px;padding:18px 20px;background:#fff}
.cd-sp b{display:block;font-family:var(--serif);font-size:1.05rem;margin-bottom:4px}
.cd-sp span{font-size:.86rem;color:#4a5f59}
.cd-cta{text-align:center;padding:18px 0 40px}
"""


def trang_chu_de(base, cd, cards):
    ten, phu = CHU_DE[cd]
    bai = [(s, MAP[s][1]) for s in cards if s in MAP and MAP[s][0] == cd]
    thu_tu = NHAN_THU_TU[cd]
    bai.sort(key=lambda x: thu_tu.index(x[1]))
    co = [n for n in thu_tu if any(x == n for _, x in bai)]  # chỉ hiện nhãn đã có bài
    chips = '<button class="cd-chip on" data-nhan="">Tất cả (%d)</button>' % len(bai) + "".join(
        f'<button class="cd-chip" data-nhan="{html.escape(n)}">{html.escape(n)} ({sum(1 for _, x in bai if x == n)})</button>' for n in co)
    the = "\n    ".join(the_html(s, cards[s], n) for s, n in bai)
    pick = "".join(f'<a href="/cam-nang/{s}.html">{cards[s]["h2"]}</a>' for s in NEN_DOC[cd])
    sp = "".join(f'<a href="{u}"><b>{t}</b><span>{d}</span></a>' for t, d, u in SAN_PHAM[cd])
    url = f"https://thenesthouse.com.vn/cam-nang/{cd}/"
    tieu_de, mo_ta, gioi_thieu = META[cd]
    ld = ('{"@context":"https://schema.org","@type":"CollectionPage","name":"%s","url":"%s","description":"%s","isPartOf":{"@id":"https://thenesthouse.com.vn/cam-nang/"}}' % (ten, url, mo_ta))
    bc = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Trang chủ","item":"https://thenesthouse.com.vn/"},'
          '{"@type":"ListItem","position":2,"name":"Cẩm nang","item":"https://thenesthouse.com.vn/cam-nang/"},{"@type":"ListItem","position":3,"name":"%s","item":"%s"}]}' % (ten, url))
    head = base["head"] if CSS.strip() in base["head"] else base["head"].replace("</style>", CSS + "</style>", 1)
    head = re.sub(r"<title>.*?</title>", f"<title>{tieu_de}</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{mo_ta}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", head, flags=re.S)
    head = head.replace("</head>", f'<script type="application/ld+json">{ld}</script>\n<script type="application/ld+json">{bc}</script>\n</head>', 1)
    js = """<script>
(function(){var b=document.querySelectorAll('.cd-chip'),c=document.querySelectorAll('#cdList .card');
b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.classList.remove('on')});x.classList.add('on');
var n=x.getAttribute('data-nhan');c.forEach(function(k){k.style.display=(!n||k.getAttribute('data-nhan')===n)?'':'none'})})})})();
</script>"""
    return f"""{head}<body>
{base["topbar"]}
<div class="head">
  <h1>{ten}</h1>
  <p>{phu}.</p>
</div>
<div class="container">
  <nav class="crumb"><a href="/">Trang chủ</a> › <a href="/cam-nang/">Cẩm nang</a> › {ten}</nav>
  <p class="cd-intro" style="padding-top:18px">{gioi_thieu}</p>
  <h2 class="cd-h2">Nên đọc trước</h2>
  <div class="cd-pick">{pick}</div>
  <div class="cd-chips">{chips}</div>
  <div class="grid" id="cdList">
    {the}
  </div>
  <h2 class="cd-h2">Sản phẩm hợp với chủ đề này</h2>
  <div class="cd-sp">{sp}</div>
  <div class="cd-cta"><a class="btn btn-gold" href="https://zalo.me/0969850153" target="_blank" rel="noopener">💬 Nhắn Zalo để được tư vấn</a></div>
</div>
{base["footer"]}
{js}
</body>
</html>
"""


REL_CSS = ('<style>.cd-rel{max-width:760px;margin:34px auto 10px;padding:0 20px;font-family:var(--sans)}'
           '.cd-rel h2{font-family:var(--serif);font-size:1.2rem;margin-bottom:10px}'
           '.cd-rel a.i{display:block;border-left:3px solid var(--gold);background:var(--cream);border-radius:10px;padding:11px 16px;margin:8px 0;font-size:.92rem;font-weight:600}'
           '.cd-rel a.all{display:inline-block;margin-top:6px;font-size:.88rem;color:var(--gold-text);font-weight:600}</style>')


def ap_dung_bai(repo, cards):
    """Đường dẫn Chủ đề + khối «Cùng chủ đề» vào 79 bài đang lên mục lục. Chạy lại an toàn (xoá khối cũ rồi dựng lại)."""
    dem = 0
    for slug, (cd, nhan) in MAP.items():
        p = repo / "cam-nang" / f"{slug}.html"
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        ten = CHU_DE[cd][0]
        s = re.sub(r"<!--CD-BEGIN-->.*?<!--CD-END-->\n?", "", s, flags=re.S)
        s = s.replace(f'<a href="/cam-nang/{cd}/">{ten}</a> › ', "")
        s = s.replace('<a href="/cam-nang/">Cẩm nang</a> › ', f'<a href="/cam-nang/">Cẩm nang</a> › <a href="/cam-nang/{cd}/">{ten}</a> › ', 1)
        if '"position": 4' not in s and '"position": 3,' in s:
            s = s.replace('{"@type": "ListItem", "position": 3,',
                          f'{{"@type": "ListItem", "position": 3, "name": "{ten}", "item": "https://thenesthouse.com.vn/cam-nang/{cd}/"}},{{"@type": "ListItem", "position": 4,', 1)
        cung = [x for x, v in MAP.items() if v[0] == cd and x != slug]
        cung.sort(key=lambda x: (MAP[x][1] != nhan,))
        gan = "".join(f'<a class="i" href="/cam-nang/{x}.html">{cards[x]["h2"]}</a>' for x in cung[:3])
        khoi = (f'<!--CD-BEGIN-->\n{REL_CSS}<section class="cd-rel"><h2>Cùng chủ đề: {ten}</h2>{gan}'
                f'<a class="all" href="/cam-nang/{cd}/">Xem tất cả bài về «{ten}» ›</a></section>\n<!--CD-END-->\n')
        if "</article>\n" in s:
            s = s.replace("</article>\n", "</article>\n" + khoi, 1)
        else:
            s = s.replace("<footer>", khoi + "<footer>", 1)
        p.write_text(s, encoding="utf-8")
        dem += 1
    print("đã gắn chủ đề vào", dem, "bài")


def main():
    repo = Path(sys.argv[1])
    idx_p = repo / "cam-nang" / "index.html"
    idx = idx_p.read_text(encoding="utf-8")
    cards = doc_the(idx)
    them_bai_moi(repo, cards)
    thieu = [s for s in cards if s not in MAP]
    if thieu:
        print("chưa có chủ đề (chỉ hiện ở «Tất cả bài viết»):", ", ".join(thieu), file=sys.stderr)
    for s_ in [s_ for s_ in MAP if s_ not in cards]:  # bài chưa lên mục lục → chưa tính
        del MAP[s_]
    if "--bang" in sys.argv:
        for cd in CHU_DE:
            print(f"\n## {CHU_DE[cd][0]} ({sum(1 for v in MAP.values() if v[0]==cd)} bài)")
            for s, (c, n) in MAP.items():
                if c == cd:
                    print(f"- {n} | {cards[s]['h2']} | /cam-nang/{s}.html")
        return
    # 1) ô chủ đề trên /cam-nang/
    dem = {cd: sum(1 for v in MAP.values() if v[0] == cd) for cd in CHU_DE}
    ties = "".join(f'<a class="cd-tile" href="/cam-nang/{cd}/"><b>{CHU_DE[cd][0]}</b><span>{CHU_DE[cd][1]}</span><em>{dem[cd]} bài · Xem chủ đề ›</em></a>' for cd in CHU_DE)
    khoi = ('<!--CHU-DE-BEGIN-->\n<div class="container"><div class="cd-tiles">' + ties + '</div>\n<h2 class="cd-h2">Tất cả bài viết</h2></div>\n<!--CHU-DE-END-->\n')
    s = idx
    s = re.sub(r"<!--CHU-DE-BEGIN-->.*?<!--CHU-DE-END-->\n", "", s, flags=re.S)
    if CSS.strip() not in s:
        s = s.replace("footer a{color:var(--gold-light)}\n</style>", "footer a{color:var(--gold-light)}\n" + CSS + "</style>", 1)
    s = s.replace('<div class="container">\n  <div class="grid" id="cnGrid">', khoi + '<div class="container">\n  <div class="grid" id="cnGrid">', 1)
    idx_p.write_text(s, encoding="utf-8")
    # 2) trang chủ đề mẫu
    head = idx[: idx.index("<body>")]
    topbar = idx[idx.index('<header class="topbar">'): idx.index("</header>") + len("</header>")]
    footer = idx[idx.index("<footer>"): idx.index("</footer>") + len("</footer>")]
    for cd in CHU_DE:
        out = repo / "cam-nang" / cd / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(trang_chu_de(dict(head=head, topbar=topbar, footer=footer), cd, cards), encoding="utf-8")
        print("ok", out)
    if "--bai" in sys.argv:
        ap_dung_bai(repo, cards)


if __name__ == "__main__":
    main()
