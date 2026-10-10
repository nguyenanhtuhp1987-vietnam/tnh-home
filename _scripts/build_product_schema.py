#!/usr/bin/env python3
"""Sinh lại JSON-LD "Product" (+ khối đánh giá hiển thị) cho 12 trang sản phẩm của thenesthouse.com.vn (CEO 10/10/2026).

Chạy:  python3 _scripts/build_product_schema.py          # ghi vào các trang
       python3 _scripts/build_product_schema.py --check  # chỉ kiểm, không ghi (thoát mã 1 nếu có lỗi)

Nguồn: giá từng quy cách = assets/tnh-cart.js (bảng P) để khớp giá hiển thị · đánh giá = data/reviews.json (chỉ đánh giá THẬT của khách đặt trực tiếp, đã đồng ý).
Luật Google: KHÔNG lấy điểm/đánh giá Shopee·Lazada·TikTok Shop vào schema; trang chưa có đánh giá thì KHÔNG xuất review/aggregateRating.
"""
import json, re, sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://thenesthouse.com.vn"
VALID_UNTIL = "2026-12-31"
FREESHIP_FROM = 1000000
PAGES = {  # product_id → đường dẫn trang
    "soi-dai": "/yen-sao/tinh-che/soi-dai/", "soi-ngan": "/yen-sao/tinh-che/soi-ngan/", "rut-long": "/yen-sao/tinh-che/rut-long/",
    "chan-yen": "/yen-sao/tinh-che/chan-yen/", "yen-vun": "/yen-sao/tinh-che/yen-vun/", "yen-tho": "/yen-sao/yen-tho/",
    "yen-chung-100": "/yen-sao/yen-chung/yen-chung-100/", "yen-chung-30": "/yen-sao/yen-chung/yen-chung-30/",
    "tam-giao": "/yen-sao/set-qua-bieu/tam-giao/", "tu-quy": "/yen-sao/set-qua-bieu/tu-quy/",
    "sac-xuan-30g": "/yen-sao/set-qua-bieu/sac-xuan-30g/", "hop-1-to": "/yen-sao/set-qua-bieu/hop-1-to/",
}
# Quy cách có trong bảng giá trên trang nhưng KHÔNG nằm trong giỏ hàng (mua qua Zalo): (sku, tên, giá)
EXTRA = {
    "yen-vun": [("YV3G", "Yến vụn — set 3g (1 lần chưng)", 90000), ("YV50G", "Yến vụn — 50g + hộp + nguyên liệu", 1300000), ("YV100G", "Yến vụn — 100g + hộp + nguyên liệu", 2500000)],
    "yen-chung-30": [("YC1", "Yến chưng 30% — 1 hũ lẻ 70ml", 25000), ("YC20", "Yến chưng 30% — 20 hũ", 450000), ("YC40", "Yến chưng 30% — 40 hũ", 900000)],
}
BAD = ["chữa", "khỏi bệnh", "đặc trị", "điều trị", "trị bệnh", "ung thư", "tiểu đường", "huyết áp"]  # đánh giá chứa từ này → cảnh báo, không đưa lên
SELLER = {"@type": "Organization", "name": "Công ty TNHH The Nest House Việt Nam"}


def load_cart():
    src = (ROOT / "assets/tnh-cart.js").read_text(encoding="utf-8")
    byp = {}
    for i, pg, name, qc, price, img in re.findall(r'(\w+): \["(/[^"]+)", "([^"]+)", [^,]+, "([^"]+)", (\d+), "([^"]+)"\]', src):
        byp.setdefault(pg, []).append({"id": i, "name": name, "price": int(price)})
    return byp


def ship_free():
    return {"@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "VND"},
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "VN"},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                             "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                             "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 5, "unitCode": "DAY"}}}


def return_policy(pid):
    days = 1 if "/yen-chung/" in PAGES[pid] else 90  # yến chưng sẵn: chỉ đổi khi lỗi/vỡ/hỏng, báo trong 24 giờ (chính sách đổi trả)
    return {"@type": "MerchantReturnPolicy", "applicableCountry": "VN",
            "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow", "merchantReturnDays": days,
            "returnMethod": "https://schema.org/ReturnByMail", "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
            "merchantReturnLink": SITE + "/chinh-sach/doi-tra/"}


def offer(pid, sku, name, price, url):
    o = {"@type": "Offer", "name": name, "sku": sku, "url": url, "price": str(price), "priceCurrency": "VND",
         "priceValidUntil": VALID_UNTIL, "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
         "seller": SELLER, "hasMerchantReturnPolicy": return_policy(pid)}
    if price >= FREESHIP_FROM:
        o["shippingDetails"] = ship_free()
    return o


def reviews_for(data, pid, problems):
    out = []
    for r in data.get("reviews", []):
        where = "đánh giá của '%s'" % r.get("name", "?")
        if r.get("product_id") != pid: continue
        if r.get("consent") is not True: problems.append(where + ": thiếu consent=true (khách chưa đồng ý) — bỏ qua"); continue
        if not isinstance(r.get("rating"), int) or not 1 <= r["rating"] <= 5: problems.append(where + ": rating phải là số nguyên 1–5"); continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(r.get("date", ""))): problems.append(where + ": date phải dạng YYYY-MM-DD"); continue
        if len(str(r.get("text", "")).strip()) < 10 or not str(r.get("name", "")).strip(): problems.append(where + ": thiếu tên hoặc nội dung"); continue
        if any(b in r["text"].lower() for b in BAD): problems.append(where + ": nội dung có từ về chữa bệnh — bỏ qua (luật 'yến không phải thuốc')"); continue
        out.append(r)
    return sorted(out, key=lambda r: r["date"], reverse=True)


def review_block(revs):
    n = len(revs); avg = sum(r["rating"] for r in revs) / n
    star = lambda k: "★" * k + "☆" * (5 - k)
    css = ("<style>.tnhrv{background:#faf7ee;border:1px solid #e8e0cc;border-radius:16px;padding:20px;margin:26px 0;color:#0E3B33}.tnhrv h2{margin:0 0 6px!important}"
           ".tnhrv .sum{font-size:.95rem;margin-bottom:10px}.tnhrv .st{color:#C1A374;letter-spacing:2px}.tnhrv .c{background:#fff;border:1px solid #e8e0cc;border-radius:12px;padding:12px 14px;margin:10px 0}"
           ".tnhrv .c b{font-size:.95rem}.tnhrv .c small{color:#5b6b66}.tnhrv .c p{margin:6px 0 0;font-size:.95rem}</style>")
    cards = "".join('<div class="c"><b>%s</b> <span class="st" aria-label="%d sao">%s</span> <small>· %s</small><p>%s</p></div>' % (
        escape(r["name"]), r["rating"], star(r["rating"]), "%s/%s/%s" % (r["date"][8:], r["date"][5:7], r["date"][:4]), escape(r["text"])) for r in revs)
    return ('<!--tnh-reviews-->\n' + css + '<div class="tnhrv" id="danh-gia-khach"><h2>Đánh giá của khách đặt trực tiếp</h2>'
            '<div class="sum"><span class="st">%s</span> <strong>%s/5</strong> · %d đánh giá thật của khách đặt tại The Nest House</div>%s</div>\n<!--/tnh-reviews-->\n') % (
        star(round(avg)), ("%.1f" % avg).replace(".", ","), n, cards)


def build_product(old, pid, cart, revs):
    url = SITE + PAGES[pid]
    items = []
    for c in cart.get(PAGES[pid], []):
        items.append(offer(pid, c["id"].upper(), c["name"], c["price"], url + "?qc=" + c["id"]))
    for sku, name, price in EXTRA.get(pid, []):
        items.append(offer(pid, sku, name, price, url))
    prices = [int(o["price"]) for o in items]
    img = old.get("image", "")
    p = {"@context": "https://schema.org", "@type": "Product", "name": old["name"], "url": url,
         "image": img if img.startswith("http") else SITE + img, "description": old["description"],
         "brand": {"@type": "Brand", "name": "The Nest House"}, "productID": pid,
         "offers": {"@type": "AggregateOffer", "priceCurrency": "VND", "lowPrice": str(min(prices)), "highPrice": str(max(prices)),
                    "offerCount": str(len(items)), "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                    "seller": SELLER, "offers": items}}
    if revs:
        p["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": "%.1f" % (sum(r["rating"] for r in revs) / len(revs)),
                                "reviewCount": str(len(revs)), "bestRating": "5", "worstRating": "1"}
        p["review"] = [{"@type": "Review", "author": {"@type": "Person", "name": r["name"]}, "datePublished": r["date"],
                        "reviewRating": {"@type": "Rating", "ratingValue": str(r["rating"]), "bestRating": "5", "worstRating": "1"},
                        "reviewBody": r["text"]} for r in revs[:20]]
    return p


def main():
    check = "--check" in sys.argv
    data = json.loads((ROOT / "data/reviews.json").read_text(encoding="utf-8"))
    cart = load_cart(); problems = []; changed = 0
    for r in data.get("reviews", []):
        if r.get("product_id") not in PAGES:
            problems.append("đánh giá của '%s': product_id '%s' không hợp lệ (xem _product_id_hop_le)" % (r.get("name", "?"), r.get("product_id")))
    for pid, path in PAGES.items():
        f = ROOT / path.strip("/") / "index.html"
        html = f.read_text(encoding="utf-8")
        pat = re.compile(r'<script type="application/ld\+json">(\{[^<]*?"@type": "Product"[^<]*?)</script>', re.S)
        ms = pat.findall(html)
        if len(ms) != 1: problems.append("%s: có %d khối Product (cần đúng 1)" % (path, len(ms))); continue
        old = json.loads(ms[0])
        revs = reviews_for(data, pid, problems)
        new = build_product(old, pid, cart, revs)
        # khớp giá hiển thị: mọi giá trong schema phải xuất hiện trên trang (bảng giá hoặc khung mua tnh-cart.js)
        for o in new["offers"]["offers"]:
            shown = "{:,}".format(int(o["price"])).replace(",", ".")
            if shown not in html and o["url"].split("?qc=")[-1] not in html and o["sku"].lower() not in cart_ids(cart):
                problems.append("%s: giá %s (%s) không thấy trên trang" % (path, shown, o["sku"]))
        out = html.replace(ms[0], json.dumps(new, ensure_ascii=False))
        out = re.sub(r"<!--tnh-reviews-->.*?<!--/tnh-reviews-->\n?", "", out, flags=re.S)
        if revs:
            blk = review_block(revs)
            anchor = '    <div class="faq"'
            if anchor not in out: problems.append(path + ": không thấy chỗ chèn khối đánh giá"); continue
            out = out.replace(anchor, blk + anchor, 1)
        if len(re.findall(r'"@type": "Product"', out)) != 1: problems.append(path + ": sau khi sinh còn != 1 Product")
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S): json.loads(m)
        if out != html:
            changed += 1
            if not check: f.write_text(out, encoding="utf-8")
    print(("KIỂM" if check else "GHI"), "- trang thay đổi:", changed, "· đánh giá thật:", len(data.get("reviews", [])))
    for p in problems: print("⚠️", p)
    sys.exit(1 if problems and check else 0)


def cart_ids(cart):
    return {c["id"] for v in cart.values() for c in v}


if __name__ == "__main__":
    main()
