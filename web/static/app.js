/* AI 좋소 웹 동작. 서버 없음: 개인 데이터는 이 브라우저(localStorage)에만 저장 */
(function () {
  'use strict';
  var D = window.AIJ || {}, R = document.body.getAttribute('data-root') || '';
  var CAT = {}; (D.categories || []).forEach(function (c) { CAT[c.id] = c.name; });
  var DIFF = { easy: '쉬움', normal: '보통', hard: '어려움' };
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
    var done = function () { toast(msg || '복사했어요! Claude에 붙여넣으세요'); };
    var fallback = function () {
      layer('<div class="fallback" role="dialog" aria-label="직접 복사"><b>길게 눌러 전체 선택 후 복사하세요</b><textarea id="fbta" readonly>' + esc(t) + '</textarea><div class="pact" style="padding:8px 0 0"><button type="button" class="btn ghost" data-close="1">닫기</button></div></div>');
      var ta = $('#fbta'); ta.focus(); ta.select();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, fallback); else fallback();
  }

  /* ───── 검색 (앱 Searcher와 같은 규칙) ───── */
  function score(it, q) {
    q = (q || '').trim().toLowerCase(); if (!q) return 1;
    var qs = q.replace(/\s+/g, ''), s = 0, title = it.title.toLowerCase();
    it.terms.forEach(function (w) { var lw = w.toLowerCase(); if (lw.length > 1 && (q.indexOf(lw) >= 0 || qs.indexOf(lw) >= 0)) s += title.indexOf(lw) >= 0 ? 3 : 2; });
    q.split(/\s+/).forEach(function (w) { if (w.length > 1 && it.title.indexOf(w) >= 0) s += 2; });
    if (it.status === 'published' && s) s += 0.5;
    return s;
  }
  function cardHtml(it) {
    var pub = it.status === 'published';
    var meta = '<span class="pill">' + esc(CAT[it.category] || '') + '</span><span class="pill">난이도 ' + esc(DIFF[it.difficulty] || '') + '</span>';
    if (pub) return '<a class="card pub" href="' + R + 'm/' + esc(it.id) + '.html"><h3>' + esc(it.title) + '</h3><p>' + esc(it.subtitle).replace(/\n/g, '<br>') + '</p><div class="meta">' + meta + '<span class="pill save">' + it.before + '분 → ' + it.after + '분</span></div></a>';
    var req = S.reqs.indexOf(it.id) >= 0;
    return '<button type="button" class="card draft" data-req="' + esc(it.id) + '"><h3>' + esc(it.title) + '</h3><div class="meta">' + meta + '<span class="pill ' + (req ? 'req' : 'draft') + '" data-reqpill="' + esc(it.id) + '">' + (req ? '요청함' : '준비 중') + '</span></div></button>';
  }
  function markReqPills() {
    $$('[data-reqpill]').forEach(function (p) { var on = S.reqs.indexOf(p.getAttribute('data-reqpill')) >= 0; p.className = 'pill ' + (on ? 'req' : 'draft'); p.textContent = on ? '요청함' : '준비 중'; });
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
      res.innerHTML = list.length ? list.map(cardHtml).join('') : '<div class="empty"><b>아직 없는 업무예요</b>다른 말로 찾거나 아래 의견으로 요청해 주세요</div>';
      $('#count').textContent = (st.q ? '\'' + st.q + '\' 검색 결과 ' : '') + list.length + '개';
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
    b.querySelector('span').textContent = on ? '보관함에 있음' : '보관함에 담기';
    b.setAttribute('aria-pressed', String(on));
  }
  function reactBtns() { $$('[data-react]').forEach(function (b) { b.setAttribute('aria-pressed', String(S.react[ITEM_ID] === b.getAttribute('data-react'))); }); }
  function fbCount() { var n = S.myfb.filter(function (f) { return f.contentId === ITEM_ID; }).length; var el = $('#fbcount'); if (el) el.textContent = n ? '보낸 의견 ' + n + '건 · 보관함에서 확인' : ''; }

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
    var strip = function (s) { return s.replace(/[^가-힣ㄱ-ㅎㅏ-ㅣa-z]/g, ''); };
    var allow = M.allow.map(function (s) { return s.toLowerCase(); });
    var banned = M.banned.map(function (s) { return strip(s.toLowerCase()); }).filter(Boolean);
    return function (raw) {
      var text = String(raw || ''), t = text.toLowerCase().normalize('NFC'), len = text.trim().length;
      if (len < M.minLength) return { ok: false, reason: 'short', msg: M.minLength + '자 이상 적어 주세요' };
      if (len > M.maxLength) return { ok: false, reason: 'long', msg: M.maxLength + '자까지 쓸 수 있어요' };
      if (/01[016789][\s.\-]?\d{3,4}[\s.\-]?\d{4}/.test(t) || /[\w.+-]+@[\w-]+\.[\w.]+/.test(t) || /\d{6}[\s\-]?[1-8]\d{6}/.test(t))
        return { ok: false, reason: 'pii', msg: '전화번호·이메일·주민번호는 적지 말아 주세요' };
      var s = t; allow.forEach(function (a) { s = s.split(a).join(' '); });
      var toks = s.split(/\s+/).map(strip).filter(Boolean), cands = toks.slice(), run = '';
      toks.concat(['##']).forEach(function (w) { if (w.length === 1) run += w; else { if (run.length > 1) cands.push(run); run = ''; } });
      if (cands.some(function (c) { return banned.some(function (b) { return c.indexOf(b) >= 0; }); })) return { ok: false, reason: 'abuse', msg: '욕설·비속어가 있어 보낼 수 없어요' };
      return { ok: true };
    };
  }
  var CHECK = D.moderation ? makeChecker(D.moderation) : function () { return { ok: true }; };
  var fbType = 'error';
  function fbSheet() {
    var types = D.feedback.types, max = D.feedback.maxLength;
    document.body.style.overflow = 'hidden';
    layer('<div class="scrim" data-close="1"></div><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="fbh"><h3 id="fbh">의견 남기기</h3><p class="note">' + esc(ITEM.title) + '</p>' +
      '<div class="types" role="group" aria-label="의견 종류">' + types.map(function (x) { return '<button type="button" class="f" data-fbtype="' + x.id + '" aria-pressed="' + (x.id === fbType) + '">' + esc(x.label) + '</button>'; }).join('') + '</div>' +
      '<label for="fbtext" class="note"><b>내용</b></label><textarea id="fbtext" maxlength="' + max + '" placeholder="예) 2단계 메뉴 이름이 달라요"></textarea>' +
      '<div class="fbmeta"><span id="fbmsg" class="fbmsg" aria-live="polite"></span><span id="fbcnt" class="num">0/' + max + '</span></div>' +
      '<p class="note">욕설·비속어, 개인정보는 보낼 수 없어요. 지금은 이 기기에 저장되고, 곧 운영자에게 전달되도록 연결돼요.</p>' +
      '<div class="pact"><button type="button" class="btn ghost" data-close="1">취소</button><button type="button" class="btn copy" id="fbsend" disabled>보내기</button></div></div>');
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
    layer('<div class="scrim" data-close="1"></div><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="rqh"><h3 id="rqh">지금 쓰고 있는 매뉴얼이에요</h3><p><b>' + esc(it.title) + '</b></p><p class="note">요청이 많은 매뉴얼부터 올려요</p>' +
      '<div class="pact"><button type="button" class="btn ghost" data-close="1">닫기</button><button type="button" class="btn copy" data-reqtoggle="' + esc(id) + '">' + (on ? '요청 취소' : '먼저 보고 싶어요') + '</button></div></div>');
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
    return '<div class="a4 ' + ps.orientation + '" id="a4">' + head + body + '<div class="foot4">1 / 1 쪽</div></div>';
  }
  var ZOOM = false, PS = null;
  function openPrint() {
    PS = ITEM.printSample; ZOOM = false;
    document.body.style.overflow = 'hidden';
    layer('<div class="pv" role="dialog" aria-modal="true" aria-label="A4 출력 미리보기"><div class="pv-bar"><div class="wrap"><button type="button" class="iconbtn" data-close="1" aria-label="닫기"><svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button><h2>A4 출력 미리보기</h2><button type="button" class="btn copy" data-doprint="1">인쇄하기</button></div></div>' +
      '<div class="pv-info wrap"><p><b>결과물 예시</b> · 밑줄 숫자에 마우스를 올리면(휴대폰은 탭) 산식이 보여요</p><div class="pv-tools"><div class="chips" style="margin:0">' + PS.printSetup.map(function (s) { return '<span class="chip">' + esc(s) + '</span>'; }).join('') + '</div><button type="button" class="btn ghost" data-zoom="1">크게 보기</button></div></div>' +
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
    tipEl.innerHTML = (el.getAttribute('data-f') ? '<b>엑셀 수식</b><code>' + esc(el.getAttribute('data-f')) + '</code>' : '') + '<b>산식</b>' + esc(el.getAttribute('data-d'));
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
      b.textContent = { fav: '즐겨찾기', recent: '최근 본', fb: '내 의견' }[b.getAttribute('data-seg')] + ' ' + n;
    });
    var byId = {}; D.index.forEach(function (x) { byId[x.id] = x; });
    if (seg === 'fb') {
      var T = {}; D.feedback.types.forEach(function (x) { T[x.id] = x.label; });
      var list = S.myfb.slice().reverse();
      box.innerHTML = list.length ? list.map(function (f) {
        var done = (D.resolvedFeedback || []).indexOf(f.id) >= 0, it = byId[f.contentId];
        return '<div class="fbi"><div class="meta"><span class="pill ' + (done ? 'save' : '') + '">' + (done ? '반영됨' : '접수됨') + '</span><span class="pill">' + esc(T[f.type] || '') + '</span><span class="num note">' + esc(f.date) + '</span></div><h3>' + esc(it ? it.title : '') + '</h3><p>' + esc(f.text) + '</p></div>';
      }).join('') : '<div class="empty"><b>보낸 의견이 없어요</b>매뉴얼 맨 아래에서 남길 수 있어요</div>';
      return;
    }
    var ids = seg === 'fav' ? S.favs : S.recent, its = ids.map(function (i) { return byId[i]; }).filter(Boolean);
    box.innerHTML = its.length ? its.map(cardHtml).join('') : '<div class="empty"><b>' + (seg === 'fav' ? '담아 둔 매뉴얼이 없어요' : '아직 본 매뉴얼이 없어요') + '</b>' + (seg === 'fav' ? '매뉴얼에서 [보관함에 담기]를 눌러 보세요' : '매뉴얼을 열면 여기 남아요') + '</div>';
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
    if (b.hasAttribute('data-copyproj')) { copyText(ITEM.project.instructions, '지침을 복사했어요'); return; }
    if (b.hasAttribute('data-fav')) { var i = S.favs.indexOf(ITEM_ID); if (i >= 0) S.favs.splice(i, 1); else S.favs.unshift(ITEM_ID); save('favs'); favBtn(); toast(i >= 0 ? '보관함에서 뺐어요' : '보관함에 담았어요'); return; }
    if (b.hasAttribute('data-share')) {
      var data = { title: ITEM.title + ' | AI 좋소', text: ITEM.subtitle.replace(/\n/g, ' '), url: location.href };
      if (navigator.share) navigator.share(data).catch(function () {}); else copyText(data.title + '\n' + data.url, '링크를 복사했어요');
      return;
    }
    if (g('data-print')) { openPrint(); return; }
    if (b.hasAttribute('data-doprint')) { doPrint(); return; }
    if (b.hasAttribute('data-zoom')) { ZOOM = !ZOOM; b.textContent = ZOOM ? '한 장 전체 보기' : '크게 보기'; hideTip(); fitA4(); return; }
    if (g('data-react')) {
      var k = g('data-react'); if (S.react[ITEM_ID] === k) delete S.react[ITEM_ID]; else S.react[ITEM_ID] = k; save('react'); reactBtns();
      if (S.react[ITEM_ID] === 'bad') fbSheet(); else if (S.react[ITEM_ID] === 'good') toast('도움이 됐다니 다행이에요');
      return;
    }
    if (b.hasAttribute('data-fbopen')) { fbSheet(); return; }
    if (g('data-fbtype')) { fbType = g('data-fbtype'); $$('[data-fbtype]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-fbtype') === fbType)); }); return; }
    if (b.id === 'fbsend') {
      var v = $('#fbtext').value; if (!CHECK(v).ok) { fbValidate(); return; }
      S.myfb.push({ id: 'fb-' + Math.random().toString(36).slice(2, 14), contentId: ITEM_ID, type: fbType, text: v.trim(), date: today() }); save('myfb');
      closeLayer(); fbCount(); toast('고마워요! 반영되면 알려 드릴게요'); return;
    }
    if (g('data-req')) { reqSheet(g('data-req')); return; }
    if (g('data-reqtoggle')) { var id = g('data-reqtoggle'), j = S.reqs.indexOf(id); if (j >= 0) S.reqs.splice(j, 1); else S.reqs.push(id); save('reqs'); closeLayer(); markReqPills(); toast(j >= 0 ? '요청을 취소했어요' : '요청했어요! 올라오면 알려 드릴게요'); return; }
    if (g('data-seg')) { seg = g('data-seg'); renderSaved(); return; }
  });
  document.addEventListener('input', function (e) { if (e.target.id === 'fbtext') fbValidate(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && $('#layer').innerHTML) closeLayer(); });

  initSearch(); initManual(); renderSaved(); markReqPills();
})();
