/* Shared behaviour: header, mobile menu, search, reveals, practice memory, patient form. */
(function () {
  var html = document.documentElement;
  html.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var top = document.getElementById('top');

  // header state
  if (top) {
    var onScroll = function () { top.classList.toggle('scrolled', window.scrollY > 12); };
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  }

  // mobile menu
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  if (burger && menu) {
    var toggle = function (open) {
      burger.setAttribute('aria-expanded', String(open));
      menu.hidden = !open;
      document.body.classList.toggle('menu-open', open);
    };
    burger.addEventListener('click', function () { toggle(burger.getAttribute('aria-expanded') !== 'true'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) { toggle(false); burger.focus(); } });
  }

  // search overlay with a static index
  var search = document.getElementById('search');
  var q = document.getElementById('q');
  var results = document.getElementById('search-results');
  var indexCache = null;
  var openSearch = function () {
    if (!search) return;
    search.hidden = false; document.body.classList.add('search-open');
    q.focus();
    if (!indexCache) fetch(q.getAttribute('data-index')).then(function (r) { return r.json(); }).then(function (d) { indexCache = d; render(q.value); });
  };
  var closeSearch = function () { if (!search) return; search.hidden = true; document.body.classList.remove('search-open'); };
  var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  var render = function (value) {
    if (!indexCache) return;
    var v = norm(value.trim());
    results.innerHTML = '';
    if (!v) return;
    var hits = indexCache.filter(function (i) { return norm(i.t + ' ' + i.d).indexOf(v) !== -1; }).slice(0, 8);
    if (!hits.length) { results.innerHTML = '<li class="none">' + results.getAttribute('data-none') + '</li>'; return; }
    hits.forEach(function (i) {
      var li = document.createElement('li');
      li.innerHTML = '<a href="' + i.u + '"><b></b><span></span></a>';
      li.querySelector('b').textContent = i.t; li.querySelector('span').textContent = i.d;
      results.appendChild(li);
    });
  };
  document.querySelectorAll('[data-open-search]').forEach(function (b) { b.addEventListener('click', openSearch); });
  document.querySelectorAll('[data-close-search]').forEach(function (b) { b.addEventListener('click', closeSearch); });
  if (q) q.addEventListener('input', function () { render(q.value); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && search && !search.hidden) closeSearch();
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
  });

  // reveals
  var targets = [].slice.call(document.querySelectorAll('.mask, .r, .hero-pic, .hero-band, .loc, .quick-list li, .trust-item, .soin-row'));
  if (reduce || !('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
    targets.forEach(function (el) { el.classList.add('r'); io.observe(el); });
  }

  // dropdown menus: click or keyboard on the small button, hover handled in CSS
  document.querySelectorAll('.has-sub').forEach(function (li) {
    var btn = li.querySelector('.sub-btn');
    btn.addEventListener('click', function () {
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      document.querySelectorAll('.has-sub').forEach(function (o) { if (o !== li) { o.classList.remove('open'); o.querySelector('.sub-btn').setAttribute('aria-expanded', 'false'); } });
    });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget)) { li.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); } });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') document.querySelectorAll('.has-sub.open').forEach(function (o) { o.classList.remove('open'); o.querySelector('.sub-btn').setAttribute('aria-expanded', 'false'); }); });

  // remember the chosen practice
  document.querySelectorAll('[data-choose]').forEach(function (a) {
    a.addEventListener('click', function () { try { localStorage.setItem('cdm-cabinet', a.getAttribute('data-choose')); } catch (e) {} });
  });

  // simple contact form feedback
  var form = document.querySelector('.form');
  if (form) form.addEventListener('submit', function () { var ok = form.querySelector('.form-ok'); if (ok) ok.hidden = false; });

  // patient form
  var pf = document.getElementById('pform');
  if (pf) {
    var steps = [].slice.call(pf.querySelectorAll('.fstep'));
    var navItems = [].slice.call(document.querySelectorAll('.form-steps li'));
    var prev = pf.querySelector('[data-prev]'), next = pf.querySelector('[data-next]'), print = pf.querySelector('[data-print]'), send = pf.querySelector('[data-send]'), clear = pf.querySelector('[data-clear]');
    var status = pf.querySelector('.form-status'), progress = pf.querySelector('.form-progress');
    var KEY = 'cdm-patient-form';
    var cur = 0;
    var labelFor = function (el) {
      var id = el.id; var l = id ? pf.querySelector('label[for="' + id + '"]') : null;
      if (l) return l.textContent;
      var fl = el.closest('.field'); if (fl && fl.querySelector('.field-label')) return fl.querySelector('.field-label').textContent;
      var chk = el.closest('.chk'); if (chk) return chk.querySelector('span').textContent;
      return el.name;
    };
    var values = function () {
      var out = [];
      steps.slice(0, 5).forEach(function (st) {
        [].slice.call(st.querySelectorAll('input, select, textarea')).forEach(function (el) {
          if (el.type === 'radio' && !el.checked) return;
          if (el.type === 'checkbox') { if (el.checked) out.push([labelFor(el), pf.getAttribute('data-empty') === el.value ? '' : el.value]); return; }
          out.push([labelFor(el), el.value]);
        });
      });
      return out;
    };
    var save = function () {
      var data = {};
      [].slice.call(pf.querySelectorAll('input, select, textarea')).forEach(function (el) {
        if (el.type === 'checkbox') data[el.name] = el.checked; else if (el.type === 'radio') { if (el.checked) data[el.name] = el.value; } else data[el.name] = el.value;
      });
      try { localStorage.setItem(KEY, JSON.stringify(data)); status.textContent = pf.getAttribute('data-saved'); } catch (e) {}
    };
    var load = function () {
      try {
        var data = JSON.parse(localStorage.getItem(KEY) || 'null'); if (!data) return;
        [].slice.call(pf.querySelectorAll('input, select, textarea')).forEach(function (el) {
          if (!(el.name in data)) return;
          if (el.type === 'checkbox') el.checked = !!data[el.name]; else if (el.type === 'radio') el.checked = data[el.name] === el.value; else el.value = data[el.name];
        });
      } catch (e) {}
    };
    var avsValid = function (raw) {
      var d = raw.replace(/\D/g, '');
      if (d.length !== 13 || d.slice(0, 3) !== '756') return false;
      var sum = 0;
      for (var i = 0; i < 12; i++) sum += parseInt(d[i], 10) * (i % 2 === 0 ? 1 : 3);
      return (10 - (sum % 10)) % 10 === parseInt(d[12], 10);
    };
    var avs = pf.querySelector('[data-avs]');
    if (avs) avs.addEventListener('input', function () {
      var chk = avs.closest('.field').querySelector('.avs-check');
      var d = avs.value.replace(/\D/g, '');
      if (!d) { chk.textContent = ''; avs.classList.remove('bad', 'good'); return; }
      var ok = avsValid(d);
      chk.textContent = ok ? pf.getAttribute('data-avs-ok') : pf.getAttribute('data-avs-bad');
      avs.classList.toggle('bad', !ok && d.length >= 13); avs.classList.toggle('good', ok);
      if (ok) avs.value = d.slice(0, 3) + '.' + d.slice(3, 7) + '.' + d.slice(7, 11) + '.' + d.slice(11);
    });
    var validate = function (st) {
      var ok = true;
      [].slice.call(st.querySelectorAll('[required]')).forEach(function (el) {
        var field = el.closest('.field') || el.closest('.chk');
        var bad = el.type === 'checkbox' ? !el.checked : !el.value.trim();
        if (!bad && el.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value)) bad = true;
        var msg = field.querySelector('.err');
        if (bad) { if (!msg) { msg = document.createElement('p'); msg.className = 'err'; field.appendChild(msg); } msg.textContent = el.type === 'email' && el.value ? pf.getAttribute('data-email-bad') : pf.getAttribute('data-required'); ok = false; }
        else if (msg) msg.remove();
      });
      if (avs && st.contains(avs) && avs.value.replace(/\D/g, '') && !avsValid(avs.value)) { ok = false; avs.focus(); }
      return ok;
    };
    var recap = function () {
      var dl = document.getElementById('recap'); dl.innerHTML = '';
      values().forEach(function (kv) {
        var div = document.createElement('div');
        var dt = document.createElement('dt'); dt.textContent = kv[0];
        var dd = document.createElement('dd'); dd.textContent = kv[1] || pf.getAttribute('data-empty'); if (!kv[1]) dd.className = 'empty';
        div.appendChild(dt); div.appendChild(dd); dl.appendChild(div);
      });
    };
    var show = function (i) {
      cur = i;
      steps.forEach(function (st, k) { st.hidden = k !== i; });
      navItems.forEach(function (li, k) { if (k === i) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current'); li.classList.toggle('done', k < i); });
      prev.hidden = i === 0; next.hidden = i === steps.length - 1; print.hidden = i !== steps.length - 1; send.hidden = i !== steps.length - 1;
      progress.textContent = pf.getAttribute('data-step') + ' ' + (i + 1) + ' ' + pf.getAttribute('data-of') + ' ' + steps.length;
      if (i === steps.length - 1) { recap(); var dt = pf.querySelector('#p-date'); if (dt && !dt.value) dt.value = new Date().toISOString().slice(0, 10); }
      steps[i].querySelector('legend').setAttribute('tabindex', '-1'); steps[i].querySelector('legend').focus({ preventScroll: false });
      window.scrollTo({ top: pf.getBoundingClientRect().top + window.scrollY - 120, behavior: reduce ? 'auto' : 'smooth' });
    };
    next.addEventListener('click', function () { if (validate(steps[cur])) { save(); show(cur + 1); } });
    prev.addEventListener('click', function () { show(cur - 1); });
    navItems.forEach(function (li, k) { li.addEventListener('click', function () { if (k < cur) show(k); }); });
    pf.addEventListener('input', function () { clearTimeout(pf._t); pf._t = setTimeout(save, 400); });
    print.addEventListener('click', function () { if (validate(steps[cur])) { save(); window.print(); } });
    send.addEventListener('click', function () {
      if (!validate(steps[cur])) return;
      var body = values().map(function (kv) { return kv[0] + ': ' + (kv[1] || '-'); }).join('\n');
      window.location.href = 'mailto:' + pf.getAttribute('data-mail') + '?subject=' + encodeURIComponent('Formulaire patient') + '&body=' + encodeURIComponent(body);
    });
    clear.addEventListener('click', function () { try { localStorage.removeItem(KEY); } catch (e) {} pf.reset(); show(0); status.textContent = ''; });
    load();
    var want = new URLSearchParams(location.search).get('cabinet');
    if (want) { var r = pf.querySelector('input[name="cabinet"][value="' + (want.charAt(0).toUpperCase() + want.slice(1)) + '"]'); if (r) r.checked = true; }
    show(0);
  }
})();
