/* Giỏ hàng The Nest House (CEO chốt 05/10/2026) — gửi đơn về Worker tnh-chatbot /cart/order.
   - Trang sản phẩm: <div data-tnh-buy="/yen-sao/..."></div> → chọn quy cách + số lượng + Thêm vào giỏ / Mua ngay.
     Link ?qc=<mã> chọn sẵn quy cách (Google Mua sắm trỏ về đúng quy cách, giá hiện khớp feed).
   - Trang /gio-hang/: <div data-tnh-checkout></div> → danh sách, phí ship, quà theo mốc, form đặt hàng.
   - Mọi trang: nút "🛒 Giỏ hàng (n)" góc trái dưới khi giỏ có hàng (nạp qua tnh-chat.js).
   GIÁ ở đây phải khớp banggia. (máy chủ tự tính lại; lệch → báo khách tải lại trang, không nhận đơn sai tiền).
   Nguồn: vault 09-marketing/website/assets/tnh-cart.js → copy sang repo tnh-home/assets/. */
(function () {
  if (window.__tnhCart) return;
  window.__tnhCart = 1;

  var API = "https://tnh-chatbot.telegram-duyet-worker.workers.dev/cart/order";
  var KEY = "tnh_cart_v1";
  var SHIP = 50000, FREESHIP = 1000000;
  var GIFTS = [
    { from: 2400000, text: "Combo 3 quà (đông trùng · kỷ tử · thố chưng sứ) + yến chưng sẵn" },
    { from: 1250000, text: "Combo 3 quà (đông trùng · kỷ tử · thố chưng sứ)" }
  ];
  var G = {
    sd: "🕊️ Yến tinh chế sợi dài loại 1", sn: "🕊️ Yến tinh chế sợi ngắn", rl: "👑 Yến rút lông xuất khẩu",
    th: "🌿 Yến thô nguyên tổ", vun: "🍥 Yến vụn tinh chế", cy: "🪺 Chân yến rút lông",
    c30: "🥣 Yến chưng sẵn 70ml — 30% sợi yến (dòng phổ thông)", hk: "✨ Yến chưng sẵn 70ml — 100% sợi yến (Hoàng Kim)"
  };
  // id: [trang, tên hiển thị, nhóm banggia, quy cách banggia, giá, ảnh]
  var P = {
    sd30: ["/yen-sao/tinh-che/soi-dai/", "Yến sợi dài loại 1 — 30G + hộp túi (3 tổ)", G.sd, "30G + hộp túi", 900000, "/assets/30G-yen-tinh-che-hop-xanh.jpg"],
    sd50: ["/yen-sao/tinh-che/soi-dai/", "Yến sợi dài loại 1 — 50G + hộp túi (5 tổ)", G.sd, "50G + hộp túi", 1450000, "/assets/50G-soi-dai.jpg"],
    sd100: ["/yen-sao/tinh-che/soi-dai/", "Yến sợi dài loại 1 — 100G + hộp túi (10 tổ)", G.sd, "100G + hộp túi", 2750000, "/assets/100G-soi-dai.jpg"],
    sn30: ["/yen-sao/tinh-che/soi-ngan/", "Yến sợi ngắn — 30G + hộp túi (4 tổ)", G.sn, "30G + hộp túi", 850000, "/assets/30G-yen-tinh-che-hop-xanh.jpg"],
    sn50: ["/yen-sao/tinh-che/soi-ngan/", "Yến sợi ngắn — 50G + hộp túi (7 tổ)", G.sn, "50G + hộp túi", 1250000, "/assets/50G-soi-ngan.jpg"],
    sn100: ["/yen-sao/tinh-che/soi-ngan/", "Yến sợi ngắn — 100G + hộp túi (14 tổ)", G.sn, "100G + hộp túi", 2400000, "/assets/100g-yen-tinh-che-soi-ngan.jpg"],
    rl50: ["/yen-sao/tinh-che/rut-long/", "Yến rút lông nguyên tổ — 50G + hộp túi (4 tổ)", G.rl, "50G + hộp túi", 1750000, "/assets/100g-yen-tinh-che-rut-long.jpg"],
    rl100: ["/yen-sao/tinh-che/rut-long/", "Yến rút lông nguyên tổ — 100G + hộp túi (9 tổ)", G.rl, "100G + hộp túi", 3400000, "/assets/100g-yen-tinh-che-rut-long.jpg"],
    cy50: ["/yen-sao/tinh-che/chan-yen/", "Chân yến rút lông — 50G + hộp túi", G.cy, "50G + hộp túi", 1450000, "/assets/chan-yen-rut-long.jpg"],
    cy100: ["/yen-sao/tinh-che/chan-yen/", "Chân yến rút lông — 100G + hộp túi", G.cy, "100G + hộp túi", 2850000, "/assets/chan-yen-rut-long.jpg"],
    th50: ["/yen-sao/yen-tho/", "Yến thô nguyên tổ — 50G", G.th, "50G", 1000000, "/assets/yen-tho-nguyen-to.jpg"],
    th100: ["/yen-sao/yen-tho/", "Yến thô nguyên tổ — 100G", G.th, "100G", 1900000, "/assets/yen-tho-nguyen-to.jpg"],
    hk15: ["/yen-sao/yen-chung/yen-chung-100/", "Yến chưng 100% Hoàng Kim — set 15 hũ 70ml + hộp túi", G.hk, "Set Yến Chưng Hoàng Kim (15 hũ)", 960000, "/assets/yen-chung-hoang-kim-concept-1.jpg"],
    hk10: ["/yen-sao/yen-chung/yen-chung-100/", "Yến chưng 100% Hoàng Kim — 10 hũ 70ml (không hộp)", G.hk, "10 hũ · 100% sợi yến", 480000, "/assets/yen-chung-hoang-kim-concept-1.jpg"],
    yc6: ["/yen-sao/yen-chung/yen-chung-30/", "Yến chưng 30% — set 6 hũ 70ml + hộp túi", G.c30, "Set 6 hũ + hộp túi", 200000, "/assets/yen-chung-6-hu-concept-1.jpg"],
    yc10: ["/yen-sao/yen-chung/yen-chung-30/", "Yến chưng 30% — 10 hũ 70ml (không hộp)", G.c30, "10 hũ · 30% sợi yến", 250000, "/assets/yen-chung-6-hu-concept-1.jpg"],
    tgn: ["/yen-sao/set-qua-bieu/tam-giao/", "Set quà Tâm Giao — sợi ngắn (2 tổ)", G.sn, "Set Tâm Giao (2 tổ)", 499000, "/assets/set-tam-giao-concept-1.jpg"],
    tgd: ["/yen-sao/set-qua-bieu/tam-giao/", "Set quà Tâm Giao — sợi dài (2 tổ)", G.sd, "Set Tâm Giao (2 tổ)", 650000, "/assets/set-tam-giao-concept-1.jpg"],
    tq: ["/yen-sao/set-qua-bieu/tu-quy/", "Set quà Tứ Quý (4 hộp × 3g)", G.vun, "Set quà Tứ Quý", 399000, "/assets/set-tu-quy-concept-1.jpg"],
    sxn: ["/yen-sao/set-qua-bieu/sac-xuan-30g/", "Set Sắc Xuân 30G — sợi ngắn (4 tổ)", G.sn, "30G + hộp túi", 850000, "/assets/30G-yen-tinh-che-hop-xanh.jpg"],
    sxd: ["/yen-sao/set-qua-bieu/sac-xuan-30g/", "Set Sắc Xuân 30G — sợi dài (3 tổ)", G.sd, "30G + hộp túi", 900000, "/assets/30G-yen-tinh-che-hop-xanh.jpg"],
    h1n: ["/yen-sao/set-qua-bieu/hop-1-to/", "Hộp 1 tổ yến — sợi ngắn (8g)", G.sn, "1 tổ (8g)", 200000, "/assets/hop-1-to-yen-tinh-che-tao-do.jpg"],
    h1d: ["/yen-sao/set-qua-bieu/hop-1-to/", "Hộp 1 tổ yến — sợi dài (9g)", G.sd, "1 tổ (9g)", 280000, "/assets/hop-1-to-yen-tinh-che-tao-do.jpg"]
  };
  // Nhãn ngắn trên nút chọn quy cách ở trang sản phẩm
  var SHORT = { sd30: "30G", sd50: "50G", sd100: "100G", sn30: "30G", sn50: "50G", sn100: "100G", rl50: "50G", rl100: "100G",
    cy50: "50G", cy100: "100G", th50: "50G", th100: "100G", hk15: "Set 15 hũ có hộp", hk10: "10 hũ không hộp",
    yc6: "Set 6 hũ có hộp", yc10: "10 hũ không hộp", tgn: "Sợi ngắn", tgd: "Sợi dài", tq: "Set Tứ Quý", sxn: "Sợi ngắn", sxd: "Sợi dài",
    h1n: "Sợi ngắn 8g", h1d: "Sợi dài 9g" };

  function money(n) { return Number(n).toLocaleString("vi-VN").replace(/,/g, ".") + "đ"; }
  function load() { try { var c = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(c) ? c.filter(function (x) { return P[x.id] && x.sl > 0; }) : []; } catch (e) { return []; } }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} fab(); }
  function count(c) { return c.reduce(function (a, x) { return a + x.sl; }, 0); }
  function ga(ev, p) { try { if (typeof gtag === "function") gtag("event", ev, p || {}); } catch (e) {} }
  // Meta Pixel + CAPI (CEO 10/10/2026): chỉ gửi mã sản phẩm, giá, số lượng — KHÔNG SĐT/tên/địa chỉ. KHÔNG phát Purchase ở trình duyệt (Worker phát khi nhân viên ✅).
  function px(name, ids, value, n, nameTxt) {
    var d = { content_ids: ids, content_type: "product", value: value, currency: "VND", num_items: n };
    if (nameTxt) d.content_name = nameTxt;
    try {
      if (typeof window.tnhTrack === "function") window.tnhTrack(name, d);
      else (window.__tnhPxQ = window.__tnhPxQ || []).push([name, d]); // tnh-pixel.js chưa nạp xong → xếp hàng, nạp xong tự gửi
    } catch (e) {}
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function item(id) { var p = P[id]; return { item_id: id, item_name: p[1], price: p[4], quantity: 1 }; }

  function add(id, sl) {
    var c = load(), f = c.filter(function (x) { return x.id === id; })[0];
    if (f) f.sl = Math.min(50, f.sl + sl); else c.push({ id: id, sl: sl });
    save(c);
    var it = item(id); it.quantity = sl;
    ga("add_to_cart", { currency: "VND", value: P[id][4] * sl, items: [it] });
    px("AddToCart", [id], P[id][4] * sl, sl, P[id][1]);
  }

  function totals(c) {
    var sub = c.reduce(function (a, x) { return a + P[x.id][4] * x.sl; }, 0);
    var ship = sub >= FREESHIP || !sub ? 0 : SHIP;
    var gift = null;
    for (var i = 0; i < GIFTS.length; i++) if (sub >= GIFTS[i].from) { gift = GIFTS[i]; break; }
    return { sub: sub, ship: ship, total: sub + ship, gift: gift };
  }

  // ---------- CSS ----------
  var css =
    ".tnhk-fab{position:fixed;left:16px;bottom:20px;z-index:9997;display:none;align-items:center;gap:8px;background:#C1A374;color:#0E3B33;border:0;border-radius:999px;padding:12px 18px;font:700 15px/1 'Be Vietnam Pro',system-ui,sans-serif;box-shadow:0 8px 22px rgba(0,0,0,.28);text-decoration:none}" +
    ".tnhk-buy{background:#FFFDF7;border:1.5px solid #C1A374;border-radius:16px;padding:18px;margin:18px 0;color:#1d2a27;font-family:'Be Vietnam Pro',system-ui,sans-serif}" +
    ".tnhk-buy h3{margin:0 0 10px;font-size:1.05rem;color:#0E3B33}" +
    ".tnhk-opts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}" +
    ".tnhk-opt{border:1.5px solid #cdbf9f;background:#fff;color:#1d2a27;border-radius:10px;padding:9px 12px;font-weight:600;font-size:14px;line-height:1.25;font-family:inherit;cursor:pointer;text-align:left}" +
    ".tnhk-opt small{display:block;font-weight:500;color:#5b6b66;margin-top:2px}" +
    ".tnhk-opt[aria-pressed=true]{border-color:#0E3B33;background:#0E3B33;color:#F4ECD6}.tnhk-opt[aria-pressed=true] small{color:#e6d9b8}" +
    ".tnhk-price{font-size:1.5rem;font-weight:800;color:#0E3B33;margin:4px 0}" +
    ".tnhk-was{color:#7a847f;text-decoration:line-through;font-size:.95rem;margin-left:8px;font-weight:500}" +
    ".tnhk-row{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:10px}" +
    ".tnhk-qty{display:inline-flex;align-items:center;border:1.5px solid #cdbf9f;border-radius:10px;overflow:hidden;background:#fff}" +
    ".tnhk-qty button{width:38px;height:40px;border:0;background:#f4ecd6;font-size:18px;cursor:pointer;color:#0E3B33}" +
    ".tnhk-qty input{width:46px;height:40px;border:0;text-align:center;font-weight:600;font-size:16px;font-family:inherit}" +
    ".tnhk-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border-radius:999px;padding:12px 20px;font-weight:700;font-size:15px;line-height:1;font-family:inherit;cursor:pointer;border:1.5px solid #0E3B33;text-decoration:none}" +
    ".tnhk-btn.pri{background:#0E3B33;color:#F4ECD6}.tnhk-btn.sec{background:#fff;color:#0E3B33}" +
    ".tnhk-note{font-size:.86rem;color:#4b5a55;margin-top:10px;line-height:1.5}" +
    ".tnhk-toast{position:fixed;left:50%;bottom:84px;transform:translateX(-50%);background:#0E3B33;color:#F4ECD6;padding:12px 18px;border-radius:12px;z-index:10000;font:600 14px 'Be Vietnam Pro',system-ui,sans-serif;box-shadow:0 8px 22px rgba(0,0,0,.3)}" +
    ".tnhk-co{font-family:'Be Vietnam Pro',system-ui,sans-serif;color:#1d2a27}" +
    ".tnhk-line{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid #e8dfc8}" +
    ".tnhk-line img{width:64px;height:64px;object-fit:cover;border-radius:10px}" +
    ".tnhk-line .nm{font-weight:600;line-height:1.35}.tnhk-line .pr{color:#5b6b66;font-size:.9rem;margin-top:4px}" +
    ".tnhk-rm{background:none;border:0;color:#a33;cursor:pointer;font-size:.85rem;padding:4px 0}" +
    ".tnhk-sum{background:#FFFDF7;border:1px solid #e3d7b8;border-radius:14px;padding:14px 16px;margin:14px 0}" +
    ".tnhk-sum div{display:flex;justify-content:space-between;gap:12px;padding:4px 0}.tnhk-sum .tt{font-weight:800;font-size:1.15rem;color:#0E3B33;border-top:1px dashed #cdbf9f;margin-top:6px;padding-top:10px}" +
    ".tnhk-gift{background:#f4ecd6;border-radius:10px;padding:10px 12px;margin:8px 0;font-size:.92rem}" +
    ".tnhk-form label{display:block;font-weight:600;margin:12px 0 4px}.tnhk-form input,.tnhk-form textarea{width:100%;box-sizing:border-box;border:1.5px solid #cdbf9f;border-radius:10px;padding:11px 12px;font:16px 'Be Vietnam Pro',system-ui,sans-serif;background:#fff}" +
    ".tnhk-pay{display:grid;gap:8px;margin-top:6px}.tnhk-pay label{display:flex;gap:10px;align-items:flex-start;font-weight:500;border:1.5px solid #cdbf9f;border-radius:10px;padding:10px 12px;margin:0;cursor:pointer;background:#fff}" +
    ".tnhk-err{color:#a33;font-weight:600;margin-top:10px}.tnhk-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}" +
    ".tnhk-ok{background:#FFFDF7;border:1.5px solid #C1A374;border-radius:16px;padding:20px;text-align:center}.tnhk-ok img{max-width:260px;width:100%;margin:12px auto;display:block}" +
    "@media(max-width:560px){.tnhk-btn{flex:1 1 100%}.tnhk-fab{left:12px;bottom:16px;padding:11px 15px}}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  function toast(msg) { var t = el("div", "tnhk-toast", esc(msg)); document.body.appendChild(t); setTimeout(function () { t.remove(); }, 2600); }

  // ---------- Nút nổi ----------
  var fabEl;
  function fab() {
    if (/^\/gio-hang\/?$/.test(location.pathname)) return;
    if (!fabEl) { fabEl = el("a", "tnhk-fab"); fabEl.href = "/gio-hang/"; fabEl.setAttribute("aria-label", "Xem giỏ hàng"); document.body.appendChild(fabEl); }
    var n = count(load());
    fabEl.innerHTML = "🛒 Giỏ hàng (" + n + ")";
    fabEl.style.display = n ? "inline-flex" : "none";
  }

  // ---------- Khối mua ở trang sản phẩm ----------
  // Thiết kế giá "hời" (CEO 04/10/2026): giá đặt trực tiếp to + % giảm + "tiết kiệm X" so với giá niêm yết sàn (data-was),
  // quy đổi ~giá/tổ, thanh tiến độ freeship / quà theo mốc nhảy theo số lượng. Không đếm ngược hay "sắp hết" giả.
  var BUY_CSS =
    ".tnhk-buy{position:relative;overflow:hidden;padding:0!important;border:1.5px solid #C1A374;box-shadow:0 10px 30px rgba(14,59,51,.12)}" +
    ".tnhk-rib{background:linear-gradient(90deg,#0E3B33,#1a5a4d);color:#F4ECD6;padding:10px 18px;font:700 13px/1.3 'Be Vietnam Pro',system-ui,sans-serif;letter-spacing:.04em;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}" +
    ".tnhk-rib b{color:#E3C97A}" +
    ".tnhk-in{padding:16px 18px 18px}" +
    ".tnhk-buy .tnhk-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:10px;margin-top:6px}" +
    ".tnhk-opt{position:relative;font-family:'Be Vietnam Pro',system-ui,sans-serif}" +
    ".tnhk-opt s{display:block;font-weight:500;font-size:12px;color:#8a948f;margin-top:1px}.tnhk-opt[aria-pressed=true] s{color:#bfb59a}" +
    ".tnhk-opt i{position:absolute;top:-9px;right:-6px;background:#B8322A;color:#fff;font:800 11px/1 'Be Vietnam Pro',system-ui,sans-serif;font-style:normal;padding:4px 6px;border-radius:999px}" +
    ".tnhk-pbox{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:6px 0 2px}" +
    ".tnhk-now{font:800 2.1rem/1 'Be Vietnam Pro',system-ui,sans-serif;color:#0E3B33;letter-spacing:-.01em}" +
    ".tnhk-off{background:#B8322A;color:#fff;font:800 1rem/1 'Be Vietnam Pro',system-ui,sans-serif;padding:7px 10px;border-radius:8px}" +
    ".tnhk-cmp{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:6px 0 4px;font-size:.92rem;color:#5b6b66}" +
    ".tnhk-cmp s{color:#7a847f}" +
    ".tnhk-save{background:#f6e7c4;color:#7a4f00;font-weight:800;padding:4px 10px;border-radius:999px}" +
    ".tnhk-unit{font-size:.88rem;color:#4b5a55;margin-top:2px}" +
    ".tnhk-perk{margin-top:12px;background:#f7f2e4;border-radius:12px;padding:10px 12px;font-size:.9rem;line-height:1.45}" +
    ".tnhk-bar{height:7px;background:#e6dcc3;border-radius:99px;overflow:hidden;margin:7px 0 2px}.tnhk-bar b{display:block;height:100%;background:linear-gradient(90deg,#C1A374,#E3C97A);border-radius:99px;transition:width .3s}" +
    ".tnhk-ok-l{color:#0E3B33;font-weight:700}" +
    ".tnhk-trust{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:12px;font-size:.84rem;color:#33443f}.tnhk-trust span:before{content:'✓ ';color:#1a7a52;font-weight:800}" +
    // nút + ô số lượng: khai báo font đầy đủ (shorthand "font:… inherit" không hợp lệ → trình duyệt bỏ cả dòng, nút ra chữ hệ thống nhỏ)
    ".tnhk-buy .tnhk-btn{font:700 16px/1.2 'Be Vietnam Pro',system-ui,sans-serif;padding:14px 20px}" +
    ".tnhk-buy .tnhk-btn.sec{background:linear-gradient(135deg,#C1A374,#E3C97A);border-color:#C1A374;color:#072E2C;box-shadow:0 6px 16px rgba(193,163,116,.35)}" +
    ".tnhk-buy .tnhk-qty input{font:700 16px 'Be Vietnam Pro',system-ui,sans-serif;color:#0E3B33}" +
    ".tnhk-buy .tnhk-name{font-size:.86rem!important}" +
    "@media(max-width:560px){.tnhk-now{font-size:1.85rem}.tnhk-rib{font-size:12px;padding:10px 14px}.tnhk-rib span:last-child{display:none}" +
    ".tnhk-in{padding:14px 14px 16px}.tnhk-buy .tnhk-opts{gap:8px}.tnhk-opt{padding:9px 8px!important}.tnhk-buy .tnhk-row{gap:8px}}";
  var buyCssDone = false;

  function buyBox(box) {
    var page = box.getAttribute("data-tnh-buy");
    var ids = Object.keys(P).filter(function (id) { return P[id][0] === page; });
    if (!ids.length) return;
    if (!buyCssDone) { var s2 = document.createElement("style"); s2.textContent = BUY_CSS; document.head.appendChild(s2); buyCssDone = true; }
    var qc = (location.search.match(/[?&]qc=([a-z0-9]+)/) || [])[1];
    var cur = ids.indexOf(qc) > -1 ? qc : ids[ids.length > 2 ? ids.length - 1 : 0];
    var was = {}; try { was = JSON.parse(box.getAttribute("data-was") || "{}"); } catch (e) {}
    function pct(id) { return was[id] > P[id][4] ? Math.round((1 - P[id][4] / was[id]) * 100) : 0; }
    // số tổ ghi trong tên, vd "(10 tổ)" → ra khoảng giá/tổ "250.000–275.000đ" (không lấy mỗi cận đẹp nhất để khỏi nói quá)
    function perTo(id) {
      var m = P[id][1].match(/\((\d+)(?:\s*[–-]\s*(\d+))?\s*tổ\)/); if (!m) return "";
      var r = function (k) { return Math.round(P[id][4] / k / 1000) * 1000; }, lo = r(+(m[2] || m[1])), hi = r(+m[1]);
      return lo === hi ? money(lo) : money(lo).replace("đ", "") + "–" + money(hi);
    }
    var maxOff = Math.max.apply(null, ids.map(pct));
    box.className = "tnhk-buy";
    box.innerHTML =
      "<div class='tnhk-rib'><span>🏷️ GIÁ TRỰC TIẾP" + (maxOff ? " · <b>RẺ HƠN SÀN ĐẾN " + maxOff + "%</b>" : "") + "</span><span>Giao tận nhà · COD</span></div>" +
      "<div class='tnhk-in'><div class='tnhk-opts' role='group' aria-label='Chọn quy cách'></div>" +
      "<div class='tnhk-pbox' aria-live='polite'><span class='tnhk-now'></span><span class='tnhk-off'></span></div>" +
      "<div class='tnhk-cmp'></div><div class='tnhk-unit'></div><div class='tnhk-name' style='color:#4b5a55;font-size:.9rem;margin-top:2px'></div>" +
      "<div class='tnhk-row'><span class='tnhk-qty'><button type='button' aria-label='Bớt'>−</button><input type='number' min='1' max='50' value='1' aria-label='Số lượng'><button type='button' aria-label='Thêm'>+</button></span>" +
      "<button type='button' class='tnhk-btn pri' data-act='add'>🛒 Thêm vào giỏ</button><button type='button' class='tnhk-btn sec' data-act='now'>Mua ngay</button></div>" +
      "<div class='tnhk-perk'></div>" +
      "<div class='tnhk-trust'><span>Kiểm tra hàng trước khi trả tiền</span><span>Đổi trả 90 ngày</span><span>COD hoặc chuyển khoản</span><span>Kèm nguyên liệu chưng</span></div></div>";
    var opts = box.querySelector(".tnhk-opts"), nm = box.querySelector(".tnhk-name"), qty = box.querySelector("input");
    var now = box.querySelector(".tnhk-now"), off = box.querySelector(".tnhk-off"), cmp = box.querySelector(".tnhk-cmp"),
        unit = box.querySelector(".tnhk-unit"), perk = box.querySelector(".tnhk-perk");
    ids.forEach(function (id) {
      var b = el("button", "tnhk-opt", esc(SHORT[id] || id) + "<small>" + money(P[id][4]) + "</small>" +
        (was[id] > P[id][4] ? "<s>" + money(was[id]) + "</s><i>−" + pct(id) + "%</i>" : ""));
      b.type = "button"; b.setAttribute("data-id", id);
      b.onclick = function () { cur = id; paint(); };
      opts.appendChild(b);
    });
    function n() { var v = Math.max(1, Math.min(50, parseInt(qty.value, 10) || 1)); qty.value = v; return v; }
    function paint() {
      [].forEach.call(opts.children, function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-id") === cur ? "true" : "false"); });
      var pr = P[cur][4], w = was[cur], q = n();
      now.textContent = money(pr);
      off.style.display = pct(cur) ? "" : "none"; off.textContent = "−" + pct(cur) + "%";
      cmp.innerHTML = w > pr ? "<span>Giá niêm yết trên sàn <s>" + money(w) + "</s></span><span class='tnhk-save'>Tiết kiệm " + money((w - pr) * q) + "</span>" : "";
      var pt = perTo(cur); unit.textContent = pt ? "≈ " + pt + " mỗi tổ yến" : "";
      nm.textContent = P[cur][1];
      // freeship + quà theo mốc, tính trên tạm tính của khối này (giỏ có món khác thì ở trang giỏ hàng tính lại đủ)
      var sub = pr * q, nxt = null, got = null;
      for (var i = GIFTS.length - 1; i >= 0; i--) { if (sub >= GIFTS[i].from) got = GIFTS[i]; else if (!nxt) nxt = GIFTS[i]; }
      var lines = [];
      lines.push(sub >= FREESHIP ? "<span class='tnhk-ok-l'>🚚 Được freeship toàn quốc</span>" : "🚚 Mua thêm <b>" + money(FREESHIP - sub) + "</b> để được freeship");
      if (got) lines.push("<span class='tnhk-ok-l'>🎁 Đơn này được tặng: " + esc(got.text) + "</span>");
      if (nxt) {
        lines.push("🎁 Mua thêm <b>" + money(nxt.from - sub) + "</b> để nhận: " + esc(nxt.text) +
          "<div class='tnhk-bar'><b style='width:" + Math.min(100, Math.round(sub / nxt.from * 100)) + "%'></b></div>");
      }
      perk.innerHTML = lines.join("<br>");
    }
    box.querySelectorAll(".tnhk-qty button")[0].onclick = function () { qty.value = Math.max(1, n() - 1); paint(); };
    box.querySelectorAll(".tnhk-qty button")[1].onclick = function () { qty.value = Math.min(50, n() + 1); paint(); };
    qty.onchange = paint;
    box.querySelector("[data-act=add]").onclick = function () { add(cur, n()); toast("Đã thêm vào giỏ: " + SHORT[cur]); };
    box.querySelector("[data-act=now]").onclick = function () { add(cur, n()); location.href = "/gio-hang/"; };
    paint();
    ga("view_item", { currency: "VND", value: P[cur][4], items: [item(cur)] });
    px("ViewContent", [cur], P[cur][4], 1, P[cur][1]);
  }

  // ---------- Đơn chuyển khoản: chờ nhân viên bấm "💰 Đã nhận tiền" trên Telegram (CEO chốt 05/10/2026) ----------
  // Hỏi Worker GET /cart/status mỗi 6 giây khi trang đang mở (tối đa 45 phút); có tiền → thay khối QR bằng thông báo đã thanh toán.
  var PAID_CSS = ".tnhk-paid{background:#e9f6ee;border:1.5px solid #1a7a52;border-radius:14px;padding:16px;margin:12px 0;color:#0f4d33;font-size:1.02rem;line-height:1.5}" +
    ".tnhk-paid b{font-size:1.15rem}.tnhk-paystat{font-size:.88rem;color:#5b6b66;margin-top:8px}";
  function watchPaid(root, j) {
    var st3 = document.createElement("style"); st3.textContent = PAID_CSS; document.head.appendChild(st3);
    var url = API.replace("/cart/order", "/cart/status") + "?code=" + encodeURIComponent(j.code) + "&t=" + encodeURIComponent(j.token);
    var until = Date.now() + 45 * 60 * 1000, timer = null, done = false;
    function tick() {
      if (done || Date.now() > until) return;
      var gap = document.hidden ? 15000 : 6000; // trang bị ẩn (khoá màn hình, đổi tab) vẫn hỏi nhưng thưa hơn
      fetch(url, { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (s) {
        var box = root.querySelector(".tnhk-paywait");
        if (s && s.ok && s.paid && box) {
          done = true;
          box.innerHTML = "<div class='tnhk-paid'>✅ <b>Đã nhận thanh toán " + money(j.total) + "</b><br>Đơn <b>" + esc(j.code) +
            "</b> đang được đóng gói và gửi đi sớm nhất. Cảm ơn anh/chị đã tin chọn The Nest House!</div>";
          ga("payment_confirmed", { transaction_id: j.code, currency: "VND", value: j.total });
          return;
        }
        if (s && s.ok && s.cancelled && box) {
          done = true;
          box.insertAdjacentHTML("beforeend", "<p class='tnhk-err'>Đơn này đã được huỷ — anh/chị nhắn Zalo 0969.850.153 để được hỗ trợ.</p>");
          return;
        }
        timer = setTimeout(tick, gap);
      }).catch(function () { timer = setTimeout(tick, 15000); });
    }
    document.addEventListener("visibilitychange", function () { if (!document.hidden && !done) { clearTimeout(timer); tick(); } });
    timer = setTimeout(tick, 4000);
  }

  // ---------- Trang thanh toán ----------
  function checkout(root) {
    root.className = "tnhk-co";
    var c = load();
    if (!c.length) {
      root.innerHTML = "<p>Giỏ hàng đang trống.</p><p><a class='tnhk-btn pri' href='/yen-sao/'>Xem sản phẩm yến sào →</a></p>";
      return;
    }
    var t = totals(c);
    var html = "<div class='tnhk-lines'>";
    c.forEach(function (x, i) {
      var p = P[x.id];
      html += "<div class='tnhk-line'><img src='" + p[5] + "' alt='" + esc(p[1]) + "' loading='lazy'><div><div class='nm'>" + esc(p[1]) + "</div><div class='pr'>" + money(p[4]) + "</div>" +
        "<button class='tnhk-rm' data-rm='" + i + "' type='button'>Xoá</button></div>" +
        "<span class='tnhk-qty'><button type='button' data-dec='" + i + "' aria-label='Bớt'>−</button><input type='number' value='" + x.sl + "' min='1' max='50' data-q='" + i + "' aria-label='Số lượng'><button type='button' data-inc='" + i + "' aria-label='Thêm'>+</button></span></div>";
    });
    html += "</div><div class='tnhk-sum'><div><span>Tạm tính</span><b>" + money(t.sub) + "</b></div><div><span>Phí ship</span><b>" + (t.ship ? money(t.ship) : "Miễn phí") + "</b></div>" +
      (t.ship ? "<div style='font-size:.85rem;color:#5b6b66'><span>Mua thêm " + money(FREESHIP - t.sub) + " để được freeship</span></div>" : "") +
      "<div class='tt'><span>Tổng thanh toán</span><span>" + money(t.total) + "</span></div></div>" +
      (t.gift ? "<div class='tnhk-gift'>🎁 <b>Quà tặng kèm (0đ):</b> " + esc(t.gift.text) + "</div>" :
        "<div class='tnhk-gift'>🎁 Đơn từ 1.250.000đ tặng combo 3 quà (đông trùng · kỷ tử · thố chưng sứ); từ 2.400.000đ tặng thêm yến chưng sẵn.</div>") +
      "<form class='tnhk-form' novalidate><h2 style='margin:18px 0 0;font-size:1.2rem;color:#0E3B33'>Thông tin nhận hàng</h2>" +
      "<label for='tk-name'>Họ tên người nhận *</label><input id='tk-name' name='name' autocomplete='name' required maxlength='80'>" +
      "<label for='tk-phone'>Số điện thoại *</label><input id='tk-phone' name='phone' type='tel' inputmode='tel' autocomplete='tel' required maxlength='15'>" +
      "<label for='tk-addr'>Địa chỉ nhận hàng *</label><textarea id='tk-addr' name='address' rows='2' autocomplete='street-address' required maxlength='300' placeholder='Số nhà, đường, phường/xã, tỉnh/thành phố'></textarea>" +
      "<label for='tk-note'>Ghi chú (không bắt buộc)</label><input id='tk-note' name='note' maxlength='300' placeholder='Giờ nhận hàng, xuất hoá đơn, lời chúc kèm quà…'>" +
      "<input class='tnhk-hp' name='website' tabindex='-1' autocomplete='off' aria-hidden='true'>" +
      "<label>Phương thức thanh toán *</label><div class='tnhk-pay'>" +
      "<label><input type='radio' name='method' value='cod' checked> <span><b>Thanh toán khi nhận hàng (COD)</b><br><small>Kiểm tra hàng cùng shipper, ưng mới trả tiền</small></span></label>" +
      "<label><input type='radio' name='method' value='chuyen_khoan'> <span><b>Chuyển khoản</b><br><small>Hiện mã QR và số tài khoản ngay sau khi đặt</small></span></label></div>" +
      "<div class='tnhk-err' hidden></div>" +
      "<p style='margin-top:16px'><button class='tnhk-btn pri' type='submit' style='width:100%'>Đặt hàng — " + money(t.total) + "</button></p>" +
      "<p class='tnhk-note'>Bấm Đặt hàng là anh/chị đồng ý với <a href='/chinh-sach/dieu-khoan/'>điều khoản giao dịch</a> và <a href='/chinh-sach/bao-mat/'>chính sách bảo mật</a>. Nhân viên gọi/nhắn Zalo xác nhận đơn trong giờ làm việc. Xem <a href='/chinh-sach/van-chuyen/'>vận chuyển</a> · <a href='/chinh-sach/doi-tra/'>đổi trả</a>.</p></form>";
    root.innerHTML = html;

    function setQ(i, v) { c[i].sl = Math.max(1, Math.min(50, v || 1)); save(c); checkout(root); }
    root.querySelectorAll("[data-rm]").forEach(function (b) { b.onclick = function () { c.splice(+b.getAttribute("data-rm"), 1); save(c); checkout(root); }; });
    root.querySelectorAll("[data-dec]").forEach(function (b) { b.onclick = function () { var i = +b.getAttribute("data-dec"); setQ(i, c[i].sl - 1); }; });
    root.querySelectorAll("[data-inc]").forEach(function (b) { b.onclick = function () { var i = +b.getAttribute("data-inc"); setQ(i, c[i].sl + 1); }; });
    root.querySelectorAll("[data-q]").forEach(function (b) { b.onchange = function () { setQ(+b.getAttribute("data-q"), parseInt(b.value, 10)); }; });

    var form = root.querySelector("form"), err = root.querySelector(".tnhk-err"), btn = form.querySelector("[type=submit]");
    var gaItems = c.map(function (x) { var it = item(x.id); it.quantity = x.sl; return it; });
    ga("begin_checkout", { currency: "VND", value: t.total, items: gaItems });
    if (!window.__tnhPxIC) { window.__tnhPxIC = 1; px("InitiateCheckout", c.map(function (x) { return x.id; }), t.total, count(c)); } // 1 lần/lượt mở trang (checkout() vẽ lại mỗi lần đổi số lượng)
    form.onsubmit = function (e) {
      e.preventDefault();
      var f = form.elements, msg = "";
      var phone = (f.phone.value || "").replace(/[\s.\-()]/g, "");
      if ((f.name.value || "").trim().length < 2) msg = "Vui lòng nhập họ tên người nhận.";
      else if (!/^(0|\+?84)(3|5|7|8|9)\d{8}$/.test(phone)) msg = "Số điện thoại chưa đúng (10 số, bắt đầu bằng 0).";
      else if ((f.address.value || "").trim().length < 10) msg = "Vui lòng nhập địa chỉ nhận hàng đầy đủ.";
      if (msg) { err.textContent = msg; err.hidden = false; return; }
      err.hidden = true; btn.disabled = true; btn.textContent = "Đang gửi đơn…";
      var method = form.querySelector("input[name=method]:checked").value;
      var body = { items: c.map(function (x) { return { nhom: P[x.id][2], quy_cach: P[x.id][3], sl: x.sl }; }), name: f.name.value, phone: phone,
        address: f.address.value, note: f.note.value, method: method, website: f.website.value, expect: t.total, page: location.pathname };
      try { var ck = window.tnhCookies ? window.tnhCookies() : null; if (ck) { if (ck.fbp) body.fbp = ck.fbp; if (ck.fbc) body.fbc = ck.fbc; } } catch (e) {} // cookie của Pixel, để Worker nối Purchase về lượt bấm quảng cáo
      fetch(API, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) throw j;
          ga("purchase", { transaction_id: j.code, currency: "VND", value: j.total, shipping: j.ship, items: gaItems });
          save([]);
          var ok = "<div class='tnhk-ok'><h2 style='margin:0 0 6px;color:#0E3B33'>🎉 Đặt hàng thành công</h2><p>Mã đơn: <b>" + esc(j.code) + "</b> · Tổng: <b>" + money(j.total) + "</b></p>" +
            (j.gift ? "<p>🎁 Quà tặng kèm: " + esc(j.gift) + "</p>" : "") +
            "<p>Nhân viên The Nest House sẽ gọi/nhắn Zalo số <b>" + esc(phone) + "</b> để xác nhận đơn trong giờ làm việc.</p>";
          if (method === "chuyen_khoan") {
            ok += "<div class='tnhk-paywait'>";
            ok += j.qr ? "<p><b>Quét mã để chuyển khoản đúng số tiền</b></p><img src='" + esc(j.qr) + "' alt='Mã QR chuyển khoản đơn " + esc(j.code) + "'>" +
              "<p style='text-align:left;display:inline-block'>Ngân hàng: " + esc(j.bank.bank) + "<br>Số tài khoản: <b>" + esc(j.bank.acc) + "</b><br>Chủ tài khoản: " + esc(j.bank.holder) + "<br>Số tiền: <b>" + money(j.bank.amount) + "</b><br>Nội dung: <b>" + esc(j.bank.content) + "</b></p>"
              : "<p>Nhân viên sẽ gửi thông tin chuyển khoản khi xác nhận đơn ạ.</p>";
            if (j.token) ok += "<p class='tnhk-paystat'>⏳ Chuyển khoản xong, anh/chị cứ để trang này mở — khi The Nest House nhận được tiền, trang sẽ tự báo.</p>";
            ok += "</div>";
          }
          ok += "<p class='tnhk-note'>Cần hỗ trợ gấp: <a href='https://zalo.me/0969850153'>Zalo 0969.850.153</a></p></div>";
          root.innerHTML = ok;
          window.scrollTo(0, root.offsetTop - 80);
          if (method === "chuyen_khoan" && j.token) watchPaid(root, j);
        })
        .catch(function (j) {
          btn.disabled = false; btn.textContent = "Đặt hàng — " + money(t.total);
          var m = {
            price_changed: "Giá vừa được cập nhật — vui lòng tải lại trang để xem tổng mới.",
            unknown_item: "Một sản phẩm trong giỏ đã ngừng bán — vui lòng xoá và chọn lại.",
            rate: "Anh/chị đã gửi nhiều đơn liên tiếp — vui lòng nhắn Zalo 0969.850.153 để được hỗ trợ.",
            phone: "Số điện thoại chưa đúng.", address: "Vui lòng nhập địa chỉ đầy đủ.", name: "Vui lòng nhập họ tên."
          }[j && j.error] || "Chưa gửi được đơn. Anh/chị thử lại hoặc nhắn Zalo 0969.850.153 nhé.";
          err.innerHTML = esc(m) + " <a href='https://zalo.me/0969850153'>Nhắn Zalo</a>"; err.hidden = false;
        });
    };
  }

  function init() {
    fab();
    document.querySelectorAll("[data-tnh-buy]").forEach(buyBox);
    var co = document.querySelector("[data-tnh-checkout]");
    if (co) checkout(co);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
