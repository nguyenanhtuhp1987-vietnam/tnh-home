/* Hiệu ứng trang sản phẩm (bản thử 18/10/2026) — không thư viện, tắt hẳn khi khách bật "giảm chuyển động".
   1 bụi vàng + chữ tiêu đề hiện dần · 2 ảnh nghiêng 3D theo chuột + ánh sáng lướt · 3 kính soi sợi yến
   4 thanh tiến độ đọc · 5 khối hiện dần khi cuộn · 6 số đánh giá tự đếm, thanh sao tự chạy · 7 viền vàng thẻ quà, nút mua loé sáng */
(function () {
  if (!window.matchMedia || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var d = document, fine = matchMedia('(hover:hover) and (pointer:fine)').matches;

  var css = d.createElement('style'); css.setAttribute('data-tnh', 'wow');
  css.textContent = [
    '.wow-bar{position:fixed;top:0;left:0;height:3px;width:100%;transform-origin:0 50%;transform:scaleX(0);z-index:9999;background:linear-gradient(90deg,#C1A374,#E3C97A,#fff6d8,#C1A374);pointer-events:none}',
    '.head,section.hero{position:relative;overflow:hidden}.head .container,section.hero .container{position:relative;z-index:1}',
    'section.hero .container>div:first-child>*{opacity:0;transform:translateY(18px);animation:wowUp .8s cubic-bezier(.2,.7,.2,1) forwards}',
    'section.hero h1 em{background:linear-gradient(100deg,#E3C97A 40%,#fff6d8 50%,#E3C97A 60%) 120% 0/250% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:wowSweep 2.4s 1.2s ease-in-out 1 forwards}',
    '.hero-img{perspective:1100px}.hero-img img{transition:transform .3s ease-out}',
    '.card{transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}',
    '@media (hover:hover){.card:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(7,46,44,.16)}}',
    '.wow-dust{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}',
    '.head h1 .w{display:inline-block;opacity:0;transform:translateY(.6em);animation:wowUp .7s cubic-bezier(.2,.7,.2,1) forwards}',
    '.head h1.wow-shine{background:linear-gradient(100deg,#fff 42%,#E3C97A 48%,#fff6d8 50%,#E3C97A 52%,#fff 58%) 120% 0/250% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:wowSweep 2.2s .2s ease-in-out 1 forwards}',
    '@keyframes wowUp{to{opacity:1;transform:none}}',
    '@keyframes wowSweep{to{background-position:-20% 0}}',
    '.pdp-gal{perspective:1100px}',
    '.pdp-gal .gal-wrap{position:relative;transform-style:preserve-3d;transition:transform .25s ease-out;border-radius:inherit;will-change:transform}',
    '.pdp-gal .gal-glare{position:absolute;inset:0;pointer-events:none;border-radius:inherit;opacity:0;transition:opacity .3s;background:radial-gradient(circle at var(--gx,50%) var(--gy,50%),rgba(255,246,216,.45),transparent 55%);mix-blend-mode:soft-light}',
    '.pdp-gal .gal-wrap:hover .gal-glare{opacity:1}',
    '.pdp-gal .gal-main{transition:opacity .35s ease,transform .5s ease}',
    '.pdp-gal .gal-main.wow-swap{opacity:0;transform:scale(.97)}',
    '.wow-loupe{position:absolute;width:170px;height:170px;border-radius:50%;pointer-events:none;border:3px solid #E3C97A;box-shadow:0 10px 30px rgba(7,46,44,.35),inset 0 0 0 1px rgba(255,255,255,.6);background-repeat:no-repeat;background-color:#faf7ee;opacity:0;transform:scale(.6);transition:opacity .2s,transform .2s;z-index:3}',
    '.wow-loupe.on{opacity:1;transform:scale(1)}',
    '.wow-hint{position:absolute;left:12px;bottom:12px;z-index:2;font:600 .74rem/1 var(--sans,sans-serif);color:#072E2C;background:rgba(244,236,214,.92);padding:7px 10px;border-radius:99px;box-shadow:0 2px 8px rgba(0,0,0,.12);pointer-events:none;transition:opacity .3s}',
    '.wow-in{opacity:0;transform:translateY(28px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1)}',
    '.wow-in.vis{opacity:1;transform:none}',
    '.rv-bar b{transition:width 1.4s cubic-bezier(.2,.7,.2,1)}',
    '.offer-card{position:relative;isolation:isolate;border-color:transparent!important;border-style:solid!important}',
    '.offer-card::before{content:"";position:absolute;inset:-2px;border-radius:inherit;z-index:-1;background:conic-gradient(from var(--wa,0deg),#C1A374,#fff6d8,#E3C97A,#C1A374 40%,#C1A374);animation:wowSpin 6s linear infinite}',
    '.offer-card::after{content:"";position:absolute;inset:0;border-radius:inherit;z-index:-1;background:inherit}',
    '@property --wa{syntax:"<angle>";inherits:false;initial-value:0deg}',
    '@keyframes wowSpin{to{--wa:360deg}}',
    '.tnhk-btn.pri,.tnhk-now{position:relative;overflow:hidden}',
    '.tnhk-btn.pri::after,.tnhk-now::after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-20deg);animation:wowGlint 4.5s 2s ease-in-out infinite}',
    '@keyframes wowGlint{0%,70%{left:-60%}90%,100%{left:130%}}'
  ].join('\n');
  d.head.appendChild(css);

  /* 4 thanh tiến độ đọc */
  var bar = d.createElement('div'); bar.className = 'wow-bar'; d.body.appendChild(bar);
  var ticking = false;
  addEventListener('scroll', function () {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      var h = d.documentElement.scrollHeight - innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, scrollY / h) : 0) + ')'; ticking = false;
    });
  }, { passive: true });

  /* 1 tiêu đề hiện từng chữ + bụi vàng */
  var head = d.querySelector('.head') || d.querySelector('section.hero'), h1 = head && head.querySelector('h1');
  if (h1 && !h1.children.length) {
    var words = h1.textContent.trim().split(/\s+/);
    h1.setAttribute('aria-label', h1.textContent.trim());
    h1.innerHTML = words.map(function (w, i) { return '<span class="w" aria-hidden="true" style="animation-delay:' + (i * 45) + 'ms">' + w.replace(/</g, '&lt;') + '</span>'; }).join(' ');
    var txt = h1.getAttribute('aria-label');
    setTimeout(function () { h1.textContent = txt; h1.removeAttribute('aria-label'); h1.classList.add('wow-shine'); }, words.length * 45 + 800);
  }
  if (head && head.matches('section.hero')) {
    head.querySelectorAll('.container>div:first-child>*').forEach(function (el, i) { el.style.animationDelay = (i * 140) + 'ms'; });
    var hi = head.querySelector('.hero-img img');
    if (hi && fine) {
      head.querySelector('.hero-img').addEventListener('mousemove', function (e) { var r = hi.getBoundingClientRect(); hi.style.transform = 'rotateX(' + ((e.clientY - r.top) / r.height - .5) * -6 + 'deg) rotateY(' + ((e.clientX - r.left) / r.width - .5) * 8 + 'deg)'; });
      head.querySelector('.hero-img').addEventListener('mouseleave', function () { hi.style.transform = ''; });
    }
  }
  if (head) {
    var cv = d.createElement('canvas'); cv.className = 'wow-dust'; cv.setAttribute('aria-hidden', 'true');
    head.insertBefore(cv, head.firstChild);
    var cx = cv.getContext('2d'), P = [], W = 0, H = 0, dpr = Math.min(2, devicePixelRatio || 1), run = true;
    function size() { W = head.clientWidth; H = head.clientHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    size(); addEventListener('resize', size);
    var n = W < 640 ? 22 : 46;
    for (var i = 0; i < n; i++) P.push({ x: Math.random() * W, y: Math.random() * H, r: .6 + Math.random() * 1.8, v: .12 + Math.random() * .35, a: Math.random() * 6.28, t: Math.random() * 6.28 });
    function draw() {
      if (!run) return;
      cx.clearRect(0, 0, W, H);
      for (var i = 0; i < P.length; i++) {
        var p = P[i]; p.y -= p.v; p.a += .01; p.t += .04; p.x += Math.sin(p.a) * .25;
        if (p.y < -4) { p.y = H + 4; p.x = Math.random() * W; }
        var g = .35 + .45 * Math.abs(Math.sin(p.t));
        cx.beginPath(); cx.arc(p.x, p.y, p.r, 0, 6.28);
        cx.fillStyle = 'rgba(227,201,122,' + g + ')'; cx.shadowColor = 'rgba(227,201,122,.9)'; cx.shadowBlur = 6; cx.fill();
      }
      requestAnimationFrame(draw);
    }
    new IntersectionObserver(function (e) { var was = run; run = e[0].isIntersecting; if (run && !was) requestAnimationFrame(draw); }).observe(head);
    requestAnimationFrame(draw);
  }

  /* 2 + 3 ảnh nghiêng 3D, ánh sáng lướt, kính soi sợi yến */
  var gal = d.querySelector('.pdp-gal'), img = gal && gal.querySelector('.gal-main');
  if (img) {
    var wrap = d.createElement('div'); wrap.className = 'gal-wrap';
    img.parentNode.insertBefore(wrap, img); wrap.appendChild(img);
    var glare = d.createElement('div'); glare.className = 'gal-glare'; wrap.appendChild(glare);
    var lp = d.createElement('div'); lp.className = 'wow-loupe'; lp.setAttribute('aria-hidden', 'true'); wrap.appendChild(lp);
    var hint = d.createElement('div'); hint.className = 'wow-hint'; hint.textContent = fine ? '🔍 Rê chuột để soi sợi yến' : '🔍 Giữ trên ảnh để soi sợi yến'; wrap.appendChild(hint);
    var Z = 2.6;
    function big() { return img.src || img.currentSrc; }
    function at(x, y) {
      var r = wrap.getBoundingClientRect(), px = x - r.left, py = y - r.top;
      if (px < 0 || py < 0 || px > r.width || py > r.height) { lp.classList.remove('on'); return; }
      /* ảnh object-fit:contain → tính khung ảnh thật trong ô */
      var iw = img.naturalWidth || r.width, ih = img.naturalHeight || r.height, s = Math.min(r.width / iw, r.height / ih),
          dw = iw * s, dh = ih * s, ox = (r.width - dw) / 2, oy = (r.height - dh) / 2;
      lp.style.left = (px - 85) + 'px'; lp.style.top = (py - (fine ? 85 : 190)) + 'px';
      lp.style.backgroundImage = 'url("' + big() + '")';
      lp.style.backgroundSize = (dw * Z) + 'px ' + (dh * Z) + 'px';
      lp.style.backgroundPosition = (85 - (px - ox) * Z) + 'px ' + ((fine ? 85 : 85) - (py - oy) * Z) + 'px';
      lp.classList.add('on'); hint.style.opacity = 0;
      if (fine) {
        var rx = (py / r.height - .5) * -7, ry = (px / r.width - .5) * 9;
        wrap.style.transform = 'rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
        glare.style.setProperty('--gx', (px / r.width * 100) + '%'); glare.style.setProperty('--gy', (py / r.height * 100) + '%');
      }
    }
    function off() { lp.classList.remove('on'); wrap.style.transform = ''; }
    if (fine) {
      wrap.addEventListener('mousemove', function (e) { at(e.clientX, e.clientY); });
      wrap.addEventListener('mouseleave', off);
    } else {
      var hold;
      wrap.addEventListener('touchstart', function (e) { var t = e.touches[0]; hold = setTimeout(function () { at(t.clientX, t.clientY); }, 220); }, { passive: true });
      wrap.addEventListener('touchmove', function (e) { if (lp.classList.contains('on')) { e.preventDefault(); var t = e.touches[0]; at(t.clientX, t.clientY); } else clearTimeout(hold); }, { passive: false });
      wrap.addEventListener('touchend', function () { clearTimeout(hold); off(); });
    }
    /* đổi ảnh mờ dần thay vì nhảy */
    d.addEventListener('click', function (e) {
      if (!(e.target.closest && e.target.closest('.gal-th button'))) return;
      img.classList.add('wow-swap');
      var done = function () { img.classList.remove('wow-swap'); };
      if (img.complete) setTimeout(done, 60); img.addEventListener('load', done, { once: true });
    }, true);
  }

  /* 5 hiện dần khi cuộn — chỉ khối nằm dưới màn hình đầu, để không nháy và không làm xô bố cục */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  var sel = '.grid > .card, main h2, article h2, section > .container > h2, .rv-main, .rv-quotes > *, .rv-tile, .faq details, table, figure:not(.pdp-gal), .ft-connect';
  d.querySelectorAll(sel).forEach(function (el, i) {
    if (el.getBoundingClientRect().top < innerHeight) return;
    el.classList.add('wow-in'); el.style.transitionDelay = (i % 3) * 90 + 'ms'; io.observe(el);
  });

  /* 6 số đánh giá tự đếm + thanh sao chạy */
  var rv = d.querySelector('.rv-main');
  if (rv) {
    var bars = rv.querySelectorAll('.rv-bar b'), ws = [];
    bars.forEach(function (b) { ws.push(b.style.width); b.style.width = '0'; });
    var bigEl = rv.querySelector('.big'), target = bigEl && parseFloat(bigEl.textContent.replace(',', '.'));
    var cnt = rv.querySelector('small'), m = cnt && cnt.textContent.match(/^([\d.]+)/), N = m && parseInt(m[1].replace(/\./g, ''), 10);
    new IntersectionObserver(function (es, o) {
      if (!es[0].isIntersecting) return; o.disconnect();
      bars.forEach(function (b, i) { setTimeout(function () { b.style.width = ws[i]; }, 120 + i * 110); });
      var t0 = performance.now(), dur = 1500, rest = cnt && cnt.textContent.slice(m[1].length);
      (function step(t) {
        var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        if (target) bigEl.textContent = (target * e).toFixed(1).replace('.', ',');
        if (N) cnt.textContent = Math.round(N * e).toLocaleString('vi-VN') + rest;
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    }, { threshold: .4 }).observe(rv);
  }
})();
