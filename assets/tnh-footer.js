/* Khối "Kết nối" ở chân trang (CEO 10/10/2026): bản đồ cửa hàng + khung fanpage Facebook + biểu tượng Facebook/YouTube/Zalo/Maps.
   Nạp từ tnh-chat.js (mọi trang) — thêm 1 chỗ, không sửa từng trang. Trang đã có sẵn khối .ft-connect (trang 100G sợi dài) thì bỏ qua.
   Iframe chỉ tải khi khách cuộn gần tới chân trang (không làm chậm trang). Nguồn: vault website/assets/tnh-footer.js → copy sang tnh-home/assets/. */
(function () {
  if (window.__tnhFooter) return; window.__tnhFooter = 1;
  if (/^\/gio-hang\/?$/.test(location.pathname)) return;
  function go() {
    var ft = document.querySelector("footer");
    if (!ft || document.querySelector(".ft-connect")) return;
    var MAP = "https://maps.google.com/maps?q=The+Nest+House+Y%E1%BA%BFn+S%C3%A0o+Nha+Trang%2C+685+%C3%82u+C%C6%A1%2C+T%C3%A2n+Ph%C3%BA%2C+TP.HCM&z=17&output=embed";
    var FB = "https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fthenesthouse&tabs=timeline&width=340&height=340&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=false";
    var GM = "https://share.google/Jlp2IjomZLla08vaa";
    var css = ".tnhft{background:#0a2f2c;color:#F4ECD6;padding:34px 0 10px;margin-top:30px;border-top:2px solid #C1A374;font-family:'Be Vietnam Pro',system-ui,sans-serif}" +
      ".tnhft *{box-sizing:border-box}.tnhft-in{max-width:1120px;margin:0 auto;padding:0 20px}" +
      ".tnhft h3{font:700 .95rem/1.3 'Be Vietnam Pro',system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#E3C97A;text-align:center;margin:0 0 14px}" +
      ".tnhft-g{display:grid;grid-template-columns:1.1fr 1fr .9fr;gap:26px;align-items:start}" +
      ".tnhft iframe{width:100%;height:340px;border:0;border-radius:12px;background:#fff;display:block}.tnhft-fb iframe{max-width:340px;margin:0 auto}" +
      ".tnhft-l{text-align:center}.tnhft-i{display:flex;justify-content:center;gap:12px;margin:2px 0 16px}" +
      ".tnhft-i a{width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font:800 .8rem 'Be Vietnam Pro',system-ui,sans-serif;text-decoration:none}" +
      ".tnhft-i svg{width:26px;height:26px;fill:#fff}.tnhft-i .fb{background:#1877f2}.tnhft-i .yt{background:#e62117}.tnhft-i .zl{background:#0068ff}.tnhft-i .mp{background:#34a853}" +
      ".tnhft-l p{font-size:.88rem;opacity:.92;margin:0 0 10px;line-height:1.55}" +
      ".tnhft-b{display:flex;align-items:center;justify-content:center;border-radius:999px;padding:11px 16px;margin:6px 0;font:600 .92rem 'Be Vietnam Pro',system-ui,sans-serif;text-decoration:none;border:1.5px solid #C1A374}" +
      ".tnhft-b.g{background:linear-gradient(135deg,#C1A374,#E3C97A);color:#072E2C}.tnhft-b.o{color:#E3C97A}" +
      "@media(max-width:900px){.tnhft-g{grid-template-columns:1fr}.tnhft iframe{height:300px}}";
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var s = document.createElement("section"); s.className = "tnhft ft-connect"; s.setAttribute("aria-label", "Kết nối The Nest House");
    s.innerHTML = "<div class='tnhft-in'><div class='tnhft-g'>" +
      "<div><h3>Cửa hàng The Nest House</h3><iframe data-src='" + MAP + "' title='Bản đồ cửa hàng The Nest House' referrerpolicy='no-referrer-when-downgrade'></iframe></div>" +
      "<div class='tnhft-fb'><h3>Fanpage Facebook</h3><iframe data-src='" + FB + "' title='Fanpage Facebook The Nest House' scrolling='no' allow='encrypted-media'></iframe></div>" +
      "<div class='tnhft-l'><h3>Mạng liên kết</h3><div class='tnhft-i'>" +
      "<a class='fb' href='https://www.facebook.com/thenesthouse' target='_blank' rel='noopener' aria-label='Facebook'><svg viewBox='0 0 24 24'><path d='M13.5 21v-8h2.7l.5-3.2h-3.2V7.7c0-.9.4-1.7 1.8-1.7h1.5V3.2S15.5 3 14.3 3C11.8 3 10.2 4.5 10.2 7.3v2.5H7.5V13h2.7v8z'/></svg></a>" +
      "<a class='yt' href='https://www.youtube.com/@nhatrangyensaonguyenchat2932' target='_blank' rel='noopener' aria-label='YouTube'><svg viewBox='0 0 24 24'><path d='M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2C2 8.8 2 12 2 12s0 3.2.4 4.8a2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8c.4-1.6.4-4.8.4-4.8s0-3.2-.4-4.8zM10 15V9l5.2 3z'/></svg></a>" +
      "<a class='zl' href='https://zalo.me/0969850153' target='_blank' rel='noopener' aria-label='Zalo'>Zalo</a>" +
      "<a class='mp' href='" + GM + "' target='_blank' rel='noopener' aria-label='Google Maps'><svg viewBox='0 0 24 24'><path d='M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z'/></svg></a></div>" +
      "<p>Kios A126, Tầng 2, TTTM Tops Market, 685 Âu Cơ, P. Tân Phú, TP.HCM · 08:30–18:00 mỗi ngày</p>" +
      "<a class='tnhft-b g' href='" + GM + "' target='_blank' rel='noopener'>📍 Chỉ đường &amp; xem đánh giá</a>" +
      "<a class='tnhft-b o' href='https://zalo.me/0969850153' target='_blank' rel='noopener'>💬 Nhắn Zalo 0969.850.153</a></div></div></div>";
    ft.parentNode.insertBefore(s, ft);
    var frames = [].slice.call(s.querySelectorAll("iframe[data-src]"));
    function load() { frames.forEach(function (f) { if (!f.src) f.src = f.getAttribute("data-src"); }); }
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (e) { if (e[0].isIntersecting) { load(); io.disconnect(); } }, { rootMargin: "500px" });
      io.observe(s);
    } else { load(); }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go); else go();
})();
