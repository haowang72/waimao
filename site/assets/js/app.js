
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
