#!/usr/bin/env python3
"""Bộ 8 ảnh mỗi trang sản phẩm (CEO 15/10/2026): ảnh chính + 8 ô ảnh nhỏ bấm đổi ảnh, mỗi ảnh một góc nhìn/bố cục.

Nguồn chọn ảnh: _scripts/pdp_anh_8.json — {trang: {slug, items: [[nguồn, alt], ...8]}}.
  nguồn "asset:<tên>"  = ảnh đã có trong assets/ (giữ nguyên)
  nguồn "file:<đường dẫn>" = ảnh CEO chỉ định thẳng
  nguồn "<bảng>:<số>"  = ảnh gốc trong kho ảnh của CEO, đã chọn bằng mắt trên bảng ảnh đánh số (đường dẫn trong --nguon <thư mục chứa <bảng>.json>)
Chạy:  python3 _scripts/pdp_gallery.py --nguon <thư mục bảng ảnh>   (chép ảnh mới vào assets/sp/, rồi chạy toi_uu_toc_do.py)
       python3 _scripts/pdp_gallery.py --html-only [<thư mục web vault>]   (chỉ sửa HTML, ảnh đã có)
Ảnh .jpg trung gian xoá sau khi sinh .webp (web chỉ dùng .webp; og:image vẫn là ảnh .jpg cũ của trang). Chạy lại an toàn: thay nguyên khối <figure class="pdp-img ...">…</figure> trong section.pdp.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SP = ROOT / "assets/sp"
CFG = json.loads((ROOT / "_scripts/pdp_anh_8.json").read_text(encoding="utf-8"))
JS = """<script>/* bộ ảnh trang sản phẩm: bấm ô nhỏ → đổi ảnh chính */
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.gal-th button');if(!b)return;var g=b.closest('.pdp-gal'),m=g.querySelector('.gal-main');
m.src=b.dataset.src;m.srcset=b.dataset.srcset||'';m.alt=b.dataset.alt;g.querySelector('figcaption').textContent=b.dataset.alt;
g.querySelectorAll('.gal-th button').forEach(function(x){x.classList.toggle('on',x===b)});
if(typeof gtag==='function')gtag('event','pdp_gallery',{index:b.dataset.i,page_path:location.pathname});});</script>
"""
CSS = """
  /* bộ 8 ảnh (15/10/2026) */
  .pdp-gal{min-width:0;max-width:100%}.pdp-gal figcaption{min-height:1.2em}
  .gal-th{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin-top:8px}
  .gal-th button{padding:0;border:2px solid transparent;border-radius:9px;background:none;cursor:pointer;overflow:hidden;aspect-ratio:1/1}
  .gal-th button.on{border-color:var(--gold)}
  .gal-th img{width:100%;height:100%;object-fit:cover;display:block;border-radius:7px;border:0!important;aspect-ratio:auto!important}
  @media(max-width:900px){.pdp-grid{grid-template-columns:minmax(0,1fr)!important}.gal-th{grid-template-columns:repeat(8,64px);overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}}
"""


def src_path(ref, nguon):
    if ref.startswith("asset:"):
        return None
    if ref.startswith("file:"):  # CEO chỉ định thẳng đường dẫn ảnh
        return Path(ref[5:])
    sheet, i = ref.split(":")
    return Path(json.loads((Path(nguon) / f"{sheet}.json").read_text())[i])


def copy_images(nguon):
    from PIL import Image, ImageOps
    SP.mkdir(exist_ok=True)
    for page, d in CFG.items():
        for k, (ref, alt) in enumerate(d["items"], 1):
            if ref.startswith("asset:"):
                continue
            out = SP / f"{d['slug']}-{k:02d}.jpg"
            if out.exists() or out.with_suffix(".webp").exists():
                continue
            p = src_path(ref, nguon)
            if p.suffix.lower() == ".heic":
                import subprocess, tempfile
                tmp = Path(tempfile.mkdtemp()) / "x.jpg"
                subprocess.run(["sips", "-s", "format", "jpeg", str(p), "--out", str(tmp)], capture_output=True, check=True); p = tmp
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            if im.width > 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(out, quality=86, optimize=True)
            print("  +", out.relative_to(ROOT), "←", p.name)


def web(ref, slug, k):
    if ref.startswith("asset:"):
        base = "/assets/" + ref[6:]
    else:
        base = f"/assets/sp/{slug}-{k:02d}"
    f = ROOT / (base.lstrip("/") + ".webp")
    vs = [(w, f"{base}-{w}.webp") for w in (480, 960) if (ROOT / f"{base.lstrip('/')}-{w}.webp").exists()]
    from PIL import Image
    W, H = Image.open(f).size
    srcset = ", ".join(f"{u} {w}w" for w, u in vs) + (f", {base}.webp {W}w" if vs else "")
    thumb = vs[0][1] if vs else base + ".webp"
    return base + ".webp", srcset, W, H, thumb


def gallery(page, d):
    imgs = [web(ref, d["slug"], k) for k, (ref, alt) in enumerate(d["items"], 1)]
    alts = [alt for ref, alt in d["items"]]
    s0, ss0, W, H, _ = imgs[0]
    btns = []
    for i, ((s, ss, w, h, t), a) in enumerate(zip(imgs, alts)):
        on = ' class="on"' if i == 0 else ""
        btns.append(f'<button type="button"{on} data-i="{i+1}" data-src="{s}" data-srcset="{ss}" data-alt="{a}" aria-label="Ảnh {i+1}: {a}"><img src="{t}" alt="" loading="lazy" width="120" height="120"></button>')
    th = "".join(btns)
    return (f'<figure class="pdp-img pdp-gal"><img class="gal-main" srcset="{ss0}" sizes="(max-width:640px) 100vw, 50vw" fetchpriority="high" width="{W}" height="{H}" src="{s0}" alt="{alts[0]}">'
            f'<figcaption>{alts[0]}</figcaption><div class="gal-th">{th}</div></figure>')


def apply_html(root):
    n = 0
    for page, d in CFG.items():
        p = Path(root) / "yen-sao" / page / "index.html"
        s = p.read_text(encoding="utf-8")
        sec = s.find('<section class="pdp"')
        a = s.find("<figure", sec); b = s.find("</figure>", a) + 9
        assert sec > 0 and a > 0, page
        x = s[:a] + gallery(page, d) + s[b:]
        if "/* bộ 8 ảnh" not in x:
            he = x.find("</head>"); st = x.rfind("</style>", 0, he); x = x[:st] + CSS + x[st:]
        if "bộ ảnh trang sản phẩm" not in x:
            x = x.replace("</body>", JS + "</body>", 1)
        if x != s:
            p.write_text(x, encoding="utf-8"); n += 1
    print(n, "trang có bộ 8 ảnh")


if __name__ == "__main__":
    if "--nguon" in sys.argv:
        copy_images(sys.argv[sys.argv.index("--nguon") + 1])
    else:
        apply_html(next((a for a in sys.argv[1:] if not a.startswith("--")), ROOT))
