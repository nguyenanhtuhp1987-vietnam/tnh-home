/* Trợ lý chat The Nest House — widget nổi góc phải, gọi Worker tnh-chatbot.
   Gắn vào trang: <script src="/assets/tnh-chat.js" defer></script>
   Nguồn: vault 09-marketing/website/assets/tnh-chat.js → copy sang repo tnh-home/assets/. */
(function () {
  if (window.__tnhChat) return;
  window.__tnhChat = 1;
  // Giỏ hàng (nút "🛒 Giỏ hàng" + khối Đặt mua ở trang sản phẩm) — nạp kèm để mọi trang có, không phải sửa từng trang
  if (!window.__tnhCart && !document.querySelector('script[src*="tnh-cart.js"]')) {
    var cs = document.createElement("script"); cs.src = "/assets/tnh-cart.js"; cs.defer = true; document.head.appendChild(cs);
  }
  var API = "https://tnh-chatbot.telegram-duyet-worker.workers.dev/chat";
  var ZALO = "https://zalo.me/0969850153";
  var KEY = "tnh_chat_v1";
  var HELLO = "Dạ, em là trợ lý của The Nest House. Anh/chị cần em tư vấn chọn yến, báo giá hay hướng dẫn cách chưng ạ?";
  var CHIPS = ["Bảng giá yến sào", "Chọn quà biếu bố mẹ", "Cách chưng yến", "Đặt hàng thế nào?"];

  var st = load();
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (s && s.sid && Date.now() - (s.at || 0) < 7 * 864e5) return s;
    } catch (e) {}
    return { sid: uuid(), msgs: [], at: Date.now() };
  }
  function save() {
    st.at = Date.now();
    st.msgs = st.msgs.slice(-40);
    try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {}
  }
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0;
      return (c === "x" ? r : (r & 3) | 8).toString(16);
    });
  }
  function ga(ev, p) { try { if (typeof gtag === "function") gtag("event", ev, p || {}); } catch (e) {} }

  var css =
    ".tc-btn{position:fixed;right:20px;bottom:20px;z-index:9998;display:flex;align-items:center;gap:8px;background:#0E3B33;color:#F4ECD6;border:1px solid #C1A374;border-radius:999px;padding:12px 18px;font:600 15px/1 'Be Vietnam Pro',system-ui,sans-serif;box-shadow:0 8px 22px rgba(0,0,0,.28);cursor:pointer}" +
    ".tc-btn:hover{background:#072E2C}.tc-btn .d{width:8px;height:8px;border-radius:50%;background:#E3C97A}" +
    ".tc-box{position:fixed;right:20px;bottom:20px;z-index:9999;width:370px;max-width:calc(100vw - 32px);height:560px;max-height:calc(100vh - 40px);display:none;flex-direction:column;background:#FFFDF7;border-radius:16px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.32);font:15px/1.5 'Be Vietnam Pro',system-ui,sans-serif;color:#1d2a27}" +
    ".tc-box.open{display:flex}" +
    ".tc-hd{background:#0E3B33;color:#F4ECD6;padding:12px 14px;display:flex;align-items:center;gap:10px}" +
    ".tc-hd b{font-family:'Playfair Display',Georgia,serif;font-size:17px;color:#E3C97A;display:block}.tc-hd small{opacity:.85;font-size:12px}" +
    ".tc-x{margin-left:auto;background:none;border:0;color:#F4ECD6;font-size:24px;line-height:1;cursor:pointer;padding:4px 6px}" +
    ".tc-body{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:#F8F3E6}" +
    ".tc-m{max-width:86%;padding:9px 12px;border-radius:14px;white-space:normal;word-wrap:break-word}" +
    ".tc-m.b{background:#fff;border:1px solid #eadfc4;align-self:flex-start;border-bottom-left-radius:4px}" +
    ".tc-m.u{background:#0E3B33;color:#F4ECD6;align-self:flex-end;border-bottom-right-radius:4px}" +
    ".tc-m a{color:#0E3B33;font-weight:600;text-decoration:underline}.tc-m.u a{color:#E3C97A}" +
    ".tc-qr{padding:6px}.tc-qr img{display:block;width:220px;max-width:100%;border-radius:8px}" +
    ".tc-m.t{color:#7a6c4f;font-style:italic;background:none;border:0;padding:2px 4px}" +
    ".tc-chips{display:flex;flex-wrap:wrap;gap:6px}.tc-chips button{background:#fff;border:1px solid #C1A374;color:#0E3B33;border-radius:999px;padding:6px 11px;font:500 13px 'Be Vietnam Pro',system-ui,sans-serif;cursor:pointer}" +
    ".tc-zalo{display:block;margin:0 14px 8px;text-align:center;background:#0068FF;color:#fff;border-radius:10px;padding:9px;font-weight:600;text-decoration:none;font-size:14px}" +
    ".tc-ft{display:flex;gap:8px;padding:10px 12px;border-top:1px solid #eadfc4;background:#fff}" +
    ".tc-ft textarea{flex:1;resize:none;border:1px solid #d9cba8;border-radius:10px;padding:9px 10px;font:15px/1.4 'Be Vietnam Pro',system-ui,sans-serif;max-height:96px;outline:none}" +
    ".tc-ft textarea:focus{border-color:#0E3B33}" +
    ".tc-ft button{background:#C1A374;color:#0E3B33;border:0;border-radius:10px;padding:0 14px;font-weight:700;cursor:pointer}.tc-ft button:disabled{opacity:.5}" +
    ".tc-note{font-size:11px;color:#8a7d60;text-align:center;padding:0 12px 8px;background:#fff}" +
    "@media(max-width:480px){.tc-box{right:16px;bottom:16px;height:calc(100vh - 32px)}.tc-btn{right:16px}.tc-ft textarea{font-size:16px}}" +
    // cụm nút Zalo/gọi nổi tự thêm (giống hệt trang chủ) cho trang chưa có
    ".tc-fz{position:fixed;right:20px;bottom:20px;z-index:60;display:flex;flex-direction:column;gap:10px}" +
    ".tc-fz a{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.35rem;text-decoration:none;box-shadow:0 8px 22px rgba(0,0,0,.3)}" +
    ".tc-fz .fz{background:#0068ff;color:#fff;font:800 .8rem 'Be Vietnam Pro',system-ui,sans-serif}" +
    ".tc-fz .fp{background:linear-gradient(135deg,#C1A374,#E3C97A);color:#072E2C}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var btn = el("button", "tc-btn", '<span class="d"></span>Hỏi trợ lý');
  btn.type = "button";
  btn.setAttribute("aria-label", "Mở khung chat tư vấn");
  var box = el("div", "tc-box");
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-label", "Trợ lý The Nest House");
  box.innerHTML =
    '<div class="tc-hd"><div><b>The Nest House</b><small>Trợ lý tư vấn · trả lời trong vài giây</small></div><button class="tc-x" type="button" aria-label="Đóng">×</button></div>' +
    '<div class="tc-body"></div>' +
    '<a class="tc-zalo" href="' + ZALO + '" target="_blank" rel="noopener">💬 Nhắn Zalo nhân viên · 0969.850.153</a>' +
    '<div class="tc-ft"><textarea rows="1" maxlength="600" placeholder="Nhập câu hỏi…"></textarea><button type="button">Gửi</button></div>' +
    '<div class="tc-note">Trợ lý AI trả lời chính xác các thông tin về giá, thông tin sản phẩm, thời gian bảo hành, giao hàng.<br>Quý khách muốn được hỗ trợ gấp, yêu cầu đặc biệt liên hệ nhân viên qua Zalo ở trên.</div>';
  document.body.appendChild(btn);
  document.body.appendChild(box);

  // Trang chưa có nút Zalo/gọi nổi (bài cẩm nang, trang sản phẩm, chính sách…) → tự thêm cho giống trang chủ
  // (CEO 04/10/2026). Lượt bấm vẫn được GA4 đếm click_zalo / click_call qua bộ nghe click sẵn trên mỗi trang.
  if (!document.querySelector(".float-zalo")) {
    document.body.appendChild(el("div", "float-zalo tc-fz",
      '<a class="fz" href="' + ZALO + '" target="_blank" rel="noopener" title="Nhắn Zalo">Zalo</a>' +
      '<a class="fp" href="tel:0969850153" title="Gọi hotline">☎</a>'));
  }

  // Trang có sẵn nút Zalo/gọi nổi góc phải → đặt nút chat lên trên cụm đó
  var fz = document.querySelector(".float-zalo");
  if (fz) btn.style.bottom = 20 + fz.offsetHeight + 12 + "px";

  var body = box.querySelector(".tc-body");
  var ta = box.querySelector("textarea");
  var send = box.querySelector(".tc-ft button");
  var busy = false;

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    e.className = cls;
    if (html) e.innerHTML = html;
    return e;
  }
  function fmt(t) {
    var s = String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    s = s.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    s = s.replace(/(https?:\/\/[^\s<)]+|(?:[a-z]+\.)?thenesthouse\.com\.vn[^\s<)]*)/g, function (u) {
      var tail = u.match(/[.,;:!?]+$/);
      tail = tail ? tail[0] : "";
      u = u.slice(0, u.length - tail.length);
      var href = /^https?:/.test(u) ? u : "https://" + u;
      return '<a href="' + href + '" target="_blank" rel="noopener">' + u + "</a>" + tail;
    });
    s = s.replace(/\b0969[.\s]?850[.\s]?153\b/g, '<a href="' + ZALO + '" target="_blank" rel="noopener">$&</a>');
    return s.replace(/\n/g, "<br>");
  }
  function add(role, text, keep) {
    var m;
    if (role === "q") {
      // Mã VietQR chuyển khoản do máy chủ tạo (chỉ nhận ảnh từ img.vietqr.io)
      if (String(text).indexOf("https://img.vietqr.io/") !== 0) return null;
      m = el("div", "tc-m b tc-qr");
      var img = document.createElement("img");
      img.src = text;
      img.alt = "Mã QR chuyển khoản";
      img.onload = function () { body.scrollTop = body.scrollHeight; };
      m.appendChild(img);
    } else m = el("div", "tc-m " + role, fmt(text));
    body.appendChild(m);
    body.scrollTop = body.scrollHeight;
    if (keep !== false) { st.msgs.push([role, text]); save(); }
    return m;
  }
  function chips() {
    var c = el("div", "tc-chips");
    CHIPS.forEach(function (t) {
      var b = el("button", "", t);
      b.type = "button";
      b.onclick = function () { c.remove(); ask(t); };
      c.appendChild(b);
    });
    body.appendChild(c);
  }
  function render() {
    body.innerHTML = "";
    add("b", HELLO, false);
    st.msgs.forEach(function (m) { add(m[0], m[1], false); });
    if (!st.msgs.length) chips();
  }

  function ask(text) {
    text = String(text || "").trim();
    if (!text || busy) return;
    busy = true;
    send.disabled = true;
    var c = body.querySelector(".tc-chips");
    if (c) c.remove();
    add("u", text);
    ga("chat_message", { page_path: location.pathname });
    var typing = add("t", "Em đang trả lời…", false);
    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sid: st.sid, page: location.host + location.pathname, message: text }),
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        typing.remove();
        if (d && d.ok) {
          add("b", d.reply);
          if (d.qr) add("q", d.qr);
          if (d.handoff) ga("chat_handoff", { page_path: location.pathname });
        } else {
          var msg = {
            rate: "Dạ anh/chị nhắn hơi nhanh, mình đợi chút rồi hỏi tiếp giúp em nhé.",
            limit: "Dạ cuộc trò chuyện đã dài, anh/chị nhắn Zalo 0969.850.153 để nhân viên tư vấn tiếp giúp em nhé.",
          }[d && d.error] || "Dạ hệ thống đang bận, anh/chị nhắn Zalo 0969.850.153 để được tư vấn ngay nhé.";
          add("b", msg, false);
        }
      })
      .catch(function () {
        typing.remove();
        add("b", "Dạ mạng đang chập chờn, anh/chị thử lại hoặc nhắn Zalo 0969.850.153 giúp em nhé.", false);
      })
      .then(function () {
        busy = false;
        send.disabled = false;
      });
  }

  btn.onclick = function () {
    box.classList.add("open");
    btn.style.display = "none";
    render();
    ga("chat_open", { page_path: location.pathname });
    setTimeout(function () { ta.focus(); }, 50);
  };
  box.querySelector(".tc-x").onclick = function () {
    box.classList.remove("open");
    btn.style.display = "";
  };
  box.querySelector(".tc-zalo").onclick = function () { ga("chat_zalo", { page_path: location.pathname }); };
  send.onclick = function () { var t = ta.value; ta.value = ""; ask(t); };
  ta.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); send.onclick(); }
  });
})();
