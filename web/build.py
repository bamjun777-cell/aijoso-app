# -*- coding: utf-8 -*-
"""AI 업무 레시피 웹사이트 생성기.
앱과 같은 콘텐츠 파일(app/src/main/assets/content.json)로 정적 웹사이트(site/)를 만든다.
- 매뉴얼마다 별도 페이지 → 네이버·구글 검색에 노출
- 서버 없음: GitHub Pages(무료)에 그대로 올림
사용: python3 web/build.py [--site-url https://아이디.github.io/저장소]
"""
import argparse, html, json, os, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / 'web'
# 고칠 때마다 바뀌는 버전 꼬리표 → 브라우저가 예전 CSS·JS를 쓰지 않고 새로 받음
import hashlib
VER = hashlib.sha1(b''.join(f.read_bytes() for f in sorted((ROOT / 'app/src/main/assets').glob('*.json')) + [ROOT / 'web/static/style.css', ROOT / 'web/static/app.js', ROOT / 'web/build.py'])).hexdigest()[:8]
CONTENT = ROOT / 'app/src/main/assets/content.json'

ap = argparse.ArgumentParser()
ap.add_argument('--site-url', default=os.environ.get('SITE_URL', ''))
ap.add_argument('--out', default=str(ROOT / 'site'))
args = ap.parse_args()
SITE_URL = args.site_url.rstrip('/')
# 스토어·개인정보처리방침에 공개하는 문의 메일 (정해지면 여기만 바꾸면 됨)
CONTACT_EMAIL = ''
POLICY_DATE = '2026-11-09'
OUT = Path(args.out)

UI_ALL = json.load(open(ROOT / 'app/src/main/assets/ui.json', encoding='utf-8'))
LANGS = UI_ALL['langs']
PREFIX = {'ko': '', 'en': 'en/', 'ja': 'ja/', 'zh-Hans': 'zh-hans/', 'zh-Hant': 'zh-hant/'}
FONTS = {  # 언어별 글꼴 (Google Fonts). 한국어는 기존 그대로
  'ko': 'family=Black+Han+Sans&family=Gothic+A1:wght@400;500;700;800',
  'en': 'family=Black+Han+Sans&family=Gothic+A1:wght@400;500;700;800',
  'ja': 'family=Noto+Sans+JP:wght@400;500;700;900',
  'zh-Hans': 'family=Noto+Sans+SC:wght@400;500;700;900',
  'zh-Hant': 'family=Noto+Sans+TC:wght@400;500;700;900',
}
e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
br = lambda s: e(s).replace('\n', '<br>')

def setup(code):
    """언어 하나의 콘텐츠·문구를 전역으로 올린다 (아래 화면 함수들이 이 값을 씀)"""
    global LANG, C, ITEMS, PUB, BY, CAT, CATS, TAGLINE, INDEX
    LANG = code
    C = json.load(open(ROOT / 'app/src/main/assets' / ('content.json' if code == 'ko' else f'content.{code}.json'), encoding='utf-8'))
    ITEMS = C['items']
    PUB = [i for i in ITEMS if i.get('status') == 'published']
    BY = {i['id']: i for i in ITEMS}
    CAT = {c['id']: c['name'] for c in C['categories']}
    CATS = sorted(C['categories'], key=lambda c: c.get('order', 0))
    TAGLINE = T('app.tagline')
    INDEX = [{'id': i['id'], 'title': i['title'], 'subtitle': i.get('subtitle', ''), 'category': i.get('category', ''),
              'difficulty': i.get('difficulty', ''), 'status': i.get('status', 'draft'),
              'before': i.get('timeBeforeMin', 0), 'after': i.get('timeAfterMin', 0), 'terms': terms(i)} for i in ITEMS]

def T(key, **a):
    m = UI_ALL['strings'].get(key, {})
    s = m.get(LANG) or m.get('en') or m.get('ko') or key
    for k, v in a.items(): s = s.replace('{' + k + '}', str(v))
    return s

def DIFFL(d): return T('diff.' + d) if d else ''
def freq(f): return T('freq.' + (f or '수시'))

# ── 검색용 단어 (앱의 Searcher와 같은 규칙) ──
SPLIT = re.compile(r'[\s·,()+→↔:/]+')
STOP = {'the', 'and', 'for', 'with', 'from', 'into', 'your', 'you', 'all', 'one', 'out', 'get', 'how', 'what', 'are', 'can', 'this', 'that', 'takes', 'forever'}
_ascii = lambda w: all(ord(c) < 128 for c in w)
def _hit(t, x):
    if _ascii(t): return re.search(r'(^|[^a-z0-9])' + re.escape(t) + (r'($|[^a-z0-9])' if len(t) <= 3 else ''), x) is not None
    return t in x
_useful = lambda w: len(w) > 1 and not (_ascii(w) and (len(w) < 3 or w in STOP))
def terms(it):
    title = it['title'].lower()
    t = list(dict.fromkeys(list(it.get('tags', [])) + [w for w in SPLIT.split(title) if _useful(w)]))
    for k, vs in C.get('synonyms', {}).items():
        grp = [k] + vs
        if any(w.lower() in t or _hit(w.lower(), title) for w in grp):
            for w in grp:
                if w not in t: t.append(w)
    return t

ICON = {
  'home': '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
  'search': '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
  'prompt': '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h5"/>',
  'saved': '<path d="M6 3h12v18l-6-4-6 4z"/>',
  'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
  'copy': '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
  'ext': '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  'print': '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>',
  'down': '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
  'star': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
  'share': '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 11l7.6-3.8M8.2 13l7.6 3.8"/>',
  'close': '<path d="M6 6l12 12M18 6L6 18"/>',
  'excel': '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 10h16M4 15h16M10 4v16"/>',
  'hr': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c2 .8 3.2 2.6 3.5 5.2"/>',
  'admin': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 12h18"/>',
  'account': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M8 15h2M12 15h2M16 11v4"/>',
  'report': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
  'gsheet': '<path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7v6H9zM12.5 11v6M9 14h7"/>',
  'sales': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  'logistics': '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
}
def svg(k, cls=''): return f'<svg class="i {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

NAV = [('home', 'tab.home', 'index.html'), ('search', 'tab.search', 'search.html'), ('prompt', 'tab.prompts', 'prompts.html'), ('saved', 'tab.saved', 'saved.html')]
ICON['globe'] = '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>'

AVAIL = {c: {i['id'] for i in json.load(open(ROOT / 'app/src/main/assets' / ('content.json' if c == 'ko' else f'content.{c}.json'), encoding='utf-8'))['items'] if i.get('status') == 'published'} for c in LANGS}

def page(path, title, desc, body, active='', jsonld=None):
    """path: 언어 폴더 기준 경로 (예: m/x.html). 상대 경로로 링크해 어느 주소에서든 동작."""
    full = PREFIX[LANG] + path
    R = '../' * full.count('/')          # 사이트 맨 위 (static·files)
    L = R + PREFIX[LANG]                  # 이 언어의 맨 위 (홈·매뉴얼)
    url = lambda code: f'{SITE_URL}/{PREFIX[code]}{path}'.replace('/index.html', '/')
    canonical = url(LANG) if SITE_URL else ''
    name = T('app.name')
    full_title = f'{title} | {name}' if title != name else f'{name} — {TAGLINE}'
    nav = ''.join(f'<a href="{L}{href}" class="nav-{k}"{" aria-current=\"page\"" if active == k else ""}>{svg(k)}<span>{e(T(key))}</span></a>' for k, key, href in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    same = path if path != '404.html' else 'index.html'
    # 다른 언어에 아직 없는 매뉴얼이면 그 언어의 홈으로
    def target(c):
        mid = path[2:-5] if path.startswith('m/') else None
        return 'index.html' if (path == '404.html' or (mid and mid not in AVAIL[c])) else path
    alts = ''.join(f'<link rel="alternate" hreflang="{c}" href="{e(url(c))}">' for c in LANGS if target(c) == path) + f'<link rel="alternate" hreflang="x-default" href="{e(url("en" if target("en") == path else LANG))}">' if SITE_URL else ''
    langs = ''.join(f'<a href="{R}{PREFIX[c]}{target(c)}" hreflang="{c}" lang="{c}" data-setlang="{c}"{" aria-current=\"true\"" if c == LANG else ""}>{e(UI_ALL["names"][c])}</a>' for c in LANGS)
    cjk = ' class="cjk"' if LANG in ('ja', 'zh-Hans', 'zh-Hant') else ''
    sug = '<div id="langsuggest" class="langsug" hidden></div>' if LANG == 'ko' else ''
    return f"""<!doctype html>
<html lang="{LANG}"{cjk}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
{f'<link rel="canonical" href="{e(canonical)}">' if canonical else ''}
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(name)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
{f'<meta property="og:url" content="{e(canonical)}">' if canonical else ''}
<meta name="theme-color" content="#FFD23F">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[LANG]}&display=swap">
<link rel="stylesheet" href="{R}static/style.css?v={VER}">
{ld}
</head>
<body data-root="{R}" data-lroot="{L}">
<a class="skip" href="#main">{e(T('a11y.skip'))}</a>
{sug}
<header class="top"><div class="wrap topin">
  <a class="logo" href="{L}index.html"><b>{e(name)}</b><small>{e(TAGLINE)}</small></a>
  <nav class="topnav" aria-label="{e(T('a11y.mainmenu'))}">{nav}<a href="{L}about.html" class="nav-info"{' aria-current="page"' if active == 'info' else ''}>{svg('info')}<span>{e(T('nav.about'))}</span></a></nav>
  <details class="langmenu"><summary aria-label="{e(T('web.lang'))}">{svg('globe')}<span>{e(UI_ALL["names"][LANG])}</span></summary><div class="langlist">{langs}</div></details>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <p><b>{e(name)}</b> · {e(TAGLINE)}</p>
  <p>{e(T('web.footer'))}</p>
  <p><a href="{L}about.html">{e(T('web.aboutLink'))}</a> · <a href="{L}privacy.html">{e(T('pp.title'))}</a> · {e(T('web.contentVer', n=C.get("contentVersion","")))}</p>
  <p class="footlangs">{langs}</p>
</div></footer>
<nav class="tabs" aria-label="{e(T('a11y.bottommenu'))}">{nav}</nav>
<div id="layer"></div>
<script src="{R}static/data.{LANG}.js?v={VER}"></script>
<script src="{R}static/app.js?v={VER}"></script>
</body>
</html>
"""

def mins(n): return T('min.n', n=n)

def card(it, L):
    pub = it.get('status') == 'published'
    href = f'{L}m/{it["id"]}.html' if pub else '#'
    meta = f'<span class="pill">{e(CAT.get(it.get("category"), ""))}</span><span class="pill">{e(T("diff.label"))} {e(DIFFL(it.get("difficulty")))}</span>'
    if pub:
        meta += f'<span class="pill save">{e(mins(it.get("timeBeforeMin")))} → {e(mins(it.get("timeAfterMin")))}</span>'
        return f'<a class="card pub" href="{href}"><h3>{e(it["title"])}</h3><p>{br(it.get("subtitle", ""))}</p><div class="meta">{meta}</div></a>'
    meta += '<span class="pill draft" data-reqpill="' + e(it['id']) + '">' + e(T('pill.draft')) + '</span>'
    return f'<button type="button" class="card draft" data-req="{e(it["id"])}"><h3>{e(it["title"])}</h3><div class="meta">{meta}</div></button>'

def cat_grid(L, jump=False):
    out = []
    for c in CATS:
        n = sum(1 for i in ITEMS if i.get('category') == c['id'])
        name = e(c['name']).replace('·', '·<wbr>')
        out.append(f'<a class="cat" href="{"#sec-" + c["id"] if jump else L + "c/" + c["id"] + ".html"}">{svg(c["id"])}<span>{name}</span><b>{e(T("count.n", n=n))}</b></a>')
    return '<div class="cats">' + ''.join(out) + '</div>'

def search_form(L, value='', big=False):
    return f"""<form class="searchbox{' big' if big else ''}" action="{L}search.html" method="get" role="search">
  <input name="q" id="q" value="{e(value)}" placeholder="{e(T('search.placeholder.web'))}" autocomplete="off" aria-label="{e(T('search.aria'))}" enterkeyhint="search">
  <button type="submit">{e(T('search.button'))}</button></form>"""

# ───────── 홈 ─────────
def build_home():
    L = ''
    chips = ''.join(f'<a class="chip" href="search.html?q={e(q)}">{e(q)}</a>' for q in UI_ALL['chips'][LANG])
    news = ''.join(f'<li><span class="num">{e(x["date"][5:].replace("-", "."))}</span>{e(x["text"])}</li>' for x in C.get('changelog', []))
    drafts = [i for i in ITEMS if i.get('status') != 'published']
    groups = ''
    for c in CATS:
        its = [i for i in PUB if i.get('category') == c['id']]
        if not its: continue
        groups += (f'<section class="catsec" id="sec-{c["id"]}"><div class="cath">{svg(c["id"])}<h2>{e(c["name"])}</h2>'
                   f'<span class="num">{e(T("count.n", n=len(its)))}</span></div><div class="grid">{"".join(card(i, L) for i in its)}</div></section>')
    side = (f"""<div><div class="sh"><h2>{e(T('home.drafts'))}</h2><span>{e(T('home.draftsAside', n=len(drafts)))}</span></div>
      <p class="note">{e(T('home.draftsNote'))}</p>
      <div class="grid narrow">{''.join(card(i, L) for i in drafts[:6])}</div></div>""" if drafts else '')
    body = f"""
<section class="hero"><div class="wrap">
  <h1>{br(T('hero.title'))}</h1>
  <p>{e(T('hero.sub'))}</p>
  {search_form(L, big=True)}
  <div class="chips">{chips}</div>
</div></section>
<div class="wrap">
  <section><div class="sh"><h2>{e(T('home.byCategory'))}</h2><span>{e(T('home.byCategoryHint'))}</span></div>{cat_grid(L, jump=True)}</section>
  <div class="sh allh"><h2>{e(T('home.all'))}</h2><span>{e(T('home.total', n=len(PUB)))}</span></div>
  {groups}
  <section class="two{' one' if not side else ''}">
    <div><div class="sh"><h2>{e(T('home.news'))}</h2></div><ul class="news">{news}</ul></div>
    {side}
  </section>
</div>"""
    ld = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': T('app.name'), 'description': TAGLINE, 'inLanguage': LANG,
          **({'url': f'{SITE_URL}/{PREFIX[LANG]}'} if SITE_URL else {})}
    return page('index.html', T('app.name'), T('web.homeDesc'), body, 'home', ld)

# ───────── 찾기 ─────────
def build_search():
    body = f"""<div class="wrap">
  <section class="pagehead"><h1>{e(T('search.title'))}</h1>{search_form('')}</section>
  <div class="filters" role="group" aria-label="{e(T('filter.area'))}"><button type="button" class="f" data-fcat="" aria-pressed="true">{e(T('filter.all'))}</button>{''.join(f'<button type="button" class="f" data-fcat="{c["id"]}" aria-pressed="false">{e(c["name"])}</button>' for c in CATS)}</div>
  <div class="filters" role="group" aria-label="{e(T('diff.label'))}"><button type="button" class="f" data-fdiff="" aria-pressed="true">{e(T('diff.all'))}</button>{''.join(f'<button type="button" class="f" data-fdiff="{d}" aria-pressed="false">{e(T("diff." + d))}</button>' for d in ('easy', 'normal', 'hard'))}</div>
  <p class="count" id="count" aria-live="polite">{e(T('home.total', n=len(ITEMS)))}</p>
  <div class="grid" id="results">{''.join(card(i, '') for i in sorted(ITEMS, key=lambda x: x.get('status') != 'published'))}</div>
</div>"""
    return page('search.html', T('search.title'), T('search.desc'), body, 'search')

# ───────── 분야 ─────────
def build_category(c):
    L = '../'
    its = sorted([i for i in ITEMS if i.get('category') == c['id']], key=lambda x: x.get('status') != 'published')
    body = f"""<div class="wrap">
  <nav class="crumb"><a href="{L}index.html">{e(T('crumb.home'))}</a> › {e(c["name"])}</nav>
  <section class="pagehead"><h1>{e(T('cat.title', name=c["name"]))}</h1><p class="note">{e(T('cat.count', a=len([i for i in its if i.get("status") == "published"]), b=len(its)))}</p></section>
  <div class="grid">{''.join(card(i, L) for i in its)}</div>
</div>"""
    names = ', '.join(i['title'] for i in its[:5])
    return page(f'c/{c["id"]}.html', T('cat.titleSeo', name=c['name']), T('cat.desc', name=c['name'], q=names), body, '')

# ───────── 매뉴얼 ─────────
def prompt_block(it, p):
    vars_html = ''.join(f"""<div class="var"><label for="v-{e(p["id"])}-{i}">{e(v["label"])}</label>
      <input id="v-{e(p["id"])}-{i}" data-var="{e(it["id"])}.{e(v["key"])}" data-pid="{e(p["id"])}" placeholder="{e(T('prompt.example', name=v["example"]))}" autocomplete="off"></div>""" for i, v in enumerate(p.get('variables', [])))
    body = e(p['body'])
    prev = re.sub(r'\{\{(.+?)\}\}', lambda m: f'<mark data-k="{m.group(1)}">{e(next((v["example"] for v in p["variables"] if v["key"] == html.unescape(m.group(1))), m.group(1)))}</mark>', body)
    return f"""<div class="prompt" id="p-{e(p["id"])}">
  <div class="ph"><h3>{e(p["title"])}</h3><small>{e(p.get("howTo", ""))}</small></div>
  {f'<div class="vars">{vars_html}</div>' if vars_html else ''}
  <div class="preview" data-prev="{e(p["id"])}">{prev}</div>
  <div class="pact"><button type="button" class="btn copy" data-copy="{e(p["id"])}">{svg('copy')} {e(T('prompt.copy'))}</button>
  <a class="btn ghost" href="https://claude.ai/new" target="_blank" rel="noopener">{svg('ext')} {e(T('prompt.openClaude'))}</a></div>
</div>"""

def build_manual(it):
    L = '../'
    R = '../' * (PREFIX[LANG] + 'm/x').count('/')
    sec = []
    def block(sid, title, inner):
        sec.append((sid, title))
        return f'<section class="block" id="{sid}"><h2><span class="n">{len(sec)}</span>{e(title)}</h2>{inner}</section>'
    tools = ''.join(f'<li class="tool"><span class="tag {"free" if t.get("free") else "own"}">{e(T("tool.free") if t.get("free") else T("tool.own"))}</span><div><b>{e(t["name"])}</b><small>{e(t.get("note", ""))}</small></div></li>' for t in it.get('tools', []))
    prep = ''.join(f'<li>{e(x)}</li>' for x in it.get('prepare', []))
    parts = [
        block('prob', T('sec.prob'), f'<p class="lead">{e(it.get("problem"))}</p>'),
        block('how', T('sec.how'), f'<div class="ba"><div><b>{e(T("how.before"))}</b>{e(it.get("before"))}</div><div class="after"><b>{e(T("detail.after"))}</b>{e(it.get("after"))}</div></div>'),
        block('prep', T('sec.prep'), f'<ul class="tools">{tools}</ul><ul class="check">{prep}</ul>'),
    ]
    pr = it.get('project')
    if pr:
        intro = e(T('proj.intro', name='\x00')).replace('\x00', f'<b>{e(pr["name"])}</b>')
        parts.append(block('proj', T('sec.proj'), f"""<div class="projbox"><p>{intro}</p>
<pre id="projtext">{e(pr["instructions"])}</pre>
<p class="note">{e(T('proj.knowledge', name=", ".join(pr.get("knowledge", []))))}</p>
<button type="button" class="btn ghost" data-copyproj="1">{svg('copy')} {e(T('proj.copy'))}</button></div>"""))
    parts.append(block('prompt', T('sec.prompt'), f'<p class="note">{e(T("prompt.hintWeb"))}</p>' + ''.join(prompt_block(it, p) for p in it.get('prompts', []))))
    def step_li(s):
        chk = f'<em>{e(T("step.check", name=s["check"]))}</em>' if s.get('check') else ''
        return f'<li><div><b>{e(s["title"])}</b><span>{e(s.get("body", ""))}</span>{chk}</div></li>'
    steps = ''.join(step_li(s) for s in it.get('steps', []))
    parts.append(block('steps', T('sec.steps'), f'<ol class="steps">{steps}</ol>'))
    r = it.get('result') or {}
    files = ''.join(f'<a class="file" href="{R}{e(f["path"])}" download="{e(f["name"])}">{svg("down")}<span><b>{e(f["name"])}</b><small>{e(f.get("note", ""))}</small></span></a>' for f in it.get('sampleFiles', []))
    res_inner = f'<p class="lead"><b>{br(r.get("summary", ""))}</b></p><div class="result">{br(r.get("example", ""))}</div>'
    if it.get('printSample'):
        res_inner += f'<div class="pact"><button type="button" class="btn copy" data-print="{e(it["id"])}">{svg("print")} {e(T("result.print"))}</button></div>'
    if files:
        res_inner += f'<div class="files"><p class="note">{e(T("result.files"))}</p>{files}</div>'
    parts.append(block('result', T('sec.result'), res_inner))
    lg = it.get('legal')
    legal = f'<div class="legal"><b>{e(T("legal.label"))}</b> {e(lg["note"])}<br>{e(T("legal.checked", d=lg["checkedAt"]))} · {e(lg["disclaimer"])}</div>' if lg else ''
    parts.append(block('caution', T('sec.caution'), f'<ul class="caution">{"".join(f"<li>{e(c)}</li>" for c in it.get("cautions", []))}</ul>{legal}'))
    docs = ''.join(f'<a class="doc" href="{e(d["url"])}" target="_blank" rel="noopener"><b>{e(d["title"])}</b><small>{e(d.get("publisher", ""))} · {e(T("detail.verified", d=d.get("verifiedAt", "")))}</small></a>' for d in it.get('docs', []))
    parts.append(block('ref', T('sec.ref'), f'<p class="note">{e(T("ref.videos"))}</p>{docs}'))
    parts.append(block('fb', T('sec.fb'), f"""<div class="react" role="group" aria-label="{e(T('react.aria'))}"><button type="button" class="f" data-react="good" aria-pressed="false">{e(T('react.good'))}</button><button type="button" class="f" data-react="bad" aria-pressed="false">{e(T('react.bad'))}</button></div>
<button type="button" class="btn ghost wide" data-fbopen="1">{e(T('fb.open'))}</button><p class="note" id="fbcount"></p>"""))
    toc = ''.join(f'<a href="#{sid}">{e(t)}</a>' for sid, t in sec)
    facts = f"""<div class="facts"><div><i>{e(T('diff.label'))}</i>{e(DIFFL(it.get("difficulty")))}</div><div><i>{e(T('detail.repeat'))}</i>{e(freq(it.get("frequency")))}</div><div><i>{e(T('detail.freePlan'))}</i>{e(T('detail.freeYes') if it.get("freePlanOk") else T('detail.freeNo'))}</div></div>"""
    body = f"""<div data-item="{e(it["id"])}">
<section class="dhead"><div class="wrap">
  <nav class="crumb"><a href="{L}index.html">{e(T('crumb.home'))}</a> › <a href="{L}c/{e(it["category"])}.html">{e(CAT.get(it["category"], ""))}</a></nav>
  <h1>{e(it["title"])}</h1>
  <p class="sub">{br(it.get("subtitle", ""))}</p>
  <div class="save-box num" aria-label="{e(T('detail.timeAria'))}"><div><span>{e(T('detail.now'))}</span><b><s>{e(mins(it.get("timeBeforeMin")))}</s></b></div><div aria-hidden="true">→</div><div><span>{e(T('detail.after'))}</span><b>{e(mins(it.get("timeAfterMin")))}</b></div></div>
  {facts}
  <p class="note">{e(T('detail.estimate'))} · {e(T('detail.verified', d=it.get("verifiedAt", "")))}</p>
  <div class="hact"><button type="button" class="btn copy" data-fav="1">{svg('star')} <span>{e(T('fav.add'))}</span></button><button type="button" class="btn ghost" data-share="1">{svg('share')} {e(T('share.web'))}</button></div>
</div></section>
<div class="wrap manual">
  <nav class="toc" aria-label="{e(T('web.toc'))}">{toc}</nav>
  <article class="content">{''.join(parts)}</article>
</div></div>"""
    desc = T('web.manualDesc', t=it['title'], p=it.get('problem', ''), a=it.get('timeBeforeMin'), b=it.get('timeAfterMin'))
    ld = {'@context': 'https://schema.org', '@type': 'HowTo', 'name': it['title'], 'description': it.get('problem', ''), 'inLanguage': LANG,
          'totalTime': f'PT{it.get("timeAfterMin", 0)}M',
          'tool': [{'@type': 'HowToTool', 'name': t['name']} for t in it.get('tools', [])],
          'step': [{'@type': 'HowToStep', 'name': s['title'], 'text': s.get('body', '')} for s in it.get('steps', [])]}
    return page(f'm/{it["id"]}.html', it['title'], desc, body, '', ld)

# ───────── 프롬프트 모음 ─────────
def build_prompts():
    out = []
    for c in CATS:
        its = [i for i in PUB if i.get('category') == c['id']]
        if not its: continue
        rows = ''.join(f"""<div class="pitem"><h3>{e(p["title"])}</h3><p>{e(it["title"])} · {e(p.get("howTo", ""))}</p>
<div class="pact"><button type="button" class="btn copy" data-qcopy="{e(it["id"])}|{e(p["id"])}">{svg('copy')} {e(T('prompt.copyShort'))}</button><a class="btn ghost" href="m/{e(it["id"])}.html#p-{e(p["id"])}">{e(T('prompt.fill'))}</a></div></div>""" for it in its for p in it.get('prompts', []))
        out.append(f'<section><div class="sh"><h2>{e(c["name"])}</h2></div><div class="grid">{rows}</div></section>')
    n = sum(len(i.get('prompts', [])) for i in PUB)
    body = f"""<div class="wrap"><section class="pagehead"><h1>{e(T('prompts.title'))}</h1><p class="note">{e(T('prompts.noteN', n=n))}</p></section>{''.join(out)}</div>"""
    return page('prompts.html', T('prompts.title'), T('prompts.desc'), body, 'prompt')

# ───────── 보관함 ─────────
def build_saved():
    body = f"""<div class="wrap"><section class="pagehead"><h1>{e(T('saved.title'))}</h1></section>
<div class="seg" role="group" aria-label="{e(T('saved.kind'))}"><button type="button" data-seg="fav" aria-pressed="true">{e(T('saved.fav'))}</button><button type="button" data-seg="recent" aria-pressed="false">{e(T('saved.recent'))}</button><button type="button" data-seg="fb" aria-pressed="false">{e(T('saved.fb'))}</button></div>
<div class="grid" id="savedlist"></div>
<p class="note">{e(T('saved.noteWeb'))}</p></div>"""
    return page('saved.html', T('saved.title'), T('saved.desc'), body, 'saved')

# ───────── 소개·개인정보 ─────────
def build_about():
    body = f"""<div class="wrap prose"><section class="pagehead"><h1>{e(T('about.title'))}</h1></section>
<p><b>{e(TAGLINE)}.</b> {e(T('about.intro'))}</p>
<h2>{e(T('about.principles'))}</h2>
<ul><li>{e(T('about.p1'))}</li><li>{e(T('about.p2'))}</li><li>{e(T('about.p3'))}</li><li>{e(T('about.p4'))}</li></ul>
<h2>{e(T('about.privacy'))}</h2>
<ul><li>{e(T('about.v1'))}</li><li>{T('about.v2')}</li><li>{e(T('about.v3'))}</li><li>{e(T('about.v4'))}</li></ul>
<h2>{e(T('about.aff'))}</h2>
<p>{e(T('about.affBody'))}</p>
<h2>{e(T('about.use'))}</h2>
<p>{e(T('about.useBody'))}</p>
<h2>{e(T('about.lawBasis'))}</h2>
<p>{e(T('about.lawBasisBody'))}</p>
<p class="note">{e(T('about.effective', d=C.get("updatedAt", ""), n=C.get("contentVersion", "")))}</p></div>"""
    return page('about.html', T('about.metaTitle'), T('about.desc'), body, 'info')

def build_privacy():
    email = CONTACT_EMAIL or T('pp.emailPending')
    secs = ''.join(f"<h2>{e(T(f'pp.h{i}'))}</h2><p>{e(T(f'pp.b{i}', email=email))}</p>" for i in range(1, 8))
    body = f"""<div class="wrap prose"><section class="pagehead"><h1>{e(T('pp.title'))}</h1></section>
<p>{e(T('pp.intro'))}</p>{secs}
<p class="note">{e(T('pp.effective', d=POLICY_DATE))}</p></div>"""
    return page('privacy.html', T('pp.title'), T('pp.desc'), body, '')

def build_404():
    body = f"""<div class="wrap"><div class="empty"><b>{e(T('web.notFound'))}</b><p>{e(T('web.notFoundBody'))}</p><p><a class="btn copy" href="./index.html">{e(T('web.toHome'))}</a></p></div></div>"""
    return page('404.html', T('web.notFound'), T('web.notFound'), body)

# ───────── 쓰기 ─────────
if OUT.exists(): shutil.rmtree(OUT)
(OUT / 'static').mkdir(parents=True)
def w(path, text):
    f = OUT / path; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(text, encoding='utf-8')
all_pages = []
for code in LANGS:
    setup(code)
    pre = PREFIX[code]
    w(pre + 'index.html', build_home()); w(pre + 'search.html', build_search()); w(pre + 'prompts.html', build_prompts())
    w(pre + 'saved.html', build_saved()); w(pre + 'about.html', build_about()); w(pre + 'privacy.html', build_privacy())
    if code == 'ko': w('404.html', build_404())
    for c in CATS: w(f'{pre}c/{c["id"]}.html', build_category(c))
    for it in PUB: w(f'{pre}m/{it["id"]}.html', build_manual(it))
    DATA = {'lang': code, 'contentVersion': C.get('contentVersion'), 'categories': CATS, 'index': INDEX,
            'items': {i['id']: {k: i.get(k) for k in ('title', 'prompts', 'project', 'printSample', 'subtitle')} for i in PUB},
            'feedback': C.get('feedback'), 'moderation': C.get('moderation'), 'resolvedFeedback': C.get('resolvedFeedback', []),
            'ui': {k: (v.get(code) or v.get('en')) for k, v in UI_ALL['strings'].items() if not k.startswith('about.')},
            'suggest': {c2: UI_ALL['strings']['web.langSuggest'][c2] for c2 in LANGS} if code == 'ko' else {}}
    w(f'static/data.{code}.js', 'window.AIJ=' + json.dumps(DATA, ensure_ascii=False, separators=(',', ':')) + ';\n')
    all_pages += [pre + x for x in ['index.html', 'search.html', 'prompts.html', 'about.html', 'privacy.html'] + [f'c/{c["id"]}.html' for c in CATS] + [f'm/{i["id"]}.html' for i in PUB]]
for f in ('style.css', 'app.js'): shutil.copy(WEB / 'static' / f, OUT / 'static' / f)
shutil.copytree(WEB / 'files', OUT / 'files')
w('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><rect width="108" height="108" rx="24" fill="#FFD23F"/><path fill="#1C1B17" d="M37,28 L63,28 L75,40 L75,76 Q75,80 71,80 L37,80 Q33,80 33,76 L33,32 Q33,28 37,28 Z"/><path d="M43,56 L51,64 L66,48" fill="none" stroke="#FFD23F" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
w('.nojekyll', '')
if SITE_URL:
    w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      ''.join(f'  <url><loc>{SITE_URL}/{p.replace("index.html", "")}</loc><lastmod>{C.get("updatedAt", "")}</lastmod></url>\n' for p in all_pages) + '</urlset>\n')
    w('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
else:
    w('robots.txt', 'User-agent: *\nAllow: /\n')
print(f'site built: {len(all_pages)} pages in {len(LANGS)} languages → {OUT}')
