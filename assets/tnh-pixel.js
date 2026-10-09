/* Meta Pixel The Nest House (CEO duyệt 10/10/2026) — đặc tả: vault website/he-thong-pixel-capi.md mục 5.
   - MỘT chỗ cấu hình duy nhất: PIXEL_ID bên dưới. Nạp từ tnh-chat.js (mọi trang) — không sửa từng trang.
   - PageView: Pixel tự bắn. ViewContent / AddToCart / InitiateCheckout: gọi tnhTrack() từ tnh-cart.js (Pixel + bản sao CAPI cùng event_id để Meta gộp 1).
   - ⛔ KHÔNG phát Purchase từ trình duyệt: Purchase chỉ do Worker (CAPI) phát khi nhân viên bấm ✅ ghi sổ.
   - ⛔ Không gửi SĐT / email / địa chỉ / tên. Chỉ cookie _fbp/_fbc của chính Pixel + mã sản phẩm, giá, số lượng.
   Nguồn: vault 09-marketing/website/assets/tnh-pixel.js → copy sang repo tnh-home/assets/. */
(function () {
  if (window.__tnhPixel) return; window.__tnhPixel = 1;
  var PIXEL_ID = "28277449071950592"; // dataset "TNH - thenesthouse.com.vn" (không phải khoá bí mật)
  if (!/^\d{8,20}$/.test(PIXEL_ID)) return;
  var CAPI = "https://tnh-chatbot.telegram-duyet-worker.workers.dev/capi/event";
  var OK = { ViewContent: 1, AddToCart: 1, InitiateCheckout: 1, Contact: 1, Lead: 1 }; // Purchase cố ý không có

  !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', PIXEL_ID);
  fbq('track', 'PageView');

  function ck(n) { var m = document.cookie.match(new RegExp("(?:^|; )" + n + "=([^;]*)")); return m ? decodeURIComponent(m[1]) : ""; }
  window.tnhCookies = function () { return { fbp: ck("_fbp"), fbc: ck("_fbc") }; }; // tnh-cart.js đính vào body /cart/order

  window.tnhTrack = function (name, data) {
    if (!OK[name]) return "";
    var eid = name + "_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8), c = window.tnhCookies();
    try { fbq("track", name, data || {}, { eventID: eid }); } catch (e) {}
    try {
      fetch(CAPI, { method: "POST", keepalive: true, headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event_name: name, event_id: eid, event_source_url: location.href, fbp: c.fbp, fbc: c.fbc, custom_data: data || {} }) }).catch(function () {});
    } catch (e) {}
    return eid;
  };

  // Sự kiện tnh-cart.js đã xếp hàng trước khi file này nạp xong
  var q = window.__tnhPxQ; window.__tnhPxQ = null;
  if (q && q.length) q.forEach(function (x) { window.tnhTrack(x[0], x[1]); });
})();
