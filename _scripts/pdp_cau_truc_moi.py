#!/usr/bin/env python3
"""Nhân cấu trúc trang sản phẩm mới (khuôn 100G sợi dài, CEO duyệt 10/10/2026) sang 11 trang còn lại — CEO đồng ý 13/10/2026.

Chạy:  python3 _scripts/pdp_cau_truc_moi.py            # repo tnh-home
       python3 _scripts/pdp_cau_truc_moi.py <thư-mục-website-vault>   # bản vault (cùng cấu trúc)
Chạy lại an toàn (đánh dấu <!--pdp-mau-->).

Mỗi trang được thêm 5 khối (3 khối "tự chạy" — khung mua, thanh Mua ngay, chân trang — đã có qua tnh-cart.js/tnh-footer.js):
  1. Hero màn hình đầu: ảnh bìa + dòng điểm đánh giá + (quà theo mốc đơn, trừ yến chưng) + khung Đặt mua + dòng cam kết.
  2. Khối "dành cho ai / chưa hợp ai" ngay sau đoạn mở đầu.
  3. Khối "Khách đã mua nói gì" (id=danh-gia) trước FAQ — SỐ THẬT từng listing Shopee của chính sản phẩm (API get_ratings, đọc 13/10/2026 qua Chrome đăng nhập):
     điểm trung bình tính từ phân bố 1–5★, số lượng + % từng mức, 2 nhận xét 5★ nguyên văn ghi tên tài khoản như Shopee hiển thị (luật 5, ngoại lệ 10/10), có ghi đánh giá thấp nếu có.
     Lazada 99% / TikTok 0% tiêu cực = điểm CẢ gian hàng (09/10/2026) — ghi rõ. ⛔ Không link sang sàn. ⛔ Không đưa vào schema AggregateRating.
  4. FAQ thêm câu "Giao hàng bao lâu, có được kiểm hàng không?" (+ "Mua yến được tặng quà gì?" cho dòng được tặng quà).
  5. CSS của khuôn.
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
MARK = "<!--pdp-mau-->"
DATE_RV = "13/10/2026"

CSS = """
  /* Khuôn trang sản phẩm (nhân từ 100G sợi dài 13/10/2026) */
  .pdp{padding-top:16px!important}
  .pdp-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:30px;align-items:start}
  .pdp-img img{border-radius:16px;width:100%;aspect-ratio:1/1;object-fit:cover;border:1px solid #e8e0cc}
  .pdp-img figcaption{font-size:.78rem;color:#536862;text-align:center;margin-top:8px}
  .rate-strip{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:center;font-size:.9rem;color:#33443f;margin-bottom:12px}
  .rate-strip .st{color:#C1A374;letter-spacing:1px;font-size:1rem}
  .rate-strip a{color:var(--gold-text);font-weight:700;text-decoration:underline}
  .offer-card{border:1.5px dashed var(--gold);background:#fffdf6;border-radius:14px;padding:14px 16px;margin:0 0 6px}
  .offer-card b.t{display:block;font-family:var(--serif);font-size:1.02rem;margin-bottom:6px}
  .offer-card ul{list-style:none;margin:0;padding:0;font-size:.92rem}
  .offer-card li{padding:3px 0 3px 26px;position:relative}
  .offer-card li:before{content:"🎁";position:absolute;left:0}
  .offer-card small{display:block;color:#5b6b66;margin-top:6px;font-size:.8rem}
  .pdp-info .tnh-proof{margin:12px 0 0!important}
  .rv{background:#faf7ee;border:1px solid #e8e0cc;border-radius:16px;padding:22px 20px;margin:26px 0}
  .rv h2{margin-top:0!important}
  .rv-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:14px 0}
  .rv-tile{background:#fff;border:1px solid #e8e0cc;border-radius:12px;padding:14px;text-align:center}
  .rv-tile .big{font-family:var(--serif);font-weight:700;font-size:1.9rem;line-height:1.1;color:var(--forest)}
  .rv-tile .lbl{font-weight:700;font-size:.88rem;display:block;margin-top:4px}
  .rv-tile small{display:block;color:#5b6b66;font-size:.78rem;margin-top:2px;line-height:1.4}
  .rv-main{display:grid;grid-template-columns:200px 1fr;gap:22px;align-items:center;margin:14px 0}
  .rv-score{text-align:center}
  .rv-score .big{font-family:var(--serif);font-weight:700;font-size:3.2rem;line-height:1;color:var(--forest);display:block}
  .rv-score .st{color:#C1A374;letter-spacing:2px;display:block}
  .rv-score small{display:block;color:#5b6b66;font-size:.78rem;line-height:1.4;margin-top:4px}
  .rv-row{display:grid;grid-template-columns:28px 1fr 46px;gap:8px;align-items:center;font-size:.84rem;margin:4px 0}
  .rv-bar{height:9px;background:#e6dcc3;border-radius:9px;overflow:hidden}
  .rv-bar b{display:block;height:100%;background:linear-gradient(90deg,#C1A374,#E3C97A)}
  .rv-quotes{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
  .rv-quotes blockquote{background:#fff;border:1px solid #e8e0cc;border-radius:12px;padding:12px 14px;font-size:.95rem;font-style:italic;margin:0}
  .rv-quotes cite{display:block;font-style:normal;font-size:.76rem;color:#5b6b66;margin-top:6px}
  .rv-note{font-size:.84rem;color:#5b6b66;margin:4px 0 12px}
  .who-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin:12px 0 18px}
  .who-grid>div{background:#faf7ee;border:1px solid #e8e0cc;border-radius:14px;padding:16px 18px}
  .who-grid p{font-weight:700;margin-bottom:8px}
  .who-grid ul{margin:0 0 0 18px;font-size:.93rem}
  .who-grid a{color:var(--gold-text);font-weight:600}
  @media(max-width:900px){.pdp-grid{grid-template-columns:1fr;gap:16px}.pdp-img img{aspect-ratio:16/9}.pdp-img figcaption{display:none}
    .rate-strip{font-size:.82rem;margin-bottom:8px;gap:2px 10px}.rate-strip .st{display:none}.rate-strip strong:before{content:"★ ";color:#C1A374}
    .offer-card{padding:11px 13px}.offer-card small{font-size:.76rem}.head{padding:22px 0}.head p,.head .crumb{display:none}.head h1{font-size:1.35rem}
    .rv-grid{grid-template-columns:1fr!important}.rv-main,.rv-quotes{grid-template-columns:1fr}
    .rv-tile{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;text-align:left;align-items:center}.rv-tile .big{grid-row:1/3;min-width:64px}}
"""

OFFER = """      <div class="offer-card">
        <b class="t">Quà tặng theo giá trị đơn hàng</b>
        <ul>
          <li>Đơn từ <strong>1.250.000đ</strong>: tặng combo 3 quà — đông trùng hạ thảo · kỷ tử · thố chưng sứ</li>
          <li>Đơn từ <strong>2.400.000đ</strong>: tặng combo 3 quà + <strong>6 hũ yến chưng sẵn 70ml</strong></li>
        </ul>
        <small>Quà nhân theo giá trị đơn: mỗi 2.400.000đ là 1 phần. Áp dụng khi mua yến tinh chế, yến thô, yến vụn hoặc set quà biếu (không áp dụng cho yến chưng sẵn). Khung "Đặt mua" bên dưới tự báo quà của quy cách anh/chị đang chọn.</small>
      </div>
"""
PROOF_COMMON = [
    "✔ Kiểm tra hàng trước khi thanh toán (COD)",
    "✔ Cửa hàng thật: Kios A126, Tầng 2, TTTM Tops Market, 685 Âu Cơ, TP.HCM (<a href=\"https://share.google/Jlp2IjomZLla08vaa\" target=\"_blank\" rel=\"noopener\" style=\"color:var(--gold-text);font-weight:600\">chỉ đường</a>)",
    "✔ Có giao trong ngày tại TP.HCM (khung 09:00–18:00, tuỳ đơn) · tỉnh khác 2–5 ngày làm việc (<a href=\"/chinh-sach/van-chuyen/\" style=\"color:var(--gold-text);font-weight:600\">xem chính sách</a>)",
    "✔ Đổi trả 90 ngày · đền 10 lần nếu sai mô tả",
]
FAQ_SHIP = ("Giao hàng bao lâu, có được kiểm hàng không?",
            "Tại TP.HCM có giao trong ngày (khung 09:00–18:00, tùy giờ đặt và địa chỉ nhận): khoảng một nửa số đơn giao được cùng ngày, các đơn còn lại 1–2 ngày làm việc; tỉnh thành khác 2–5 ngày làm việc tùy khu vực. Anh/chị được kiểm hàng cùng shipper trước khi thanh toán; vỡ, móp hoặc sai hàng thì từ chối nhận, The Nest House gửi lại đơn mới.")
FAQ_GIFT = ("Mua yến được tặng quà gì?",
            "Đơn từ 1.250.000đ được tặng combo 3 quà (đông trùng hạ thảo, kỷ tử, thố chưng sứ); đơn từ 2.400.000đ được tặng combo 3 quà và 6 hũ yến chưng sẵn 70ml. Quà nhân theo giá trị đơn, mỗi 2.400.000đ là 1 phần. Áp dụng khi mua yến tinh chế, yến thô, yến vụn hoặc set quà biếu; không áp dụng cho yến chưng sẵn.")
LAZ_TT = """      <div class="rv-grid">
        <div class="rv-tile"><span class="big">99%</span><div><span class="lbl">Lazada</span><small>đánh giá tích cực · cả gian hàng, ngày 09/10/2026</small></div></div>
        <div class="rv-tile"><span class="big">0%</span><div><span class="lbl">TikTok Shop</span><small>đánh giá tiêu cực · 97 lượt chấm trong 30 ngày, ngày 09/10/2026</small></div></div>
      </div>
      <p class="rv-note">Hai khung trên là điểm của cả gian hàng, mỗi sàn tính theo cách riêng. Anh/chị đã mua yến của The Nest House? Gửi cảm nhận qua Zalo — chúng tôi chỉ đăng khi anh/chị đồng ý và luôn ẩn tên.</p>
      <p><a class="btn btn-forest" href="https://zalo.me/0969850153" target="_blank" rel="noopener">💬 Gửi cảm nhận của anh/chị</a></p>
"""

# ---- Dữ liệu từng trang -------------------------------------------------------------
# cnt = [1★,2★,3★,4★,5★] cộng các listing Shopee của đúng sản phẩm (đọc 13/10/2026); quotes = (text, username, quy cách, tháng)
PAGES = {
 "yen-sao/tinh-che/soi-ngan": dict(
  gift=True, short="yến sợi ngắn", group="các sản phẩm yến tinh chế sợi ngắn (30g · 50g · 100g) trên Shopee", cnt=[5,2,3,12,765],
  proof=["✔ 100g = <strong>14 tổ</strong>, 100% bụng tổ không tẩm độn"],
  low="Có cả đánh giá 1–2 sao (khoảng 0,9%): chủ yếu về thời gian giao của đơn vị vận chuyển. Chúng tôi trả lời từng đánh giá trên Shopee.",
  quotes=[("Yến sào của The Nest House có chất lượng tốt. Mình mua lần này là lần thứ 3 rồi. Giá cả vừa phải, người có thu nhập trung bình cũng sử dụng được.","lethuha5","mua 100g sợi ngắn trên Shopee","08/2026"),
          ("Shop gửi hàng rất cẩn thận, quà tặng rất đầy đủ. Khâu đóng gói bao bì làm rất ổn, đem tặng quà rất đẹp.","quynh_anh_31117","mua 100g sợi ngắn trên Shopee","09/2025")],
  who_ok=["Dùng đều cho người nhà: bố mẹ lớn tuổi, trẻ em, người mới ốm dậy — sợi ngắn nở mềm, dễ ăn, giá mỗi gram mềm hơn sợi dài.","Muốn tự kiểm hàng bằng mắt: 100g có 14 tổ, đếm được khi nhận hộp.","Muốn hộp quà tươm tất mà ngân sách vừa phải: vẫn kèm hộp túi và nguyên liệu chưng."],
  who_no=["Cần món quà biếu sếp, đối tác cần \"nhìn là biết\": <a href=\"/yen-sao/tinh-che/soi-dai/\">yến sợi dài loại 1</a> hoặc <a href=\"/yen-sao/tinh-che/rut-long/\">rút lông nguyên tổ</a> hợp hơn.","Không muốn tự ngâm, tự chưng: xem <a href=\"/yen-sao/yen-chung/yen-chung-100/\">yến chưng sẵn</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/tinh-che/rut-long": dict(
  gift=True, short="yến rút lông nguyên tổ", group="sản phẩm yến rút lông nguyên tổ xuất khẩu 100g trên Shopee", cnt=[2,1,1,2,156],
  proof=["✔ 100g = <strong>9 tổ</strong>, 90% sợi phủ 2 mặt, giữ nguyên dáng tổ"],
  low="Có cả đánh giá 1–2 sao (khoảng 1,9%): chủ yếu về tổ bị vỡ vụn trong vận chuyển. Chúng tôi trả lời từng đánh giá trên Shopee và đổi hàng theo chính sách 90 ngày.",
  quotes=[("Yến rút lông nguyên tổ có mùi thơm tự nhiên, dễ sử dụng, sợi yến dai, tổ lớn, chất lượng cao cấp.","t*****l","mua rút lông xuất khẩu trên Shopee","09/2026"),
          ("Mình xem review rồi mua theo, hộp sang trọng, shop tặng luôn đồ để chưng yến luôn, mãi iu shop.","n*****9","mua yến sợi dài/rút lông trên Shopee","08/2026")],
  who_ok=["Biếu sếp, đối tác, bố mẹ chồng/vợ dịp quan trọng: dòng cao nhất của The Nest House, tổ nguyên dáng, sợi nhiều nhất.","Thích sợi yến dài rõ miếng, giòn dai khi chưng; muốn tỉ lệ sợi cao hơn dòng sợi dài loại 1.","Muốn tự kiểm: 100g có 9 tổ, nhặt lông bằng nhíp nên nhìn rõ từng sợi."],
  who_no=["Dùng đều trong nhà và muốn tiết kiệm: <a href=\"/yen-sao/tinh-che/soi-ngan/\">yến sợi ngắn</a> hoặc <a href=\"/yen-sao/tinh-che/chan-yen/\">chân yến</a> hợp hơn.","Cần quà tầm 500.000–1.000.000đ: xem <a href=\"/yen-sao/set-qua-bieu/\">set quà biếu</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/tinh-che/chan-yen": dict(
  gift=True, short="chân yến", group="sản phẩm chân yến tinh chế rút lông 50–100g trên Shopee", cnt=[0,0,1,1,55],
  proof=["✔ Chân cục và chân rìa — phần dày nhất của tổ, nở nhiều"],
  low=None,
  quotes=[("Chân yến làm sạch rất chất lượng, chưng lên giòn dai rất ngon luôn. Lại được tặng kèm đủ nguyên liệu chưng yến nữa.","s*****e","mua chân yến trên Shopee","10/2022"),
          ("Yến ngon đảm bảo chất lượng, đã mua nhiều lần và sẽ ủng hộ lâu dài.","lienbui1102","mua chân cục 100g trên Shopee","09/2025")],
  who_ok=["Nhà dùng đều, ăn thật chứ không biếu: chân yến giòn sần sật, nở nhiều, giá mềm hơn tổ sợi.","Thích chưng lâu, ăn miếng dày: chân cục hợp; thích mỏng dễ nở: chân rìa.","Muốn tiết kiệm mà vẫn đúng yến The Nest House (cùng tổ, chỉ khác phần)."],
  who_no=["Cần hộp quà biếu nhìn nguyên tổ: xem <a href=\"/yen-sao/tinh-che/soi-dai/\">yến sợi dài loại 1</a> hoặc <a href=\"/yen-sao/tinh-che/rut-long/\">rút lông nguyên tổ</a>.","Không muốn tự ngâm, tự chưng: xem <a href=\"/yen-sao/yen-chung/yen-chung-100/\">yến chưng sẵn</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/tinh-che/yen-vun": dict(
  zalo_buy='''<div id="dat-mua" class="offer-card" style="border-style:solid;background:#FFFDF7">
        <b class="t">Đặt mua yến vụn — nhắn Zalo, giao COD toàn quốc</b>
        <ul style="list-style:none">
          <li style="padding-left:0">Set 3g (1 lần chưng) — <strong>90.000đ</strong> · 50g + hộp + nguyên liệu — <strong>1.300.000đ</strong> · 100g + hộp + nguyên liệu — <strong>2.500.000đ</strong></li>
        </ul>
        <p style="margin:10px 0 0;display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-gold" href="https://zalo.me/0969850153" target="_blank" rel="noopener">💬 Nhắn Zalo đặt mua</a><a class="btn btn-outline" style="color:var(--forest)" href="tel:0969850153">☎ 0969.850.153</a></p>
        <small>Giá niêm yết; nhắn Zalo nhận giá đặt trực tiếp. Kiểm hàng trước khi thanh toán.</small>
      </div>''',
  gift=True, short="yến vụn", group="các sản phẩm yến vụn tinh chế (set 3g · 50g · 100g) trên Shopee", cnt=[3,2,6,18,594],
  proof=["✔ Tách từ chính tổ yến The Nest House, không đắp keo — ngâm nhanh, chưng 15–20 phút"],
  low="Có cả đánh giá 1–2 sao (khoảng 0,8%): về độ nở của một lô 50g năm 2023 và giao hàng. Chúng tôi trả lời từng đánh giá trên Shopee.",
  quotes=[("Hàng dùng ok, giao hàng đúng hạn. Gói hàng cẩn thận, rất ưng ý nha.","l*****6","mua yến vụn 100g trên Shopee","03/2026"),
          ("Shop đóng gói hàng cẩn thận, mỗi set yến để riêng 1 hộp nên rất dễ bảo quản.","b*****m","mua 5 set yến vụn 3g trên Shopee","09/2022")],
  who_ok=["Cho bé mới tập ăn yến hoặc muốn thử trước: set 3g đúng một lần chưng, không phải mua hộp lớn.","Nhà dùng đều, ưu tiên tiết kiệm: 50g/100g vụn cùng nguồn tổ, chỉ khác dạng.","Người bận: ngâm nhanh, chưng 15–20 phút là xong."],
  who_no=["Cần quà biếu nhìn nguyên tổ: xem <a href=\"/yen-sao/tinh-che/soi-dai/\">yến sợi dài loại 1</a> hoặc <a href=\"/yen-sao/set-qua-bieu/hop-1-to/\">hộp 1 tổ</a>.","Thích sợi dài rõ miếng khi chưng: xem <a href=\"/yen-sao/tinh-che/soi-ngan/\">sợi ngắn</a> hoặc <a href=\"/yen-sao/tinh-che/soi-dai/\">sợi dài</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/yen-tho": dict(
  gift=True, short="yến thô", group="sản phẩm yến thô ít lông nguyên tổ 50–100g trên Shopee", cnt=[1,1,5,7,87],
  proof=["✔ Tổ nguyên chưa làm sạch, ít lông — tự nhặt bằng nhíp (kèm hướng dẫn)"],
  low="Yến thô là tổ chưa làm sạch nên có góp ý 3–4 sao (khoảng 12%), chủ yếu về lượng lông phải nhặt. Chúng tôi ghi rõ điều này ở trên và trả lời từng đánh giá trên Shopee.",
  quotes=[("Lượng lông yến không quá nhiều, dễ xử lý, có cửa hàng nên yên tâm mua sử dụng.","ohu6bbm608","mua yến thô 100g trên Shopee","07/2026"),
          ("Đã mua lần hai. Được cái khá ít lông.","dg0fqxru5j","mua yến thô 50g + 100g trên Shopee","10/2025")],
  who_ok=["Muốn thấy tổ yến nguyên bản chưa qua xử lý và tự tay làm sạch cho yên tâm.","Có thời gian nhặt lông (30–60 phút/tổ) và muốn giá mỗi gram thấp nhất.","Đã quen dùng yến, biết cách ngâm – nhặt – chưng."],
  who_no=["Chưa từng nhặt lông yến hoặc không có thời gian: <a href=\"/yen-sao/tinh-che/soi-ngan/\">yến tinh chế</a> đã làm sạch sẵn.","Mua để biếu: xem <a href=\"/yen-sao/tinh-che/soi-dai/\">yến sợi dài loại 1</a> hoặc <a href=\"/yen-sao/set-qua-bieu/\">set quà biếu</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/yen-chung/yen-chung-30": dict(
  gift=False, short="yến chưng sẵn 30%", group="các sản phẩm yến chưng sẵn 30% sợi yến (set 6 hũ, từng vị, 20 hũ) trên Shopee", cnt=[6,3,17,23,1201],
  proof=["✔ 30% sợi yến thật, chưng tươi theo lô, HSD in trên nắp","✔ Giao chống sốc từng hũ"],
  low="Có cả đánh giá 1–2 sao (khoảng 0,7%): chủ yếu về giao nhầm vị trong năm 2023. Chúng tôi trả lời từng đánh giá trên Shopee; đặt trên web anh/chị chọn vị ngay trong khung Đặt mua.",
  quotes=[("Có nhiều hương vị thơm ngon, dễ uống cho mọi lứa tuổi. Hộp đẹp, shop đóng gói cẩn thận, sang trọng, thích hợp làm quà tặng.","h*****8","mua set 6 hũ trên Shopee","10/2026"),
          ("Yến thơm, ngon, ngọt thanh hợp khẩu vị. Vị đông trùng ngon tuyệt luôn.","h*****j","mua 6 hũ đông trùng trên Shopee","11/2025")],
  who_ok=["Cả nhà dùng đều mà không ai muốn chưng: mở nắp là dùng, 4 vị để mỗi người một hũ đúng ý.","Quà biếu tầm 250.000–450.000đ cho đồng nghiệp, hàng xóm, thầy cô: set 6–10 hũ có hộp túi.","Người mới bắt đầu dùng yến: giá mỗi hũ mềm, thử vị trước khi lên dòng 100%."],
  who_no=["Muốn đậm sợi yến, dùng cho người cần bồi bổ thật sự: xem <a href=\"/yen-sao/yen-chung/yen-chung-100/\">yến chưng 100% Hoàng Kim</a>.","Thích tự chưng để kiểm soát độ ngọt: xem <a href=\"/yen-sao/tinh-che/yen-vun/\">yến vụn</a> hoặc <a href=\"/yen-sao/tinh-che/soi-ngan/\">sợi ngắn</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/yen-chung/yen-chung-100": dict(
  gift=False, short="yến chưng 100% Hoàng Kim", group="các sản phẩm yến chưng sẵn 100% sợi yến (10 · 15 · 20 hũ) trên Shopee", cnt=[2,1,5,8,486],
  proof=["✔ 100% sợi yến, không pha — đã kiểm nghiệm NEWCENLAB 06/2026 (<a href=\"/kiem-nghiem/\" style=\"color:var(--gold-text);font-weight:600\">xem phiếu</a>)","✔ Tem đen–vàng Hoàng Kim, HSD in trên nắp"],
  low="Có cả đánh giá 1–2 sao (khoảng 0,6%). Chúng tôi trả lời từng đánh giá trên Shopee.",
  quotes=[("Độ ngọt: ít ngọt, rất dễ ăn · Hương vị: rất vừa miệng · Chất lượng: sánh đặc.","hcofsezg_8","mua 20 hũ 100% trên Shopee","07/2026"),
          ("Thấy review đúng nha, hộp đẹp, yến ăn không bị lỏng lỏng như mấy loại khác.","7*****b","mua 15 hũ tam vị trên Shopee","04/2026")],
  who_ok=["Bồi bổ thật sự cho bố mẹ, người mới ốm dậy, mẹ sau sinh: mỗi hũ đậm sợi yến, không pha loãng.","Biếu sang mà người nhận dùng được ngay: set 15 hũ + hộp túi tem đen–vàng.","Muốn có phiếu kiểm nghiệm độc lập để yên tâm: dòng này đã kiểm NEWCENLAB."],
  who_no=["Chỉ cần dùng thử hoặc quà tầm 250.000đ: xem <a href=\"/yen-sao/yen-chung/yen-chung-30/\">yến chưng 30%</a>.","Thích tự chưng để kiểm soát độ ngọt: xem <a href=\"/yen-sao/tinh-che/soi-ngan/\">yến tinh chế</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/set-qua-bieu/hop-1-to": dict(
  gift=True, short="hộp 1 tổ yến", group="sản phẩm hộp 1 tổ yến tinh chế trên Shopee", cnt=[1,4,5,10,278],
  proof=["✔ 1 tổ yến tinh chế nguyên dáng trong hộp quà nhỏ — chọn sợi ngắn hoặc sợi dài"],
  low="Có cả đánh giá 1–2 sao (khoảng 1,7%): chủ yếu về giao hàng. Chúng tôi trả lời từng đánh giá trên Shopee.",
  quotes=[("Hàng gói đẹp và chất lượng cao nha mọi người, mình chưng ăn thử hôm qua và khá hài lòng về sản phẩm, sẽ ủng hộ nhiều hơn.","minu1512","mua hộp 1 tổ trên Shopee","11/2023"),
          ("Hàng ổn áp, như hình, giao nhanh, để ăn thử rồi sẽ ủng hộ tiếp, đóng gói rất là đẹp, phù hợp đem biếu tặng.","n*****1","mua hộp 1 tổ trên Shopee","12/2022")],
  who_ok=["Quà nhỏ nhưng có ý: thầy cô, đồng nghiệp, khách hàng, bạn bè — tặng nhiều người cùng lúc.","Muốn cho người thân dùng thử yến The Nest House trước khi mua hộp lớn.","Kèm thiệp và túi, cầm đi tặng ngay không phải gói thêm."],
  who_no=["Biếu sếp/đối tác quan trọng: xem <a href=\"/yen-sao/tinh-che/soi-dai/\">hộp 50g–100g sợi dài</a> hoặc <a href=\"/yen-sao/set-qua-bieu/sac-xuan-30g/\">set Sắc Xuân 30g</a>.","Nhà dùng đều: 1 tổ chỉ đủ 1–2 lần chưng — xem <a href=\"/yen-sao/tinh-che/soi-ngan/\">yến sợi ngắn</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/set-qua-bieu/tam-giao": dict(
  gift=True, short="set quà Tâm Giao", group="bộ set quà biếu (Tâm Giao · Tứ Quý · Sắc Xuân) trên Shopee", cnt=[0,0,0,1,68],
  proof=["✔ 2 tổ yến tinh chế trong hộp quà — chọn sợi ngắn hoặc sợi dài"],
  low="Một khách 5 sao góp ý hộp Tâm Giao \"khá nhỏ gọn, nếu nơ to hơn sẽ sang hơn\" (10/2025) — chúng tôi ghi nhận; hộp giữ cỡ nhỏ để đúng giá quà tầm 600.000đ.",
  quotes=[("Em nhận được hàng rồi, chất lượng lắm ạ, đóng gói kỹ lưỡng, giao hàng nhanh lắm, sẽ ủng hộ shop dài dài.","uyenthi341","mua set Tâm Giao trên Shopee","01/2025"),
          ("Shop giao nhanh, đóng gói rất kỹ, được tặng kèm nhiều quà tặng, hộp rất đẹp sang trọng.","t*****k","mua set Sắc Xuân 30g trên Shopee","01/2026")],
  who_ok=["Quà Tết, 20/10, 20/11 cho người quen tầm 600.000–800.000đ: có hộp, túi, thiệp, 2 tổ đủ 2 lần chưng.","Tặng nhiều người cùng lúc (đối tác, khách hàng) mà vẫn muốn quà \"có yến thật\".","Muốn người nhận dùng thử trước khi mua hộp lớn."],
  who_no=["Biếu sếp/đối tác lớn: xem <a href=\"/yen-sao/set-qua-bieu/sac-xuan-30g/\">Sắc Xuân 30g</a> hoặc <a href=\"/yen-sao/tinh-che/soi-dai/\">hộp 50g–100g sợi dài</a>.","Người nhận không tự chưng: xem <a href=\"/yen-sao/yen-chung/yen-chung-100/\">yến chưng 100% Hoàng Kim</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/set-qua-bieu/tu-quy": dict(
  gift=True, short="set quà Tứ Quý", group="bộ set quà biếu (Tâm Giao · Tứ Quý · Sắc Xuân) trên Shopee", cnt=[0,0,0,1,68],
  proof=["✔ 4 hộp yến vụn 3g — mỗi hộp đúng 1 lần chưng"],
  low=None,
  quotes=[("Shop giao nhanh, đóng gói rất kỹ, được tặng kèm nhiều quà tặng, hộp rất đẹp sang trọng.","t*****k","mua set Sắc Xuân 30g trên Shopee","01/2026"),
          ("Em nhận được hàng rồi, chất lượng lắm ạ, đóng gói kỹ lưỡng, giao hàng nhanh lắm, sẽ ủng hộ shop dài dài.","uyenthi341","mua set Tâm Giao trên Shopee","01/2025")],
  who_ok=["Quà cho gia đình có trẻ nhỏ hoặc người lớn tuổi: 4 lần chưng chia sẵn, không phải cân đong.","Quà Tết, quà cảm ơn tầm 500.000đ cho nhiều người.","Người nhận chưa quen chưng yến: lượng nhỏ, hướng dẫn kèm hộp."],
  who_no=["Muốn quà nhìn nguyên tổ: xem <a href=\"/yen-sao/set-qua-bieu/tam-giao/\">Tâm Giao 2 tổ</a> hoặc <a href=\"/yen-sao/set-qua-bieu/sac-xuan-30g/\">Sắc Xuân 30g</a>.","Người nhận không tự chưng: xem <a href=\"/yen-sao/yen-chung/yen-chung-30/\">yến chưng sẵn</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
 "yen-sao/set-qua-bieu/sac-xuan-30g": dict(
  gift=True, short="set Sắc Xuân 30g", group="bộ set quà biếu (Tâm Giao · Tứ Quý · Sắc Xuân) trên Shopee", cnt=[0,0,0,1,68],
  proof=["✔ 30g yến tinh chế (sợi ngắn hoặc sợi dài) trong hộp quà Tết"],
  low=None,
  quotes=[("Shop giao nhanh, đóng gói rất kỹ, được tặng kèm nhiều quà tặng, hộp rất đẹp sang trọng.","t*****k","mua set Sắc Xuân 30g trên Shopee","01/2026"),
          ("Giao hàng nhanh, hộp đẹp rất xịn để mang đi biếu, lần sau sẽ ủng hộ tiếp.","92yz2rnd2_","mua set Sắc Xuân 30g trên Shopee","02/2025")],
  who_ok=["Biếu sếp, đối tác, bố mẹ dịp Tết tầm 1.000.000đ: hộp quà Tết đủ hộp – túi – thiệp, 30g đủ 3 tổ.","Muốn chọn sợi: sợi dài để biếu sang, sợi ngắn để người nhận dùng đều.","Mua số lượng cho công ty: mẫu đồng nhất, có hoá đơn."],
  who_no=["Quà tầm dưới 600.000đ: xem <a href=\"/yen-sao/set-qua-bieu/tam-giao/\">Tâm Giao</a> hoặc <a href=\"/yen-sao/set-qua-bieu/hop-1-to/\">hộp 1 tổ</a>.","Biếu người đặc biệt quan trọng: xem <a href=\"/yen-sao/tinh-che/rut-long/\">rút lông nguyên tổ 100g</a>.","Mong yến thay thế thuốc hay điều trị bệnh: yến sào là thực phẩm bồi bổ, không phải thuốc và không có tác dụng thay thế thuốc chữa bệnh."]),
}


def fmt_n(n):
    return f"{n:,}".replace(",", ".")


def review_block(d):
    cnt = d["cnt"]; total = sum(cnt)
    avg = sum((i + 1) * c for i, c in enumerate(cnt)) / total
    avg_s = f"{avg:.1f}".replace(".", ",")
    pcts = [c / total * 100 for c in cnt]
    rows = ""
    for star in (5, 4, 3, 2, 1):
        pc = pcts[star - 1]
        rows += f'<div class="rv-row"><span>{star}★</span><div class="rv-bar"><b style="width:{pc:.1f}%"></b></div><span>{pc:.1f}'.replace(f'<span>{pc:.1f}', "<span>" + f"{pc:.1f}".replace(".", ",")) + "%</span></div>"
    q = "".join(f'<blockquote>“{t}”<cite>{u} · {v} · {m}</cite></blockquote>' for t, u, v, m in d["quotes"])
    low = f'      <p class="rv-note">{d["low"]}</p>\n' if d.get("low") else ""
    return f'''<div class="rv" id="danh-gia">
      <h2>Khách đã mua nói gì về {d["short"]} The Nest House</h2>
      <p class="rv-note">Số liệu lấy từ phần đánh giá công khai của chính gian hàng chúng tôi trên Shopee, ngày {DATE_RV}, cộng đúng các listing của sản phẩm này. Điểm và số lượng giữ nguyên như sàn hiển thị; nhận xét bên dưới là đánh giá thật, ghi tên tài khoản Shopee như sàn hiển thị.</p>
      <div class="rv-main">
        <div class="rv-score"><span class="big">{avg_s}</span><span class="st" aria-hidden="true">★★★★★</span><small>{fmt_n(total)} đánh giá cho {d["group"]}</small></div>
        <div class="rv-dist">{rows}</div>
      </div>
{low}      <div class="rv-quotes">{q}</div>
{LAZ_TT}    </div>

    '''


def who_block(d):
    ok = "".join(f"<li>{x}</li>" for x in d["who_ok"]); no = "".join(f"<li>{x}</li>" for x in d["who_no"])
    return f'''<h2 id="danh-cho-ai">{d["short"][0].upper() + d["short"][1:]} dành cho ai, chưa hợp với ai?</h2>
    <div class="who-grid">
      <div><p>Phù hợp nếu anh/chị</p><ul>{ok}</ul></div>
      <div><p>Có thể chưa hợp nếu anh/chị</p><ul>{no}</ul></div>
    </div>

    '''


def transform(html, d):
    if MARK in html:
        return html
    # 1. CSS — chèn vào khối <style> chính (khối cuối trong <head>; khối đầu là font nhúng)
    he = html.find("</head>"); st = html.rfind("</style>", 0, he)
    html = html[:st] + CSS + html[st:]
    # 2. lấy khung mua + ảnh bìa ra khỏi phần chữ
    m = re.search(r'<div id="dat-mua"[^>]*>.*?</div>\n?', html, re.S)
    if m:
        buy = m.group(0).strip(); html = html[:m.start()] + html[m.end():]; pos = m.start()
    else:  # trang không có giỏ hàng (yến vụn: mua qua Zalo) → khung đặt mua Zalo
        buy = d["zalo_buy"]; pos = html.find('<div class="container prose">')
    f = re.search(r'\s*<figure>\s*<img[^>]+>\s*(?:<figcaption>.*?</figcaption>)?\s*</figure>\n?', html[pos:], re.S); assert f, "thiếu ảnh bìa"
    fig = f.group(0).strip().replace("<figure>", '<figure class="pdp-img">', 1)
    fig = re.sub(r'\s+loading="lazy"', "", fig)
    if "fetchpriority" not in fig:
        fig = fig.replace("<img", '<img fetchpriority="high"', 1)
    html = html[:pos + f.start()] + html[pos + f.end():]
    # HK: bỏ rate-strip cũ + khối đánh giá cũ (số nhóm chung 1.732) — thay bằng số đúng listing 100%
    html = re.sub(r'\s*<div class="rate-strip">.*?</div>\n?', "\n", html, count=1, flags=re.S)
    html = re.sub(r'<div class="rv"[^>]*>.*?</div>\s*(?=<div class="faq")', "", html, count=1, flags=re.S)
    html = re.sub(r'<h2>Khách đã mua nói gì.*?(?=<div class="faq")', "", html, count=1, flags=re.S)
    # 3. hero
    cnt = d["cnt"]; total = sum(cnt); avg = f"{sum((i+1)*c for i,c in enumerate(cnt))/total:.1f}".replace(".", ",")
    proof = "".join(f"\n      <li>{x}</li>" for x in d["proof"] + PROOF_COMMON)
    hero = f'''<section class="pdp" style="padding:26px 0 6px">{MARK}
  <div class="container pdp-grid">
    {fig}
    <div class="pdp-info">
      <div class="rate-strip"><span class="st" aria-hidden="true">★★★★★</span><span><strong>{avg}/5</strong> · {fmt_n(total)} đánh giá {d["short"]} trên Shopee</span><a href="#danh-gia">Xem đánh giá</a></div>
{OFFER if d["gift"] else ""}{buy}
      <ul class="tnh-proof" style="list-style:none;margin:0;padding:0;font-size:.86rem;color:#4a5f59;display:flex;flex-wrap:wrap;gap:6px 18px">{proof}
    </ul>
    </div>
  </div>
</section>
'''
    i = html.find('<section style="padding-bottom:20px">'); assert i > 0, "thiếu section mở đầu"
    html = html[:i] + hero + html[i:]
    # 4. dành cho ai — trước h2 đầu tiên trong phần chữ
    j = html.find("<h2", html.find('<div class="container prose">', i)); assert j > 0
    html = html[:j] + who_block(d) + html[j:]
    # 5. đánh giá — trước FAQ
    k = html.find('<div class="faq"'); assert k > 0, "thiếu FAQ"
    html = html[:k] + review_block(d) + html[k:]
    # 6. FAQ bổ sung
    k = html.find('<div class="faq"'); end = html.find("</div>", k)
    add = ""
    if d["gift"] and "tặng quà gì" not in html[k:end]:
        add += f'      <p style="font-weight:700;margin-top:12px">{FAQ_GIFT[0]}</p>\n      <p>{FAQ_GIFT[1]}</p>\n'
    if "kiểm hàng" not in html[k:end]:
        add += f'      <p style="font-weight:700;margin-top:12px">{FAQ_SHIP[0]}</p>\n      <p>{FAQ_SHIP[1]}</p>\n'
    html = html[:end] + add + html[end:]
    return html


def main():
    n = 0
    for rel, d in PAGES.items():
        p = ROOT / rel / "index.html"
        if not p.exists():
            print("  (không có)", rel); continue
        s = p.read_text(encoding="utf-8")
        try:
            x = transform(s, d)
        except AssertionError as e:
            print("  ✗", rel, e); continue
        if x != s:
            p.write_text(x, encoding="utf-8"); n += 1; print("  ✓", rel)
    print(f"{n} trang đổi")


if __name__ == "__main__":
    main()
