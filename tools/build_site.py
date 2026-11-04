# -*- coding: utf-8 -*-
"""
海外压缩机英文站生成器
用法： python tools/build_site.py
新增/修改型号只需编辑 data/models.json，然后重跑本脚本，整站自动重建。
"""
import json
import pathlib
import datetime

BASE = pathlib.Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "models.json"
SITE = BASE / "site"
DOCS = BASE / "docs"
TODAY = datetime.date.today().isoformat()

CSS = r"""
:root{
  --bg:#f5f7fa; --surface:#ffffff; --surface-2:#fafbfd; --ink:#101a2b; --ink-2:#3d4d63; --muted:#6b7b92;
  --line:#e4e9f0; --line-2:#d6deea; --brand:#0d3f78; --brand-2:#1a63c4; --accent:#f28c1e; --accent-2:#ffb45c;
  --ok:#0f8a5f; --radius:14px; --radius-sm:9px; --shadow-s:0 1px 2px rgba(16,26,43,.06);
  --shadow-m:0 6px 20px rgba(16,26,43,.08); --shadow-l:0 18px 44px rgba(16,26,43,.12);
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-5:24px; --space-6:32px; --space-7:48px; --space-8:72px;
  --fs-xs:.75rem; --fs-sm:.8125rem; --fs-base:.9375rem; --fs-md:1.0625rem; --fs-lg:1.25rem; --fs-xl:1.5rem;
  --fs-2xl:1.875rem; --fs-3xl:2.375rem; --fs-4xl:3rem;
  --font:'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
  --mono:'JetBrains Mono','SFMono-Regular',Consolas,monospace;
  --ease:cubic-bezier(.16,1,.3,1); --maxw:1180px;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:var(--font);background:var(--bg);color:var(--ink);font-size:var(--fs-base);line-height:1.65;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--brand-2);text-decoration:none;transition:color .18s var(--ease)}
a:hover{color:var(--brand)}
h1,h2,h3,h4{line-height:1.25;margin:0 0 var(--space-4);letter-spacing:-.02em;font-weight:700;color:var(--ink)}
h1{font-size:var(--fs-3xl)} h2{font-size:var(--fs-2xl)} h3{font-size:var(--fs-lg)} h4{font-size:var(--fs-md)}
p{margin:0 0 var(--space-4)}
ul{margin:0 0 var(--space-4);padding-left:1.15rem}
li{margin-bottom:var(--space-2)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--space-5)}
.mono{font-family:var(--mono)}
.muted{color:var(--muted)}
.small{font-size:var(--fs-sm)}
.btn{display:inline-flex;align-items:center;gap:var(--space-2);padding:10px 18px;border-radius:999px;font-size:var(--fs-sm);font-weight:600;border:1px solid transparent;cursor:pointer;transition:transform .18s var(--ease),box-shadow .18s var(--ease),background .18s var(--ease),color .18s var(--ease);white-space:nowrap}
.btn-primary{background:linear-gradient(135deg,var(--brand),var(--brand-2));color:#fff;box-shadow:0 6px 18px rgba(13,63,120,.28)}
.btn-primary:hover{color:#fff;transform:translateY(-2px);box-shadow:0 12px 26px rgba(13,63,120,.34)}
.btn-accent{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#3a2200;box-shadow:0 6px 18px rgba(242,140,30,.3)}
.btn-accent:hover{color:#3a2200;transform:translateY(-2px)}
.btn-ghost{background:transparent;border-color:var(--line-2);color:var(--ink)}
.btn-ghost:hover{background:var(--surface);border-color:var(--brand-2);color:var(--brand)}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.topbar{background:#0c1c31;color:#9fb0c6;font-size:var(--fs-xs)}
.topbar-inner{display:flex;align-items:center;justify-content:space-between;gap:var(--space-4);min-height:38px;flex-wrap:wrap;padding-top:4px;padding-bottom:4px}
.tb-tag{letter-spacing:.02em}
.tb-links{display:flex;align-items:center;gap:var(--space-4);flex-wrap:wrap}
.topbar a{color:#9fb0c6;font-size:var(--fs-xs)}
.topbar a:hover{color:#fff}
.tb-cta{color:var(--accent-2) !important;font-weight:700;letter-spacing:.02em}
.tb-cta:hover{color:#fff !important}
.site-header{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.88);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;gap:var(--space-5);height:68px}
.logo{display:flex;align-items:center;gap:11px;font-weight:800;color:var(--ink);letter-spacing:-.02em;flex:0 0 auto;margin-right:var(--space-3)}
.logo:hover{color:var(--brand)}
.logo-img{height:40px;width:auto;display:block}
.logo-text{font-size:13px;line-height:1.26;font-weight:800;color:var(--ink);max-width:196px;text-wrap:balance}
.logo-mark{width:34px;height:34px;display:grid;place-items:center;background:linear-gradient(135deg,var(--brand),var(--brand-2));border-radius:9px;box-shadow:var(--shadow-s)}
.nav-links{display:flex;gap:2px;margin-left:auto;align-items:center;flex-wrap:wrap}
.nav-links a{padding:8px 11px;border-radius:8px;font-size:var(--fs-sm);font-weight:600;color:var(--ink-2)}
.nav-links a:hover{background:var(--surface-2);color:var(--brand)}
.nav-links a.active{background:rgba(26,99,196,.09);color:var(--brand)}
.nav-links .nav-item{position:relative;display:flex;align-items:center}
.nav-links .nav-item>a{display:inline-flex;align-items:center;gap:6px}
.nav-links .nav-item>a::after{content:"";width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid currentColor;opacity:.55;margin-top:2px}
.nav-links .sub{position:absolute;top:calc(100% + 8px);left:0;min-width:198px;background:var(--surface);border:1px solid var(--line);border-radius:11px;box-shadow:var(--shadow-m);padding:6px;display:none;flex-direction:column;z-index:70}
.nav-links .sub::before{content:"";position:absolute;top:-12px;left:0;right:0;height:12px}
.nav-links .nav-item:hover .sub,.nav-links .nav-item:focus-within .sub{display:flex}
.nav-links .sub a{padding:9px 12px;border-radius:8px}
.nav-toggle{display:none;margin-left:auto;background:none;border:1px solid var(--line-2);border-radius:8px;width:40px;height:36px;cursor:pointer}
.nav-toggle span{display:block;width:18px;height:2px;background:var(--ink);margin:3px auto;border-radius:2px}
.hero{position:relative;overflow:hidden;background:linear-gradient(135deg,#0d3f78 0%,#12497f 45%,#1a63c4 100%);color:#fff}
.hero::after{content:"";position:absolute;inset:0;background:radial-gradient(880px 420px at 84% 12%,rgba(242,140,30,.26),transparent 62%)}
.hero-inner{position:relative;z-index:2;padding:var(--space-8) 0 var(--space-7)}
.hero-brand{display:flex;align-items:center;flex-wrap:wrap;margin-bottom:var(--space-6)}
.hero-brand-name{display:flex;flex-direction:column;gap:6px;min-width:0}
.hero-brand-name .en{font-size:var(--fs-2xl);font-weight:800;letter-spacing:-.02em;line-height:1.1;color:#fff;text-wrap:balance}
.hero-brand-name .desc{font-size:var(--fs-md);font-weight:600;letter-spacing:.01em;color:rgba(255,255,255,.82)}
.hero-brand-name .cn{font-size:var(--fs-sm);font-weight:600;letter-spacing:.22em;color:rgba(255,255,255,.62);margin-top:2px}
.hero-lead{font-size:var(--fs-md);color:rgba(255,255,255,.88);max-width:64ch;margin-bottom:var(--space-6)}
.hero-invite{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:var(--radius);padding:var(--space-5) var(--space-6);max-width:960px;backdrop-filter:blur(3px)}
.hero-invite p{font-size:var(--fs-md);color:#fff;margin-bottom:var(--space-5);max-width:62ch}
.hero-invite-actions{display:flex;align-items:center;gap:var(--space-5);flex-wrap:wrap}
.hero-direct{font-size:var(--fs-sm);color:rgba(255,255,255,.76)}
.hero-direct a{color:#fff;text-decoration:underline;text-decoration-color:rgba(255,255,255,.4);text-underline-offset:3px}
.hero-direct a:hover{color:var(--accent-2)}
.hero-chips{display:flex;gap:var(--space-2);flex-wrap:wrap;padding:0;list-style:none;margin:var(--space-6) 0 0}
.hero-chips li{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);padding:6px 12px;border-radius:999px;font-size:var(--fs-sm);color:#fff;margin:0}
.channel-list{display:flex;flex-direction:column;gap:2px;margin:0;padding:0;list-style:none}
.channel-list li{margin:0;border-bottom:1px dashed var(--line)}
.channel-list li:last-child{border-bottom:0}
.channel-list a,.channel-list span.ch{display:flex;align-items:center;gap:10px;padding:10px 2px;font-size:var(--fs-sm);font-weight:600;color:var(--ink-2)}
.channel-list a:hover{color:var(--brand-2)}
.channel-list .ch-ico{width:30px;height:30px;flex:0 0 auto;display:grid;place-items:center;border-radius:9px;background:rgba(26,99,196,.09);color:var(--brand-2)}
.section{padding:var(--space-8) 0}
.section.tight{padding:var(--space-7) 0}
.section-head{max-width:70ch;margin-bottom:var(--space-6)}
.section-head .eyebrow{display:inline-block;font-size:var(--fs-xs);font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--brand-2);background:rgba(26,99,196,.08);padding:5px 10px;border-radius:6px;margin-bottom:var(--space-3)}
.grid{display:grid;gap:var(--space-5)}
.grid-3{grid-template-columns:repeat(3,1fr)}
.grid-2{grid-template-columns:repeat(2,1fr)}
.grid-4{grid-template-columns:repeat(4,1fr)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:var(--space-5);box-shadow:var(--shadow-s);transition:transform .22s var(--ease),box-shadow .22s var(--ease),border-color .22s var(--ease)}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-m);border-color:var(--line-2)}
.card h3{margin-bottom:var(--space-2);font-size:var(--fs-md)}
.card p.small{color:var(--muted);margin-bottom:var(--space-3)}
.card-ico{width:38px;height:38px;display:grid;place-items:center;border-radius:10px;background:rgba(26,99,196,.09);color:var(--brand-2);margin-bottom:var(--space-3)}
.model-card{display:flex;flex-direction:column;gap:var(--space-2)}
.model-card .badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:var(--space-2)}
.badge{display:inline-block;font-size:var(--fs-xs);font-weight:700;padding:4px 9px;border-radius:6px;background:#eef3fa;color:var(--brand);border:1px solid var(--line);letter-spacing:.01em}
.badge.accent{background:rgba(242,140,30,.12);color:#8a4c00;border-color:rgba(242,140,30,.3)}
.badge.ok{background:rgba(15,138,95,.1);color:var(--ok);border-color:rgba(15,138,95,.25)}
.spec-list{margin:0;padding:0;list-style:none;font-size:var(--fs-sm)}
.spec-list li{display:flex;gap:8px;padding:5px 0;border-bottom:1px dashed var(--line)}
.spec-list li:last-child{border-bottom:0}
.spec-list span:first-child{color:var(--muted);min-width:44%}
.breadcrumbs{font-size:var(--fs-sm);color:var(--muted);padding:var(--space-4) 0 0;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.breadcrumbs a{color:var(--muted)} .breadcrumbs a:hover{color:var(--brand-2)}
.page-head{padding:var(--space-4) 0 var(--space-6)}
.layout-side{display:grid;grid-template-columns:1fr 340px;gap:var(--space-6);align-items:start}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:var(--space-5);box-shadow:var(--shadow-s)}
.panel + .panel{margin-top:var(--space-5)}
figure.photo{margin:0;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--surface);box-shadow:var(--shadow-s)}
figure.photo .ph{aspect-ratio:4/3;display:grid;place-items:center;background:linear-gradient(135deg,#eef2f8,#e2e9f3);color:var(--muted);font-size:var(--fs-sm);text-align:center;padding:var(--space-5)}
figure.photo figcaption{font-size:var(--fs-xs);color:var(--muted);padding:8px 12px;border-top:1px solid var(--line);background:var(--surface-2)}
figure.photo img{aspect-ratio:4/3;object-fit:contain;width:100%;background:#fff}
table.spec-table{width:100%;border-collapse:collapse;font-size:var(--fs-sm);background:var(--surface)}
table.spec-table th,table.spec-table td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
table.spec-table th{width:40%;color:var(--muted);font-weight:600;background:var(--surface-2)}
table.spec-table tr:hover td{background:#f8fafd}
pre.note{background:var(--surface-2);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--radius-sm);padding:var(--space-4);font-family:var(--font);font-size:var(--fs-sm);color:var(--ink-2);white-space:normal;margin:0 0 var(--space-4)}
.callout{background:linear-gradient(135deg,rgba(13,63,120,.96),rgba(26,99,196,.92));color:#fff;border-radius:var(--radius);padding:var(--space-6);box-shadow:var(--shadow-m)}
.callout h2,.callout h3{color:#fff}
.callout .btn-ghost{border-color:rgba(255,255,255,.5);color:#fff}
.callout .btn-ghost:hover{background:rgba(255,255,255,.12);color:#fff;border-color:#fff}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:0}
ol.steps li{counter-increment:s;position:relative;padding:0 0 var(--space-5) 44px;border-left:1px dashed var(--line-2);margin:0}
ol.steps li:last-child{border-left-color:transparent;padding-bottom:0}
ol.steps li::before{content:counter(s);position:absolute;left:-16px;top:-2px;width:32px;height:32px;border-radius:50%;background:var(--surface);border:1px solid var(--line-2);display:grid;place-items:center;font-weight:800;color:var(--brand-2);font-size:var(--fs-sm);box-shadow:var(--shadow-s)}
.filter-bar{display:flex;gap:var(--space-2);flex-wrap:wrap;margin-bottom:var(--space-5)}
.filter-bar select,.filter-bar input,.form input,.form select,.form textarea{font-family:var(--font);font-size:var(--fs-sm);padding:10px 12px;border:1px solid var(--line-2);border-radius:9px;background:var(--surface);color:var(--ink);transition:border-color .18s var(--ease),box-shadow .18s var(--ease)}
.filter-bar select:focus,.filter-bar input:focus,.form input:focus,.form select:focus,.form textarea:focus{outline:none;border-color:var(--brand-2);box-shadow:0 0 0 3px rgba(26,99,196,.14)}
.form{display:grid;gap:var(--space-3)}
.form label{display:block;font-size:var(--fs-sm);font-weight:600;color:var(--ink-2)}
.form label input,.form label select,.form label textarea{width:100%;margin-top:6px}
.form .row{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-3)}
.form textarea{min-height:120px;resize:vertical}
.form-actions{display:flex;align-items:center;gap:var(--space-3);flex-wrap:wrap}
.form-status{font-size:var(--fs-sm);font-weight:600}
.form-status.ok{color:var(--ok)}
.form-status.err{color:#b23c17}
.qr-row{display:flex;gap:var(--space-4);flex-wrap:wrap;margin-bottom:var(--space-3)}
.qr-cell{flex:1 1 128px;text-align:center}
.qr-cell img.qr{width:100%;max-width:140px;margin:0 auto;border:1px solid var(--line);border-radius:10px;background:#fff}
.qr-cell p.small{margin:8px 0 0}
.qr-pending{font-size:var(--fs-xs);color:var(--muted);border:1px dashed var(--line-2);border-radius:10px;padding:20px 10px;background:var(--surface-2)}
.notice{background:rgba(242,140,30,.1);border:1px solid rgba(242,140,30,.32);color:#7a4400;border-radius:var(--radius-sm);padding:var(--space-3) var(--space-4);font-size:var(--fs-sm);margin-bottom:var(--space-4)}
.footer{background:#0c1c31;color:#a9b7cb;margin-top:var(--space-8);padding:var(--space-8) 0 var(--space-5)}
.footer h4{color:#fff;font-size:var(--fs-sm);letter-spacing:.1em;text-transform:uppercase;margin-bottom:var(--space-3)}
.footer a{color:#a9b7cb;font-size:var(--fs-sm)}
.footer a:hover{color:#fff}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.2fr;gap:var(--space-6)}
.footer ul{list-style:none;padding:0;margin:0}
.footer li{margin-bottom:var(--space-2)}
.footer-bottom{border-top:1px solid rgba(255,255,255,.1);margin-top:var(--space-6);padding-top:var(--space-4);display:flex;justify-content:space-between;gap:var(--space-4);flex-wrap:wrap;font-size:var(--fs-xs)}
.tag-list{display:flex;gap:var(--space-2);flex-wrap:wrap;list-style:none;padding:0;margin:0}
.tag-list li{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:5px 10px;font-size:var(--fs-xs);color:var(--ink-2);margin:0}
.article-body{max-width:74ch}
.article-body h2{margin-top:var(--space-6)}
.article-body h3{margin-top:var(--space-5)}
.article-body ul li{margin-bottom:var(--space-2)}
.post-meta{font-size:var(--fs-sm);color:var(--muted);margin-bottom:var(--space-4)}
.scrolltop{position:fixed;right:18px;bottom:18px;width:42px;height:42px;border-radius:50%;background:var(--surface);border:1px solid var(--line-2);box-shadow:var(--shadow-m);cursor:pointer;display:grid;place-items:center;opacity:0;pointer-events:none;transition:opacity .2s var(--ease),transform .2s var(--ease);transform:translateY(8px)}
.scrolltop.show{opacity:1;pointer-events:auto;transform:translateY(0)}
.fade-up{animation:fadeUp .6s var(--ease) both}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media(max-width:1000px){
  .hero-inner{padding:var(--space-7) 0 var(--space-6)}
  .hero-brand-name .en{font-size:var(--fs-lg)} .layout-side{grid-template-columns:1fr}
  .grid-3,.grid-4{grid-template-columns:repeat(2,1fr)} .footer-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:960px){
  .nav-links{display:none;position:absolute;left:0;right:0;top:68px;background:var(--surface);border-bottom:1px solid var(--line);padding:var(--space-3) var(--space-5);flex-direction:column;align-items:stretch;box-shadow:var(--shadow-m);gap:2px}
  .nav-links.open{display:flex} .nav-toggle{display:block}
  .nav-links .nav-item{display:block}
  .nav-links .nav-item>a::after{display:none}
  .nav-links .sub{position:static;display:flex;box-shadow:none;border:0;padding:0 0 0 var(--space-4);min-width:0}
  .nav-links .sub a{padding:7px 11px;font-weight:500}
  .nav-links>a.btn{margin-top:var(--space-3);justify-content:center}
}
@media(max-width:720px){
  h1{font-size:var(--fs-2xl)} h2{font-size:var(--fs-xl)} .section{padding:var(--space-7) 0}
  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr} .footer-grid{grid-template-columns:1fr}
  .form .row{grid-template-columns:1fr}
  .logo-img{height:33px} .logo-text{font-size:12px;max-width:146px}
  .hero-brand{gap:14px} .hero-plate{padding:9px 13px} .hero-plate img{height:36px}
  .hero-invite{padding:var(--space-4)}
}
"""

JS = r"""
document.addEventListener('DOMContentLoaded', function () {
  var t = document.querySelector('.nav-toggle');
  var n = document.querySelector('.nav-links');
  if (t && n) { t.addEventListener('click', function () { n.classList.toggle('open'); }); }
  var st = document.querySelector('.scrolltop');
  if (st) {
    window.addEventListener('scroll', function () { st.classList.toggle('show', window.scrollY > 500); });
    st.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }
  var filter = document.getElementById('modelFilter');
  var brandFilter = document.getElementById('brandFilter');
  var search = document.getElementById('modelSearch');
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-model-card]'));
  function apply() {
    var cat = filter ? filter.value : 'all';
    var br = brandFilter ? brandFilter.value : 'all';
    var q = search ? search.value.trim().toLowerCase() : '';
    cards.forEach(function (c) {
      var okCat = cat === 'all' || c.dataset.category === cat;
      var okBrand = br === 'all' || c.dataset.brand === br;
      var hay = (c.dataset.search || '').toLowerCase();
      var okQ = !q || hay.indexOf(q) > -1;
      c.style.display = okCat && okBrand && okQ ? '' : 'none';
    });
  }
  if (filter) filter.addEventListener('change', apply);
  if (brandFilter) brandFilter.addEventListener('change', apply);
  if (search) search.addEventListener('input', apply);

  /* ---- enquiry / contact forms: POST to endpoint, fall back to email ---- */
  var LABELS = {
    name: 'Name', company: 'Company', email: 'E-mail', country: 'Country / port',
    model: 'Model', quantity: 'Quantity', contact: 'E-mail or WhatsApp',
    list: 'Models & quantities', notes: 'Notes', phone: 'Phone'
  };
  document.querySelectorAll('form.inquiry-form').forEach(function (f) {
    var st = f.querySelector('.form-status');
    function say(msg, cls) { if (st) { st.textContent = msg; st.className = 'form-status ' + (cls || ''); } }
    function collect() {
      var d = {};
      new FormData(f).forEach(function (v, k) { d[k] = String(v).trim(); });
      return d;
    }
    function asText(d) {
      return Object.keys(d).filter(function (k) { return d[k]; }).map(function (k) {
        return (LABELS[k] || k) + ': ' + d[k];
      }).join('\n');
    }
    function fallback(d) {
      var mail = f.getAttribute('data-email') || '';
      var subject = 'Compressor enquiry' + (d.model ? ' - ' + d.model : '');
      var body = asText(d) + '\n\n--\nSent from the website contact form';
      say('Opening your e-mail app — you can also send the same list on WhatsApp.', 'err');
      window.location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var req = f.querySelectorAll('[required]');
      for (var i = 0; i < req.length; i++) {
        if (!req[i].value.trim()) { req[i].focus(); say('Please fill in the required fields.', 'err'); return; }
      }
      var d = collect();
      if (!d.email && !d.contact) { say('Please add an e-mail address or WhatsApp number so we can reply.', 'err'); return; }
      var ep = (f.getAttribute('data-endpoint') || '').trim();
      if (!ep || ep.indexOf('REPLACE') > -1 || ep.indexOf('__') > -1) { fallback(d); return; }
      say('Sending…');
      fetch(ep, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { if (!r.ok) { throw new Error('HTTP ' + r.status); } return r.text(); })
        .then(function () { f.reset(); say('Thank you — we have your list and will reply within 24 hours.', 'ok'); })
        .catch(function () { fallback(d); });
    });
  });
});
"""

ICONS = {
    "check": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "arrow": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" y2="12" x2="19"/><polyline points="12 5 19 12 12 19"/></svg>',
    "bolt": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "ship": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 17a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3v-3H2z"/><path d="M5 14V7l7-4 7 4v7"/><path d="M9 14V9h6v5"/></svg>',
    "shield": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "box": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.3 7 12 12 20.7 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>',
    "gear": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1v.2a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-2.8-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0-1.1-2.7H3a2 2 0 1 1 0-4h.2A1.6 1.6 0 0 0 4.3 7l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 2.7-1.1V3a2 2 0 1 1 4 0v.2a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7h.2a2 2 0 1 1 0 4h-.2a1.6 1.6 0 0 0-1.4 1z"/></svg>',
    "search": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.7" y2="16.7"/></svg>',
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def cat_by_slug(data, slug):
    for c in data["categories"]:
        if c["slug"] == slug:
            return c
    return data["categories"][0]


def img_exists(name):
    return (SITE / "assets" / "img" / name).exists()


def figure(name, alt, caption, base="", fb="box"):
    path = base + "assets/img/" + name
    existing = (SITE / "assets" / "img" / name).exists()
    if existing:
        inner = '<img src="' + path + '" alt="' + esc(alt) + '" loading="lazy" width="1200" height="900">'
    else:
        inner = '<div class="ph">' + ICONS.get(fb, ICONS["box"]) + '<div>Replace with real product photo</div></div>'
    return '<figure class="photo">' + inner + '<figcaption>' + esc(caption) + '</figcaption></figure>'


def nav(active="", base=""):
    subs = [
        ("catalog.html", "All models", "catalog"),
        ("categories/rotary.html", "Rotary", "rotary"),
        ("categories/scroll.html", "Scroll", "scroll"),
        ("categories/reciprocating.html", "Refrigeration", "reciprocating"),
    ]
    sub_html = "".join(
        '<a class="' + ("active" if active == k else "") + '" href="' + base + h + '">' + lbl + "</a>"
        for h, lbl, k in subs
    )
    is_comp = active in ("catalog", "rotary", "scroll", "reciprocating")
    comp_cls = "active" if is_comp else ""
    out = []
    for href, label, key in [
        ("index.html", "Home", "index"),
    ]:
        cls = "active" if active == key else ""
        out.append('<a class="' + cls + '" href="' + base + href + '">' + label + "</a>")
        if key == "index":
            out.append(
                '<div class="nav-item has-sub"><a class="' + comp_cls + '" href="' + base + 'catalog.html">Compressors'
                "</a><div class=\"sub\">" + sub_html + "</div></div>"
            )
    return "".join(out)


def topbar(data, base=""):
    s = data["site"]
    return f"""<div class="topbar">
  <div class="wrap topbar-inner">
    <span class="tb-tag">Second-hand AC compressor recycling &middot; {esc(s['location'])}</span>
    <span class="tb-links">
      <a href="tel:{s['phone'].replace(' ', '')}">Tel</a>
      <a href="https://wa.me/{s['whatsapp'].replace(' ', '').replace('+', '')}" rel="nofollow noopener">WhatsApp</a>
      <a href="mailto:{esc(s['email'])}">Email</a>
    </span>
  </div>
</div>
"""


def head(data, title, desc, keywords, url, base="", page_type="website"):
    s = data["site"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<link rel="canonical" href="https://{s['domain']}/{url}">
<meta name="robots" content="index,follow">
<link rel="alternate" hreflang="en" href="https://{s['domain']}/{url}">
<meta property="og:type" content="{page_type}">
<meta property="og:site_name" content="{esc(s['brand'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="https://{s['domain']}/{url}">
<meta property="og:image" content="https://{s['domain']}/assets/img/{esc(s.get('og_image', 'og-cover.png'))}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d3f78">
<link rel="icon" type="image/png" sizes="96x96" href="{base}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{base}assets/css/style.css">
</head>
<body>"""


def header(data, active="", base=""):
    s = data["site"]
    logo_file = s.get("logo", "logo-horizontal.png")
    if (SITE / "assets" / "img" / logo_file).exists():
        brand_mark = (f'<img class="logo-img" src="{base}assets/img/{logo_file}" width="111" height="40"'
                      f' alt="{esc(s["brand"])}">')
    else:
        brand_mark = ('<span class="logo-mark"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"'
                      ' stroke="#fff" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/>'
                      '<circle cx="12" cy="12" r="2.6"/></svg></span>')
    return topbar(data, base) + f"""<header class="site-header">
<div class="wrap nav">
  <a class="logo" href="{base}index.html">
    {brand_mark}
    <span class="logo-text">{esc(s['brand'])}</span>
  </a>
  <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
  <nav class="nav-links">
    {nav(active, base)}
    <a class="btn btn-accent" href="{base}contact.html">Contact Us</a>
  </nav>
</div>
</header>"""


def footer(data, base=""):
    s = data["site"]
    cats = "".join(f'<li><a href="{base}categories/{c["slug"]}.html">{esc(c["name"])}</a></li>' for c in data["categories"])
    popular = [m for m in data["models"] if m.get("popular")]
    models_links = "".join(
        f'<li><a href="{base}models/{m["slug"]}.html">{esc(m["brand"])} {esc(m["model"])}</a></li>' for m in popular[:6]
    )
    return f"""<footer class="footer">
<div class="wrap">
  <div class="footer-grid">
    <div>
      <h4>{esc(s['brand'])}</h4>
      <p class="small" style="letter-spacing:.16em;color:#7f8ea6;margin:-8px 0 10px">{esc(s.get('brand_desc', ''))}</p>
      <p class="small">{esc(s['tagline'])}</p>
      <p class="small">{esc(s['location'])}<br>{esc(s['hours'])}</p>
      <p class="small" style="opacity:.75">{esc(s.get('brand_legal', ''))}</p>
      <p class="small">
        <a href="tel:{s['phone'].replace(' ', '')}">Tel: {esc(s['phone'])}</a><br>
        <a href="https://wa.me/{s['whatsapp'].replace(' ', '').replace('+', '')}" rel="nofollow noopener">WhatsApp: {esc(s['whatsapp'])}</a><br>
        WeChat: {esc(s['wechat'])}<br>
        <a href="mailto:{esc(s['email'])}">{esc(s['email'])}</a>
      </p>
    </div>
    <div>
      <h4>Products</h4>
      <ul>{cats}<li><a href="{base}catalog.html">Full model catalog</a></li></ul>
    </div>
    <div>
      <h4>Popular Models</h4>
      <ul>{models_links}</ul>
    </div>
    <div>
      <h4>Company</h4>
        <ul>
          <li><a href="{base}contact.html">Contact us</a></li>
        </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; {TODAY[:4]} {esc(s['brand'])}. All rights reserved.</span>
    <span class="small">All brand names and model numbers belong to their respective owners and are used for identification and compatibility reference only.</span>
  </div>
</div>
</footer>"""


def page_shell(data, body_html, active="", extra_head="", base=""):
    return body_html + f"""<button class="scrolltop" aria-label="Back to top">{ICONS['arrow']}</button>
<script src="{base}assets/js/app.js"></script>
{extra_head}
</body>
</html>"""


def cta_block(data, title="Let's build a long-term supply relationship", text="Tell us the models and volumes you move regularly. We would rather earn a repeat customer than win a single order — so we hold stock, keep prices competitive and answer straight.", base=""):
    s = data["site"]
    return f"""<section class="section tight">
<div class="wrap">
  <div class="callout">
    <div class="grid grid-2" style="align-items:center">
      <div>
        <h2>{esc(title)}</h2>
        <p style="color:rgba(255,255,255,.85);margin-bottom:0">{esc(text)}</p>
      </div>
      <div style="display:flex;gap:12px;justify-content:flex-end;flex-wrap:wrap">
        <a class="btn btn-accent" href="{base}contact.html">Contact us {ICONS['arrow']}</a>
        <a class="btn btn-ghost" href="mailto:{esc(s['email'])}">{esc(s['email'])}</a>
      </div>
    </div>
  </div>
</div>
</section>"""


def spec_table(specs):
    rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in specs.items())
    return f'<table class="spec-table"><tbody>{rows}</tbody></table>'


def bullets(items, cls=None):
    c = ' class="' + cls + '"' if cls else ""
    return "<ul" + c + ">" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def build_index(data):
    s = data["site"]
    title = "Baizly — Second-Hand AC Compressor Recycling & Supply in China"
    desc = "Baizly — second-hand AC compressor recycling and supply in China. Rotary, scroll and hermetic compressors for distributors, contractors and bulk or long-term buyers."
    keywords = "second hand compressor China, used ac compressor supplier, compressor recycling China, rotary compressor bulk, scroll compressor export, hermetic refrigeration compressor China"
    cat_cards = "".join(
        f"""<a class="card" href="categories/{c['slug']}.html" style="display:block">
      <div class="card-ico">{ICONS['gear']}</div>
      <h3>{esc(c['name'])}</h3>
      <p class="small">{esc(c['lead'])}</p>
      <span class="badge">Explore range {ICONS['arrow']}</span>
    </a>"""
        for c in data["categories"]
    )
    featured = [m for m in data["models"] if m.get("popular")][:6]
    featured_cards = "".join(model_card(m, data) for m in featured)
    chips = ["Bulk & long-term supply", "No minimum order", "Inspect-first-then-ship", "Export packing & documents"]
    chips_html = "".join(f"<li>{ICONS['check']}{esc(c)}</li>" for c in chips)
    why = [
        ("A supplier you can keep", "We are built for buyers who order again and again, not for one-off bargain hunters.", "bolt"),
        ("Double-checked before shipping", "Send a nameplate photo; we verify the match and re-check every electrical and mounting detail before dispatch — no surprises on arrival.", "search"),
        ("Start small, grow with trust", "We are glad to open the partnership with a single order and scale up step by step as trust builds — no large commitment needed to start.", "shield"),
        ("Sea, air or courier", "LCL/FCL from Shenzhen &amp; Guangzhou, or express samples to your door within days.", "ship"),
    ]
    why_html = "".join(
        f"<div class='card'><div class='card-ico'>{ICONS[i]}</div><h3>{esc(t)}</h3><p class='small' style='margin:0'>{esc(d)}</p></div>"
        for t, d, i in why
    )
    steps = [
        ("Send us your model list", "Email or WhatsApp the brands, models and target quantities.",),
        ("We reply within 24 h", "Availability, price, lead time, packing and freight to your port.",),
        ("Confirm &amp; pay deposit", "T/T 30% deposit, 70% before shipment. L/C available for volume.",),
        ("Inspect, ship &amp; track", "Pre-shipment testing, photos of loading, tracking until arrival.",),
    ]
    steps_html = "".join(f"<li><strong>{esc(t)}</strong><p class='small muted' style='margin:4px 0 0'>{d}</p></li>" for t, d in steps)
    org_ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": s["brand"],
        "alternateName": [s.get("brand_desc", "")],
        "legalName": s.get("brand_legal", ""),
        "url": "https://" + s["domain"] + "/",
        "logo": "https://" + s["domain"] + "/assets/img/" + s.get("logo", "logo-horizontal.png"),
        "description": s["tagline"],
        "email": s["email"],
        "telephone": s["phone"],
        "address": {"@type": "PostalAddress", "addressLocality": "Beijing", "addressCountry": "CN"},
    }, ensure_ascii=False) + "</script>"
    body = f"""{header(data, 'index')}
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-brand">
      <span class="hero-brand-name">
        <span class="en">{esc(s['brand'])}</span>
        <span class="desc">{esc(s.get('brand_desc', ''))}</span>
      </span>
    </div>
    <p class="hero-lead">{esc(s['tagline'])}</p>
    <div class="hero-invite">
      <p>{esc(s['invite'])}</p>
      <div class="hero-invite-actions">
        <a class="btn btn-accent" href="contact.html">Contact Us {ICONS['arrow']}</a>
        <span class="hero-direct">or reach us directly:
          <a href="https://wa.me/{s['whatsapp'].replace(' ', '').replace('+', '')}" rel="nofollow noopener">WhatsApp</a> &middot;
          <a href="mailto:{esc(s['email'])}">Email</a></span>
      </div>
    </div>
    <ul class="hero-chips">{chips_html}</ul>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Product families</span><h2>Three compressor families, direct from source</h2><p class="muted">Pick the family that matches your application, then drill down to the exact model numbers for specifications, compatibility notes and availability.</p></div>
    <div class="grid grid-3">{cat_cards}</div>
  </div>
</section>

<section class="section tight" style="background:var(--surface-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Popular models</span><h2>Models we move most</h2><p class="muted">Each model page carries full specifications, application notes, cross-reference checks and a direct line to our team.</p></div>
    <div class="grid grid-3">{featured_cards}</div>
    <p style="text-align:center;margin:24px 0 0"><a class="btn btn-primary" href="catalog.html">See all models {ICONS['arrow']}</a></p>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Why buyers stay with us</span><h2>Built for repeat wholesale buyers</h2></div>
    <div class="grid grid-4">{why_html}</div>
  </div>
</section>

<section class="section tight" style="background:var(--surface-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <div class="grid grid-2" style="gap:48px;align-items:start">
      <div>
        <span class="eyebrow">How it works</span>
        <h2>From first message to container in four steps</h2>
        <ol class="steps">{steps_html}</ol>
      </div>
      <div>
        <span class="eyebrow">Markets served</span>
        <h2>Shipping worldwide</h2>
        <p class="muted">We export regularly to the Middle East, Africa, Latin America, South and Southeast Asia, as well as Europe. Tell us your port and preferred Incoterm and we will price the shipment accordingly.</p>
        <ul class="tag-list">{''.join('<li>' + esc(x) + '</li>' for x in ['Middle East','West Africa','East Africa','South Africa','Latin America','Central Asia','Southeast Asia','Europe'])}</ul>
      </div>
    </div>
  </div>
</section>

{cta_block(data)}
{footer(data)}"""
    return head(data, title, desc, keywords, "") + page_shell(data, body, "index", org_ld)


def product_photo(slug):
    """型号页主图：优先实拍图 <slug>-1.jpg，回落到占位卡 -> 再回落到 HTML 占位框。
    实拍图只要按命名丢进 site/assets/img/products/ 就会自动接管，不用改代码。"""
    real = SITE / "assets" / "img" / "products" / (slug + "-1.jpg")
    ph = SITE / "assets" / "img" / "products" / (slug + "-placeholder.jpg")
    if real.exists():
        return ("products/" + slug + "-1.jpg", True)
    if ph.exists():
        return ("products/" + slug + "-placeholder.jpg", True)
    return ("__none__", False)


def model_card(m, data, base=""):
    kind = "Series" if m["kind"] == "series" else "Model"
    search = (m["brand"] + " " + m["model"] + " " + m["refrigerant"] + " " + m["hp"] + " " + m["category"]).lower()
    return f"""<a class="card model-card" href="{base}models/{m['slug']}.html" style="display:block"
        data-model-card data-category="{m['category']}" data-brand="{esc(m['brand'])}" data-search="{esc(search)}">
  <div class="badges"><span class="badge">{kind}</span><span class="badge accent">{esc(m['hp'])}</span><span class="badge">{esc(m['refrigerant'])}</span></div>
  <h3>{esc(m['brand'])} {esc(m['model'])}</h3>
  <p class="small">{esc(m['type'])} — {esc(m['category'])} range</p>
  <div style="margin-top:auto;padding-top:12px;display:flex;align-items:center;gap:6px;color:var(--brand-2);font-size:var(--fs-sm);font-weight:600">View full specification {ICONS['arrow']}</div>
</a>"""


def build_catalog(data):
    s = data["site"]
    title = "Used Compressor Model Catalog — Search by Brand, Type & Refrigerant | Baizly"
    desc = "Full catalog of air conditioner and refrigeration compressors: GMCC rotary, Copeland scroll, Embraco and Aspera hermetic units. Filter by type, brand or model keyword."
    keywords = "used compressor catalog, used AC compressor models list, buy used compressor by model number, used compressor supplier catalog"
    brands = sorted({m["brand"] for m in data["models"]})
    brand_opts = "".join(f'<option value="{esc(b)}">{esc(b)}</option>' for b in brands)
    cards = "".join(model_card(m, data) for m in data["models"])
    cats = "".join(f'<option value="{c["slug"]}">{esc(c["name"])}</option>' for c in data["categories"])
    body = f"""{header(data, 'catalog')}
<div class="wrap"><nav class="breadcrumbs"><a href="index.html">Home</a> / <span>Catalog</span></nav></div>
<section class="page-head"><div class="wrap">
  <h1>Used Compressor Model Catalog</h1>
  <p class="muted" style="max-width:70ch">{len(data['models'])} models and model families currently supplied for wholesale export. Use the filters to narrow by type, brand or keyword, or send us the model number directly and we will confirm what we can hold for you.</p>
</div></section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="filter-bar">
      <select id="modelFilter" aria-label="Filter by type"><option value="all">All types</option>{cats}</select>
      <select id="brandFilter" aria-label="Filter by brand"><option value="all">All brands</option>{brand_opts}</select>
      <input id="modelSearch" type="search" placeholder="Search model number, e.g. PH150, ZR34, NEK6213" style="min-width:260px">
      <a class="btn btn-primary" href="contact.html">Can't find it? Ask us {ICONS['arrow']}</a>
    </div>
    <div class="grid grid-3">{cards}</div>
    <div class="notice" style="margin-top:24px">Specifications shown are typical reference values and may vary slightly by production batch.</div>
  </div>
</section>
{cta_block(data, 'Missing a model in your list?', 'Send the nameplate photo and we will source it — including slow movers and older series.')}
{footer(data)}"""
    return head(data, title, desc, keywords, "catalog.html") + page_shell(data, body, "catalog")


def build_category(data, cat):
    s = data["site"]
    title = f"{cat['name']} — Second-Hand Supply from China | Baizly"
    desc = cat["lead"]
    keywords = ", ".join(cat["keywords"])
    base = "../"
    items = [m for m in data["models"] if m["category"] == cat["slug"]]
    cards = "".join(model_card(m, data, base) for m in items)
    intro = "".join(f"<p>{esc(p)}</p>" for p in cat["intro"])
    notes = bullets(cat["buying_notes"])
    body = f"""{header(data, cat['slug'], base)}
<div class="wrap"><nav class="breadcrumbs"><a href="{base}index.html">Home</a> / <span>{esc(cat['name'])}</span></nav></div>
<section class="page-head"><div class="wrap">
  <h1>{esc(cat['h1'])}</h1>
  <p class="muted" style="max-width:76ch">{esc(cat['lead'])}</p>
</div></section>
<section class="section" style="padding-top:0">
  <div class="wrap layout-side">
    <div>
      <div class="article-body">{intro}</div>
      <h2 style="margin-top:32px">{esc(cat['name'])} we supply regularly</h2>
      <div class="grid grid-2">{cards}</div>
    </div>
    <aside>
      <div class="panel">
        <h3>Buying checklist</h3>
        {notes}
      </div>
      <div class="panel">
        <h3>Trade terms</h3>
        <ul class="spec-list">
          <li><span>Quality check</span><span>{esc(s['warranty'])}</span></li>
          <li><span>Lead time (dispatch)</span><span>{esc(s['lead_time'])}</span></li>
          <li><span>Terms</span><span>{esc(s['ship_terms'])}</span></li>
        </ul>
        <p class="small muted" style="margin:14px 0 0">Dispatch from our China warehouse. International transit (sea or air) is additional — typically 7–35 days by destination and mode. Carrier and customs schedules cannot be guaranteed.</p>
        <p style="margin:16px 0 0"><a class="btn btn-accent" href="{base}contact.html">Contact us</a></p>
      </div>
      <div class="panel">
        <pre class="note" style="margin:0">{esc(s['disclaimer'])}</pre>
      </div>
    </aside>
  </div>
</section>
{cta_block(data, base=base)}
{footer(data, base)}
"""
    return head(data, title, desc, keywords, "categories/" + cat["slug"] + ".html", base) + page_shell(data, body, cat["slug"], "", base)


def build_model(data, m):
    s = data["site"]
    cat = cat_by_slug(data, m["category"])
    kind_word = "Series overview" if m["kind"] == "series" else "Model page"
    title = f"{m['brand']} {m['model']} — {m['hp']} {m['refrigerant']} {m['type']} Used Compressor | Baizly"
    desc = (m["intro"][:150].rsplit(" ", 1)[0] + " Bulk and long-term supply from China.")[:158]
    kw_list = [
        f"{m['brand']} {m['model']} used compressor",
        f"used {m['model']} compressor",
        f"{m['model']} replacement",
        f"used {m['hp']} {m['refrigerant']} compressor wholesale",
        f"buy used {m['brand']} compressor {m['model']}",
    ]
    keywords = ", ".join(kw_list)
    base = "../"
    related = [x for x in data["models"] if x["category"] == m["category"] and x["slug"] != m["slug"]][:3]
    related_cards = "".join(model_card(x, data, base) for x in related)
    if related_cards:
        related_html = f'<h2 style="margin-top:40px">Related models</h2><div class="grid grid-3">{related_cards}</div>'
    else:
        related_html = ""
    members_html = ""
    if m.get("members"):
        members_html = f'<h2>Models in this series</h2>{bullets(m["members"])}'
    breadcrumb = f"""<nav class="breadcrumbs"><a href="{base}index.html">Home</a> / <a href="{base}catalog.html">Catalog</a> / <a href="{base}categories/{cat['slug']}.html">{esc(cat['name'])}</a> / <span>{esc(m['brand'])} {esc(m['model'])}</span></nav>"""
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": f"{m['brand']} {m['model']} compressor",
        "sku": m["model"],
        "brand": {"@type": "Brand", "name": m["brand"]},
        "category": cat["name"],
        "description": desc,
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "priceSpecification": {"@type": "PriceSpecification", "valueAddedTaxIncluded": "false"},
            "seller": {"@type": "Organization", "name": s["brand"]},
        },
    }
    ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    photo_name, has_real = product_photo(m["slug"])
    photo_caption = ("Product photo — " + m["brand"] + " " + m["model"] if has_real and "-placeholder" not in photo_name
                     else "Product photo pending — real unit photo required before launch")
    highlights = bullets(m.get("highlights", []))
    apps = bullets(m.get("applications", []))
    body = f"""{header(data, m['category'], base)}
<div class="wrap">{breadcrumb}</div>
<section class="page-head"><div class="wrap">
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <span class="badge">{esc(kind_word)}</span>
    <span class="badge accent">{esc(m['hp'])}</span>
    <span class="badge">{esc(m['refrigerant'])}</span>
    <span class="badge ok">In stock</span>
  </div>
  <h1>{esc(m['brand'])} {esc(m['model'])} — {esc(m['hp'])} {esc(m['refrigerant'])} {esc(m['type'])} Used Compressor</h1>
  <p class="muted" style="max-width:76ch">{esc(m['type'])} compressor for {esc(m.get('applications', ['']) [0] if m.get('applications') else cat['name'].lower())}. Wholesale export supply — every unit is tested and inspected before dispatch.</p>
</div></section>
<section class="section" style="padding-top:0">
  <div class="wrap layout-side">
    <div>
      <div class="grid grid-2" style="align-items:start;margin-bottom:24px">
        {figure(photo_name, m['brand'] + ' ' + m['model'] + ' compressor', photo_caption, base, fb='box')}
        <div>
          <h3>Specifications</h3>
          {spec_table(m['specs'])}
          <p class="small muted" style="margin-top:8px">{esc(s['disclaimer'])}</p>
        </div>
      </div>
      <div class="article-body">
        <h2>Overview</h2>
        <p>{esc(m['intro'])}</p>
        <h2>Key points</h2>
        {highlights}
        {members_html}
        <h2>Applications</h2>
        {apps}
        <h2>Compatibility &amp; replacement notes</h2>
        <p>{esc(m.get('compatibility', ''))}</p>
      </div>
      {related_html}
    </div>
    <aside>
      <div class="panel">
        <h3 style="margin-bottom:12px">Send us your model list</h3>
        <form class="form inquiry-form" data-endpoint="{esc(s['inquiry_endpoint'])}" data-email="{esc(s['email'])}" novalidate>
          <input type="hidden" name="model" value="{esc(m['brand'])} {esc(m['model'])}">
          <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
          <label>Quantity
            <input type="number" name="quantity" min="1" placeholder="e.g. 50" style="width:100%;margin-top:6px">
          </label>
          <label>Country / port
            <input type="text" name="country" placeholder="e.g. Lagos, Nigeria" style="width:100%;margin-top:6px">
          </label>
          <label>Email or WhatsApp
            <input type="text" name="contact" placeholder="you@company.com" style="width:100%;margin-top:6px">
          </label>
          <button class="btn btn-accent" type="submit">Send message</button>
          <span class="form-status" role="status" aria-live="polite"></span>
        </form>
        <p class="small muted" style="margin:12px 0 0">We reply within 24 hours, Mon&ndash;Sat. Or message us on <a href="https://wa.me/{s['whatsapp'].replace(' ', '').replace('+', '')}" rel="nofollow noopener">WhatsApp</a>.</p>
      </div>
      <div class="panel">
        <h3>Trade terms</h3>
        <ul class="spec-list">
          <li><span>Quality check</span><span>{esc(m['buying']['warranty'])}</span></li>
          <li><span>Lead time (dispatch)</span><span>{esc(m['buying']['lead'])}</span></li>
          <li><span>Pricing</span><span>{esc(m['buying']['price'])}</span></li>
          <li><span>Terms</span><span>{esc(s['ship_terms'])}</span></li>
        </ul>
        <p class="small muted" style="margin:14px 0 0">Dispatch from our China warehouse. International transit (sea or air) is additional — typically 7–35 days by destination and mode. Carrier and customs schedules cannot be guaranteed.</p>
      </div>
      <div class="panel">
        <h3>Other {esc(cat['name'])}</h3>
        <ul>{''.join('<li><a href="' + x['slug'] + '.html">' + esc(x['brand']) + ' ' + esc(x['model']) + '</a></li>' for x in related)}</ul>
      </div>
    </aside>
  </div>
</section>
{cta_block(data, 'Build a long-term supply relationship', s['invite'], base)}
{footer(data, base)}"""
    extra = ld
    return head(data, title, desc, keywords, "models/" + m["slug"] + ".html", base, "product") + page_shell(data, body, "", extra, base)


def build_static(data, key):
    s = data["site"]
    pages = {
        "contact": {
            "title": "Contact Us — Second-Hand Compressor Recycling in Beijing | Baizly",
            "desc": "Family-run used AC compressor recycling source in Beijing, China. Reach us by phone, WhatsApp, WeChat or email. Inspect-first-then-ship, reply within 24 hours.",
            "kw": "contact compressor supplier China, used ac compressor supplier, compressor recycling Beijing",
            "h1": "Talk to us directly",
        },
    }
    p = pages[key]
    base = ""
    content = f"""
      <p>Our family runs an air-conditioning compressor recycling business based in China. The Beijing area is our home base, and we have rich sources of used compressors from all over the country.</p>
      <div class="callout" style="margin:0 0 32px">
        <p style="color:#fff;margin:0;font-size:var(--fs-md)">{esc(s['invite'])}</p>
      </div>
      <p>Pick whichever channel suits you — a phone call, a chat message or an email all reach the same small team. We support pre-shipment photo and video selection and an inspect-first-then-ship model, so you see exactly what you get before it leaves our warehouse.</p>
      <p class="small muted" style="margin:0 0 8px">Language: phone, WeChat and WhatsApp are answered in <strong>Chinese and basic English</strong>; email handles <strong>full English</strong> enquiries.</p>
      <h2>How to reach us</h2>
      <div class="grid grid-2" style="gap:24px;margin:8px 0 24px">
        <div class="panel">
          <h3>Contact channels</h3>
          <ul class="spec-list">
            <li><span>1 &middot; Phone</span><a href="tel:{s['phone'].replace(' ', '')}">{esc(s['phone'])}</a></li>
            <li><span>2 &middot; Chat apps</span><a href="https://wa.me/{s['whatsapp'].replace(' ', '').replace('+', '')}" rel="nofollow noopener">WhatsApp</a> &middot; WeChat: {esc(s['wechat'])}</li>
            <li><span>3 &middot; Email</span><a href="mailto:{esc(s['email'])}">{esc(s['email'])}</a></li>
            <li><span>Location</span>{esc(s['location'])}</li>
            <li><span>Hours</span>{esc(s['hours'])}</li>
          </ul>
        </div>
        <div class="panel">
          <h3>Chat app QR codes</h3>
          <div class="qr-row">
            <div class="qr-cell">
              <img class="qr" src="{base}assets/img/qr-whatsapp.png" alt="WhatsApp QR" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
              <div class="qr-pending" style="display:none">QR pending — drop qr-whatsapp.png into assets/img/</div>
              <p class="small">WhatsApp: {esc(s['whatsapp'])}</p>
            </div>
          </div>
          <p class="small muted">New to WhatsApp? Download it from your app store, then scan our code to add us.</p>
        </div>
      </div>
      <h2>Send us your model list</h2>
      <p>Tell us what you need and we will come back with availability, price, lead time and freight. The more specific your list, the faster we can help — and for regular volume we will keep the price competitive.</p>
      <form class="form inquiry-form" data-endpoint="{esc(s['inquiry_endpoint'])}" data-email="{esc(s['email'])}" novalidate>
        <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
        <div class="row">
          <label>Name<input type="text" name="name" required placeholder="Full name"></label>
          <label>Company<input type="text" name="company" placeholder="Company"></label>
        </div>
        <div class="row">
          <label>Email<input type="email" name="email" placeholder="you@company.com"></label>
          <label>Country / port<input type="text" name="country" placeholder="e.g. Durban, South Africa"></label>
        </div>
        <label>Models &amp; quantities<textarea name="list" placeholder="GMCC PH150X1C-4P3 x 100 pcs&#10;Copeland ZR34K3-PFJ-522 x 20 pcs"></textarea></label>
        <label>Notes<textarea name="notes" placeholder="Incoterm, target delivery, inspection requirements"></textarea></label>
        <div class="form-actions"><button class="btn btn-accent" type="submit">Send message</button><span class="form-status" role="status" aria-live="polite"></span></div>
      </form>
      <p class="notice">Prefer chat? Send the same list on WhatsApp and we will answer there. We reply within 24 hours, Mon&ndash;Sat. If the form cannot reach our server it opens your email app with the message ready to send.</p>
    """
    faq_block = ""
    body = f"""{header(data, key)}
<div class="wrap"><nav class="breadcrumbs"><a href="index.html">Home</a> / <span>{esc(p['h1'])}</span></nav></div>
<section class="page-head"><div class="wrap"><h1>{esc(p['h1'])}</h1></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="article-body">{content}</div></div></section>
{faq_block}
{cta_block(data)}
{footer(data)}"""
    return head(data, p["title"], p["desc"], p["kw"], key + ".html") + page_shell(data, body, key)



def build_404(data):
    s = data["site"]
    body = f"""{header(data)}
<section class="page-head"><div class="wrap"><h1>Page not found</h1><p class="muted">The page you were looking for has moved or never existed. Try the catalog below.</p><p><a class="btn btn-primary" href="catalog.html">Browse all models {ICONS['arrow']}</a></p></div></section>
{footer(data)}"""
    return head(data, "Page not found | Baizly", "Page not found", "", "404.html") + page_shell(data, body)


def write_sitemap(data, urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>https://{data['site']['domain']}/{u}</loc><changefreq>weekly</changefreq><priority>{0.9 if u == '' else 0.6}</priority></url>")
    lines.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def write_robots(data):
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /assets/\n\nSitemap: https://" + data["site"]["domain"] + "/sitemap.xml\n",
        encoding="utf-8",
    )


def write_keyword_doc(data):
    DOCS.mkdir(exist_ok=True)
    lines = ["# 关键词覆盖表（英文站 v1）", "", "> 由 `tools/build_site.py` 从 data/models.json 自动生成，改数据后重跑脚本即同步。", "",
             f"生成日期：{TODAY} · 站点：{data['site']['brand']} · 域名占位：{data['site']['domain']}", "",
             "## 一、型号长尾词（每型号一页，一页一词族）", "",
             "| 页面 | 主关键词 | 次级长尾词 | 覆盖意图 |", "| --- | --- | --- | --- |"]
    for m in data["models"]:
        primary = f"{m['brand']} {m['model']}"
        sec = " / ".join([
            f"{m['model']} compressor",
            f"{m['model']} replacement",
            f"{m['hp']} {m['refrigerant']} compressor wholesale",
            f"{m['model']} price FOB",
        ])
        intent = "替换件采购 / 备件囤货" if m["kind"] == "model" else "系列整体采购 / 型号选型"
        lines.append(f"| models/{m['slug']}.html | {primary} | {sec} | {intent} |")
    lines += ["", "## 二、品类词（中量，做栏目/聚合页）", "", "| 页面 | 目标词 | 说明 |", "| --- | --- | --- |"]
    for c in data["categories"]:
        lines.append(f"| categories/{c['slug']}.html | {', '.join(c['keywords'])} | {c['lead'][:40]}… |")
    lines += ["", "## 三、通用商业意图词（首页 / Contact 承接）", ""]
    for k in ["AC compressor wholesale", "air conditioner compressor supplier China", "buy compressors in bulk",
              "compressor factory direct price", "refrigeration compressor export"]:
        lines.append(f"- {k}")
    lines += ["", "## 四、后续扩词方向（待补关键词词格，按此模板扩型号页）", "",
              "- `[brand] [model] cross reference` — 替换对照，转化率最高\n"
              "- `[model] equivalent / replacement for [original brand]`\n"
              "- `[hp] hp [refrigerant] compressor [application]`（如 1.5 hp r410a compressor split unit）\n"
              "- `[model] specifications / datasheet / PDF` — 抓技术型搜索\n"
              "- `buy [model] online` / `[model] price [country]` — 后期可开国家子目录（/ng/ /sa/ /ae/）"]
    (DOCS / "01_关键词覆盖表.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    (SITE / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "img").mkdir(parents=True, exist_ok=True)
    (SITE / "categories").mkdir(exist_ok=True)
    (SITE / "models").mkdir(exist_ok=True)
    (SITE / "assets" / "css" / "style.css").write_text(CSS, encoding="utf-8")
    (SITE / "assets" / "js" / "app.js").write_text(JS, encoding="utf-8")

    urls = [""]

    (SITE / "index.html").write_text(build_index(data), encoding="utf-8")
    (SITE / "catalog.html").write_text(build_catalog(data), encoding="utf-8"); urls.append("catalog.html")
    for c in data["categories"]:
        (SITE / "categories" / (c["slug"] + ".html")).write_text(build_category(data, c), encoding="utf-8")
        urls.append("categories/" + c["slug"] + ".html")
    for m in data["models"]:
        (SITE / "models" / (m["slug"] + ".html")).write_text(build_model(data, m), encoding="utf-8")
        urls.append("models/" + m["slug"] + ".html")
    for key in ["contact"]:
        (SITE / (key + ".html")).write_text(build_static(data, key), encoding="utf-8")
        urls.append(key + ".html")
    (SITE / "404.html").write_text(build_404(data), encoding="utf-8")

    write_sitemap(data, urls)
    write_robots(data)
    write_keyword_doc(data)
    print(f"OK: {len(urls)} pages -> {SITE}")
    print("models:", len(data["models"]), "| categories:", len(data["categories"]))


if __name__ == "__main__":
    main()
