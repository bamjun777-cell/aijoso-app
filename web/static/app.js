/* AI 좋소 웹 동작. 서버 없음: 개인 데이터는 이 브라우저(localStorage)에만 저장 */
(function () {
  'use strict';
  var D = window.AIJ || {}, R = document.body.getAttribute('data-root') || '', L = document.body.getAttribute('data-lroot') || R;
  var CAT = {}; (D.categories || []).forEach(function (c) { CAT[c.id] = c.name; });
  // 화면 문구 (앱과 같은 ui.json). T('min.n', {n: 3}) → '3분'
  var U = D.ui || {};
  function T(k, a) { var s = U[k] || k; if (a) Object.keys(a).forEach(function (x) { s = s.split('{' + x + '}').join(a[x]); }); return s; }
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem('aijoso.' + k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem('aijoso.' + k, JSON.stringify(v)); } catch (e) {} }
  };
  var S = { favs: store.get('favs', []), recent: store.get('recent', []), vals: store.get('vals', {}), reqs: store.get('reqs', []), react: store.get('react', {}), myfb: store.get('myfb', []) };
  function save(k) { store.set(k, S[k]); }
  function today() { var d = new Date(Date.now() - new Date().getTimezoneOffset() * 60000); return d.toISOString().slice(0, 10); }

  function toast(t) {
    $$('.toast').forEach(function (x) { x.remove(); });
    var el = document.createElement('div'); el.className = 'toast'; el.setAttribute('role', 'status'); el.textContent = t;
    document.body.appendChild(el); setTimeout(function () { el.remove(); }, 2000);
  }
  function layer(html) { $('#layer').innerHTML = html; }
  function closeLayer() { layer(''); hideTip(); document.body.style.overflow = ''; }

  function copyText(t, msg) {
    var done = function () { toast(msg || T('prompt.copied')); };
    var fallback = function () {
      layer('<div class="fallback" role="dialog" aria-label="' + esc(T('web.copyFallbackAria')) + '"><b>' + esc(T('web.copyFallback')) + '</b><textarea id="fbta" readonly>' + esc(t) + '</textarea><div class="pact" style="padding:8px 0 0"><button type="button" class="btn ghost" data-close="1">' + esc(T('req.close')) + '</button></div></div>');
      var ta = $('#fbta'); ta.focus(); ta.select();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, fallback); else fallback();
  }

  /* ───── 검색 (앱 Searcher와 같은 규칙) ───── */
  var STOP = ['the', 'and', 'for', 'with', 'from', 'into', 'your', 'you', 'all', 'one', 'out', 'get', 'how', 'what', 'are', 'can', 'this', 'that', 'takes', 'forever'];
  var ascii = function (w) { return /^[\x00-\x7f]*$/.test(w); };
  // 영어 단어는 단어 처음부터 맞을 때만 (pay → payroll O, ar → car X). 한·중·일은 포함 여부
  function hit(term, text) {
    if (!ascii(term)) return text.indexOf(term) >= 0;
    var e = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return new RegExp('(^|[^a-z0-9])' + e + (term.length <= 3 ? '($|[^a-z0-9])' : '')).test(text);
  }
  function useful(w) { return w.length > 1 && !(ascii(w) && (w.length < 3 || STOP.indexOf(w) >= 0)); }
  function score(it, q) {
    q = (q || '').trim().toLowerCase(); if (!q) return 1;
    var qs = q.replace(/\s+/g, ''), s = 0, title = it.title.toLowerCase();
    it.terms.forEach(function (w) { var lw = w.toLowerCase(); if ((lw.length > 1 || lw === q) && (hit(lw, q) || (!ascii(lw) && qs.indexOf(lw) >= 0))) s += hit(lw, title) ? 3 : 2; });
    q.split(/\s+/).forEach(function (w) { if (useful(w) && hit(w, title)) s += 2; });
    if (it.status === 'published' && s) s += 0.5;
    return s;
  }
  function cardHtml(it) {
    var pub = it.status === 'published';
    var meta = '<span class="pill">' + esc(CAT[it.category] || '') + '</span><span class="pill">' + esc(T('diff.label') + ' ' + T('diff.' + it.difficulty)) + '</span>';
    if (pub) return '<a class="card pub" href="' + L + 'm/' + esc(it.id) + '.html"><h3>' + esc(it.title) + '</h3><p>' + esc(it.subtitle).replace(/\n/g, '<br>') + '</p><div class="meta">' + meta + '<span class="pill save">' + esc(T('min.n', { n: it.before }) + ' → ' + T('min.n', { n: it.after })) + '</span></div></a>';
    var req = S.reqs.indexOf(it.id) >= 0;
    return '<button type="button" class="card draft" data-req="' + esc(it.id) + '"><h3>' + esc(it.title) + '</h3><div class="meta">' + meta + '<span class="pill ' + (req ? 'req' : 'draft') + '" data-reqpill="' + esc(it.id) + '">' + esc(req ? T('pill.requested') : T('pill.draft')) + '</span></div></button>';
  }
  function markReqPills() {
    $$('[data-reqpill]').forEach(function (p) { var on = S.reqs.indexOf(p.getAttribute('data-reqpill')) >= 0; p.className = 'pill ' + (on ? 'req' : 'draft'); p.textContent = on ? T('pill.requested') : T('pill.draft'); });
  }

  function initSearch() {
    var res = $('#results'); if (!res) return;
    var params = new URLSearchParams(location.search);
    var st = { q: params.get('q') || '', cat: params.get('c') || '', diff: '' };
    var input = $('#q'); input.value = st.q;
    function run() {
      var list = D.index.map(function (it) { return [it, score(it, st.q)]; })
        .filter(function (x) { return x[1] > 0 && (!st.cat || x[0].category === st.cat) && (!st.diff || x[0].difficulty === st.diff); })
        .sort(function (a, b) { return b[1] - a[1] || (a[0].status === 'published' ? -1 : 1) - (b[0].status === 'published' ? -1 : 1); })
        .map(function (x) { return x[0]; });
      res.innerHTML = list.length ? list.map(cardHtml).join('') : '<div class="empty"><b>' + esc(T('search.emptyTitle')) + '</b>' + esc(T('search.emptyBodyWeb')) + '</div>';
      $('#count').textContent = st.q ? T('search.results', { q: st.q, n: list.length }) : T('home.total', { n: list.length });
      $$('[data-fcat]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-fcat') === st.cat)); });
      $$('[data-fdiff]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-fdiff') === st.diff)); });
    }
    var t;
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { st.q = input.value; run(); history.replaceState(null, '', st.q ? '?q=' + encodeURIComponent(st.q) : location.pathname); }, 200); });
    input.form.addEventListener('submit', function (e) { e.preventDefault(); st.q = input.value; run(); input.blur(); });
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fcat],[data-fdiff]'); if (!b) return;
      if (b.hasAttribute('data-fcat')) st.cat = b.getAttribute('data-fcat'); else st.diff = b.getAttribute('data-fdiff');
      run();
    });
    run();
  }

  /* ───── 매뉴얼 상세 ───── */
  var ITEM_ID = (function () { var el = $('[data-item]'); return el ? el.getAttribute('data-item') : null; })();
  var ITEM = ITEM_ID ? D.items[ITEM_ID] : null;
  function valueFor(id, p, k) {
    var v = (S.vals[id + '.' + k] || '').trim(); if (v) return v;
    for (var i = 0; i < p.variables.length; i++) if (p.variables[i].key === k) return p.variables[i].example;
    return k;
  }
  function fill(id, p) { return p.body.replace(/\{\{(.+?)\}\}/g, function (m, k) { return valueFor(id, p, k); }); }
  function promptOf(id, pid) { var it = D.items[id]; for (var i = 0; i < it.prompts.length; i++) if (it.prompts[i].id === pid) return it.prompts[i]; }
  function updPrev(pid) {
    var el = $('[data-prev="' + pid + '"]'); if (!el) return;
    var p = promptOf(ITEM_ID, pid);
    el.innerHTML = esc(p.body).replace(/\{\{(.+?)\}\}/g, function (m, k) { return '<mark>' + esc(valueFor(ITEM_ID, p, k.replace(/&amp;/g, '&'))) + '</mark>'; });
  }
  function favBtn() {
    var b = $('[data-fav]'); if (!b) return;
    var on = S.favs.indexOf(ITEM_ID) >= 0;
    b.querySelector('span').textContent = on ? T('fav.has') : T('fav.add');
    b.setAttribute('aria-pressed', String(on));
  }
  function reactBtns() { $$('[data-react]').forEach(function (b) { b.setAttribute('aria-pressed', String(S.react[ITEM_ID] === b.getAttribute('data-react'))); }); }
  function fbCount() { var n = S.myfb.filter(function (f) { return f.contentId === ITEM_ID; }).length; var el = $('#fbcount'); if (el) el.textContent = n ? T('fb.sentCount', { n: n }) : ''; }

  function initManual() {
    if (!ITEM) return;
    S.recent = [ITEM_ID].concat(S.recent.filter(function (x) { return x !== ITEM_ID; })).slice(0, 20); save('recent');
    $$('[data-var]').forEach(function (inp) { inp.value = S.vals[inp.getAttribute('data-var')] || ''; });
    ITEM.prompts.forEach(function (p) { updPrev(p.id); });
    favBtn(); reactBtns(); fbCount();
    document.addEventListener('input', function (e) {
      var t = e.target; if (!t.hasAttribute || !t.hasAttribute('data-var')) return;
      var key = t.getAttribute('data-var'); S.vals[key] = t.value; save('vals');
      $$('[data-var="' + key + '"]').forEach(function (o) { if (o !== t) o.value = t.value; updPrev(o.getAttribute('data-pid')); });
      updPrev(t.getAttribute('data-pid'));
    });
    // 목차: 지금 읽는 위치 표시
    var links = $$('.toc a'); if ('IntersectionObserver' in window && links.length) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id); }); }); }, { rootMargin: '-30% 0px -60% 0px' });
      $$('.block').forEach(function (b) { io.observe(b); });
    }
  }

  /* ───── 의견 (욕설·비속어·개인정보 차단: 앱·저장소 규칙과 같은 기준) ───── */
  function makeChecker(M) {
    var strip = function (s) { return s.replace(/[^가-힣ㄱ-ㅎㅏ-ㅣa-z\u3040-\u30ff\u3400-\u9fff]/g, ''); };
    var allow = M.allow.map(function (s) { return s.toLowerCase(); });
    var banned = M.banned.map(function (s) { return strip(s.toLowerCase()); }).filter(Boolean);
    return function (raw) {
      var text = String(raw || ''), t = text.toLowerCase().normalize('NFC'), len = text.trim().length;
      var lim = { min: M.minLength, max: M.maxLength };
      if (len < M.minLength) return { ok: false, reason: 'short', msg: T('mod.short', lim) };
      if (len > M.maxLength) return { ok: false, reason: 'long', msg: T('mod.long', lim) };
      if (/01[016789][\s.\-]?\d{3,4}[\s.\-]?\d{4}/.test(t) || /[\w.+-]+@[\w-]+\.[\w.]+/.test(t) || /\d{6}[\s\-]?[1-8]\d{6}/.test(t) ||
          (t.match(/\+?\(?\d[\d\s().\-]{7,}\d/g) || []).some(function (m) { return m.replace(/\D/g, '').length >= 9; }))
        return { ok: false, reason: 'pii', msg: T('mod.pii') };
      var s = t; allow.forEach(function (a) { s = s.split(a).join(' '); });
      var toks = s.split(/\s+/).map(strip).filter(Boolean), cands = toks.slice(), run = '';
      toks.concat(['##']).forEach(function (w) { if (w.length === 1) run += w; else { if (run.length > 1) cands.push(run); run = ''; } });
      if (cands.some(function (c) { return banned.some(function (b) { return c.indexOf(b) >= 0; }); })) return { ok: false, reason: 'abuse', msg: T('mod.abuse') };
      return { ok: true };
    };
  }
  var CHECK = D.moderation ? makeChecker(D.moderation) : function () { return { ok: true }; };
  var fbType = 'error';
  function fbSheet() {
    var types = D.feedback.types, max = D.feedback.maxLength;
    document.body.style.overflow = 'hidden';
    layer('<div class="scrim" data-close="1"></div><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="fbh"><h3 id="fbh">' + esc(T('fbs.title')) + '</h3><p class="note">' + esc(ITEM.title) + '</p>' +
      '<div class="types" role="group" aria-label="' + esc(T('fbs.kind')) + '">' + types.map(function (x) { return '<button type="button" class="f" data-fbtype="' + x.id + '" aria-pressed="' + (x.id === fbType) + '">' + esc(x.label) + '</button>'; }).join('') + '</div>' +
      '<label for="fbtext" class="note"><b>' + esc(T('fbs.content')) + '</b></label><textarea id="fbtext" maxlength="' + max + '" placeholder="' + esc(T('fbs.placeholder')) + '"></textarea>' +
      '<div class="fbmeta"><span id="fbmsg" class="fbmsg" aria-live="polite"></span><span id="fbcnt" class="num">0/' + max + '</span></div>' +
      '<p class="note">' + esc(T('fbs.noticeWeb')) + '</p>' +
      '<div class="pact"><button type="button" class="btn ghost" data-close="1">' + esc(T('fbs.cancel')) + '</button><button type="button" class="btn copy" id="fbsend" disabled>' + esc(T('fbs.send')) + '</button></div></div>');
    $('#fbtext').focus(); fbValidate();
  }
  function fbValidate() {
    var ta = $('#fbtext'); if (!ta) return;
    var v = ta.value, r = CHECK(v), typed = v.trim().length > 0, msg = $('#fbmsg');
    $('#fbcnt').textContent = v.length + '/' + D.feedback.maxLength;
    msg.textContent = typed && !r.ok ? r.msg : '';
    msg.classList.toggle('bad', typed && !r.ok && r.reason !== 'short');
    $('#fbsend').disabled = !r.ok;
    ta.setAttribute('aria-invalid', String(typed && !r.ok && r.reason !== 'short'));
  }
  function reqSheet(id) {
    var it = D.index.filter(function (x) { return x.id === id; })[0]; if (!it) return;
    var on = S.reqs.indexOf(id) >= 0;
    layer('<div class="scrim" data-close="1"></div><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="rqh"><h3 id="rqh">' + esc(T('req.title')) + '</h3><p><b>' + esc(it.title) + '</b></p><p class="note">' + esc(T('req.note')) + '</p>' +
      '<div class="pact"><button type="button" class="btn ghost" data-close="1">' + esc(T('req.close')) + '</button><button type="button" class="btn copy" data-reqtoggle="' + esc(id) + '">' + esc(on ? T('req.cancel') : T('req.want')) + '</button></div></div>');
  }

  /* ───── A4 출력 미리보기 + 실제 인쇄 ───── */
  function calcSpan(c) {
    if (typeof c === 'string') return esc(c);
    if (!c.d && !c.f) return esc(c.v);
    return '<span class="calc" tabindex="0" data-f="' + esc(c.f || '') + '" data-d="' + esc(c.d || '') + '">' + esc(c.v) + '</span>';
  }
  function a4Html(ps) {
    var K = ps.calc || {};
    var inl = function (t) { return esc(t).replace(/\[\[(\w+)\]\]/g, function (m, k) { return K[k] ? calcSpan(K[k]) : m; }); };
    var body = ps.blocks.map(function (b) {
      if (b.type === 'meta') return '<div class="m ' + (b.align === 'right' ? 'r' : '') + '">' + esc(b.text) + '</div>';
      if (b.type === 'heading') return '<div class="hd">' + esc(b.text) + '</div>';
      if (b.type === 'section') return '<div class="sec">' + esc(b.text) + '</div>';
      if (b.type === 'bullets') return '<ul>' + b.items.map(function (x) { return '<li>' + inl(x) + '</li>'; }).join('') + '</ul>';
      if (b.type === 'note') return '<div class="nt">' + esc(b.text) + '</div>';
      if (b.type === 'table') return (b.caption ? '<div class="cap">' + esc(b.caption) + '</div>' : '') + '<table><thead><tr>' + b.columns.map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>' +
        b.rows.map(function (r, i) { return '<tr class="' + (b.totalRow && i === b.rows.length - 1 ? 'tot' : '') + '">' + r.map(function (c) { return '<td>' + calcSpan(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>';
      return '';
    }).join('');
    var head = ps.blocks.some(function (b) { return b.type === 'heading'; }) ? '' : '<div class="hd">' + esc(ps.title) + '</div>';
    return '<div class="a4 ' + ps.orientation + '" id="a4">' + head + body + '<div class="foot4">' + esc(T('web.page')) + '</div></div>';
  }
  var ZOOM = false, PS = null;
  function openPrint() {
    PS = ITEM.printSample; ZOOM = false;
    document.body.style.overflow = 'hidden';
    layer('<div class="pv" role="dialog" aria-modal="true" aria-label="' + esc(T('web.a4')) + '"><div class="pv-bar"><div class="wrap"><button type="button" class="iconbtn" data-close="1" aria-label="' + esc(T('req.close')) + '"><svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button><h2>' + esc(T('web.a4')) + '</h2><button type="button" class="btn copy" data-doprint="1">' + esc(T('web.print')) + '</button></div></div>' +
      '<div class="pv-info wrap"><p>' + T('web.a4Info') + '</p><div class="pv-tools"><div class="chips" style="margin:0">' + PS.printSetup.map(function (s) { return '<span class="chip">' + esc(s) + '</span>'; }).join('') + '</div><button type="button" class="btn ghost" data-zoom="1">' + esc(T('web.zoomIn')) + '</button></div></div>' +
      '<div class="pv-stage wrap"><div class="pv-scale" id="pvs"><div class="pv-sizer" id="pvz">' + a4Html(PS) + '</div></div></div></div>');
    fitA4();
  }
  function fitA4() {
    var s = $('#pvs'), z = $('#pvz'), a = $('#a4'); if (!s || !a) return;
    var full = a.offsetWidth, fit = Math.min(1, (s.parentElement.clientWidth) / full), k = ZOOM ? Math.max(fit, 0.85) : fit;
    a.style.transform = 'scale(' + k + ')'; z.style.width = (full * k) + 'px'; z.style.height = (a.offsetHeight * k) + 'px';
    s.style.width = Math.min(full * fit, s.parentElement.clientWidth) + 'px';
    if (ZOOM) s.style.width = '100%';
  }
  window.addEventListener('resize', fitA4);
  function doPrint() {
    if (!PS) return;
    var root = document.createElement('div'); root.id = 'printroot'; root.innerHTML = a4Html(PS);
    var st = document.createElement('style'); st.id = 'pagesize';
    st.textContent = '@page{size:A4 ' + PS.orientation + ';margin:' + (PS.orientation === 'landscape' ? '12mm 14mm' : '20mm') + '}';
    document.body.appendChild(root); document.head.appendChild(st); document.body.classList.add('printing');
    var done = function () { document.body.classList.remove('printing'); root.remove(); st.remove(); window.removeEventListener('afterprint', done); };
    window.addEventListener('afterprint', done);
    window.print();
    setTimeout(function () { if (document.body.classList.contains('printing') && !window.matchMedia('print').matches) done(); }, 1500);
  }

  /* ───── 산식 툴팁 ───── */
  var tipEl = null, tipFor = null, tipAt = 0;
  function showTip(el) {
    hideTip(); tipFor = el; tipAt = Date.now(); el.classList.add('on');
    tipEl = document.createElement('div'); tipEl.className = 'tip'; tipEl.setAttribute('role', 'tooltip');
    tipEl.innerHTML = (el.getAttribute('data-f') ? '<b>' + esc(T('web.formula')) + '</b><code>' + esc(el.getAttribute('data-f')) + '</code>' : '') + '<b>' + esc(T('web.calc')) + '</b>' + esc(el.getAttribute('data-d'));
    document.body.appendChild(tipEl);
    var r = el.getBoundingClientRect(), tw = tipEl.offsetWidth, th = tipEl.offsetHeight;
    var x = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), innerWidth - tw - 8), y = r.top - th - 8; if (y < 8) y = r.bottom + 8;
    tipEl.style.left = x + 'px'; tipEl.style.top = y + 'px';
  }
  function hideTip() { if (tipEl) { tipEl.remove(); tipEl = null; } if (tipFor) { tipFor.classList.remove('on'); tipFor = null; } }
  // 마우스가 있는 PC만 올림/내림으로 표시. 휴대폰은 탭(클릭)으로만 열고, 다른 곳을 탭하면 닫힘
  var HOVER = window.matchMedia && window.matchMedia('(hover: hover)').matches;
  if (HOVER) {
    document.addEventListener('mouseover', function (e) { var c = e.target.closest && e.target.closest('.calc'); if (c && c !== tipFor) showTip(c); });
    document.addEventListener('mouseout', function (e) { var c = e.target.closest && e.target.closest('.calc'); if (c && !c.contains(e.relatedTarget)) hideTip(); });
  }
  document.addEventListener('focusin', function (e) { var c = e.target.closest && e.target.closest('.calc'); if (c) showTip(c); });
  document.addEventListener('focusout', function (e) { if (e.target.closest && e.target.closest('.calc')) hideTip(); });
  document.addEventListener('scroll', function () { if (Date.now() - tipAt > 400) hideTip(); }, true);

  /* ───── 보관함 ───── */
  var seg = 'fav';
  function renderSaved() {
    var box = $('#savedlist'); if (!box) return;
    $$('[data-seg]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-seg') === seg));
      var n = { fav: S.favs.length, recent: S.recent.length, fb: S.myfb.length }[b.getAttribute('data-seg')];
      b.textContent = T('saved.' + b.getAttribute('data-seg')) + ' ' + n;
    });
    var byId = {}; D.index.forEach(function (x) { byId[x.id] = x; });
    if (seg === 'fb') {
      var T = {}; D.feedback.types.forEach(function (x) { T[x.id] = x.label; });
      var list = S.myfb.slice().reverse();
      box.innerHTML = list.length ? list.map(function (f) {
        var done = (D.resolvedFeedback || []).indexOf(f.id) >= 0, it = byId[f.contentId];
        return '<div class="fbi"><div class="meta"><span class="pill ' + (done ? 'save' : '') + '">' + esc(done ? T('saved.resolved') : T('saved.received')) + '</span><span class="pill">' + esc(T[f.type] || '') + '</span><span class="num note">' + esc(f.date) + '</span></div><h3>' + esc(it ? it.title : '') + '</h3><p>' + esc(f.text) + '</p></div>';
      }).join('') : '<div class="empty"><b>' + esc(T('saved.noFbTitle')) + '</b>' + esc(T('saved.noFbBody')) + '</div>';
      return;
    }
    var ids = seg === 'fav' ? S.favs : S.recent, its = ids.map(function (i) { return byId[i]; }).filter(Boolean);
    box.innerHTML = its.length ? its.map(cardHtml).join('') : '<div class="empty"><b>' + esc(seg === 'fav' ? T('saved.noFavTitle') : T('saved.noRecentTitle')) + '</b>' + esc(seg === 'fav' ? T('saved.noFavBody') : T('saved.noRecentBody')) + '</div>';
  }

  /* ───── 클릭 처리 ───── */
  document.addEventListener('click', function (e) {
    var cc = e.target.closest('.calc');
    // 휴대폰 탭은 mouseover가 먼저 와서 이미 보이는 상태 → 다시 숨기지 않음. 다른 곳을 누르면 닫힘
    if (cc) { if (tipFor !== cc) showTip(cc); return; } else hideTip();
    var b = e.target.closest('button, [data-close]'); if (!b) return;
    var g = function (k) { return b.getAttribute(k); };
    if (b.hasAttribute('data-close')) { closeLayer(); return; }
    if (g('data-copy')) { copyText(fill(ITEM_ID, promptOf(ITEM_ID, g('data-copy')))); return; }
    if (g('data-qcopy')) { var q = g('data-qcopy').split('|'); copyText(fill(q[0], promptOf(q[0], q[1]))); return; }
    if (b.hasAttribute('data-copyproj')) { copyText(ITEM.project.instructions, T('proj.copied')); return; }
    if (b.hasAttribute('data-fav')) { var i = S.favs.indexOf(ITEM_ID); if (i >= 0) S.favs.splice(i, 1); else S.favs.unshift(ITEM_ID); save('favs'); favBtn(); toast(i >= 0 ? T('fav.removed') : T('fav.added')); return; }
    if (b.hasAttribute('data-share')) {
      var data = { title: ITEM.title + ' | ' + T('app.name'), text: ITEM.subtitle.replace(/\n/g, ' '), url: location.href };
      if (navigator.share) navigator.share(data).catch(function () {}); else copyText(data.title + '\n' + data.url, T('share.linkCopied'));
      return;
    }
    if (g('data-print')) { openPrint(); return; }
    if (b.hasAttribute('data-doprint')) { doPrint(); return; }
    if (b.hasAttribute('data-zoom')) { ZOOM = !ZOOM; b.textContent = ZOOM ? T('web.zoomOut') : T('web.zoomIn'); hideTip(); fitA4(); return; }
    if (g('data-react')) {
      var k = g('data-react'); if (S.react[ITEM_ID] === k) delete S.react[ITEM_ID]; else S.react[ITEM_ID] = k; save('react'); reactBtns();
      if (S.react[ITEM_ID] === 'bad') fbSheet(); else if (S.react[ITEM_ID] === 'good') toast(T('react.goodToast'));
      return;
    }
    if (b.hasAttribute('data-fbopen')) { fbSheet(); return; }
    if (g('data-fbtype')) { fbType = g('data-fbtype'); $$('[data-fbtype]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-fbtype') === fbType)); }); return; }
    if (b.id === 'fbsend') {
      var v = $('#fbtext').value; if (!CHECK(v).ok) { fbValidate(); return; }
      S.myfb.push({ id: 'fb-' + Math.random().toString(36).slice(2, 14), contentId: ITEM_ID, type: fbType, text: v.trim(), date: today() }); save('myfb');
      closeLayer(); fbCount(); toast(T('fbs.thanks')); return;
    }
    if (g('data-req')) { reqSheet(g('data-req')); return; }
    if (g('data-reqtoggle')) { var id = g('data-reqtoggle'), j = S.reqs.indexOf(id); if (j >= 0) S.reqs.splice(j, 1); else S.reqs.push(id); save('reqs'); closeLayer(); markReqPills(); toast(j >= 0 ? T('req.removed') : T('req.added')); return; }
    if (g('data-seg')) { seg = g('data-seg'); renderSaved(); return; }
  });
  document.addEventListener('input', function (e) { if (e.target.id === 'fbtext') fbValidate(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && $('#layer').innerHTML) closeLayer(); });

  /* ───── 언어 ───── */
  // 한국어 페이지를 다른 언어 사용자가 처음 열면, 맞는 언어 페이지를 권한다 (강제로 옮기지 않음)
  function initLang() {
    $$('[data-setlang]').forEach(function (a) { a.addEventListener('click', function () { store.set('lang', a.getAttribute('data-setlang')); }); });
    var box = $('#langsuggest'); if (!box || store.get('lang', '')) return;
    var nav = (navigator.languages && navigator.languages[0]) || navigator.language || '';
    nav = nav.toLowerCase(); if (!nav || nav.indexOf('ko') === 0) return;
    var want = nav.indexOf('ja') === 0 ? 'ja' : nav.indexOf('zh') === 0 ? (/hant|tw|hk|mo/.test(nav) ? 'zh-Hant' : 'zh-Hans') : 'en';
    var a = $('[data-setlang="' + want + '"]'); if (!a) return;
    box.innerHTML = '<div class="wrap"><span>' + esc((D.suggest || {})[want] || '') + '</span><a class="btn copy" href="' + a.getAttribute('href') + '" data-setlang="' + want + '">' + esc(a.textContent) + '</a><button type="button" class="iconbtn" data-langno="1" aria-label="' + esc(T('req.close')) + '">×</button></div>';
    box.hidden = false;
    box.querySelector('[data-langno]').addEventListener('click', function () { store.set('lang', 'ko'); box.hidden = true; });
    box.querySelector('[data-setlang]').addEventListener('click', function () { store.set('lang', want); });
  }

  initSearch(); initManual(); renderSaved(); markReqPills(); initLang();
})();
