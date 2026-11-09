# -*- coding: utf-8 -*-
"""AI 좋소 웹사이트 생성기.
앱과 같은 콘텐츠 파일(app/src/main/assets/content.json)로 정적 웹사이트(site/)를 만든다.
- 매뉴얼마다 별도 페이지 → 네이버·구글 검색에 노출
- 서버 없음: GitHub Pages(무료)에 그대로 올림
사용: python3 web/build.py [--site-url https://아이디.github.io/저장소]
"""
import argparse, html, json, os, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / 'web'
CONTENT = ROOT / 'app/src/main/assets/content.json'

ap = argparse.ArgumentParser()
ap.add_argument('--site-url', default=os.environ.get('SITE_URL', ''))
ap.add_argument('--out', default=str(ROOT / 'site'))
args = ap.parse_args()
SITE_URL = args.site_url.rstrip('/')
OUT = Path(args.out)

C = json.load(open(CONTENT, encoding='utf-8'))
ITEMS = C['items']
PUB = [i for i in ITEMS if i.get('status') == 'published']
BY = {i['id']: i for i in ITEMS}
CAT = {c['id']: c['name'] for c in C['categories']}
CATS = sorted(C['categories'], key=lambda c: c.get('order', 0))
DIFF = {'easy': '쉬움', 'normal': '보통', 'hard': '어려움'}
TAGLINE = '작은 회사의 큰 업무를 가볍게'
e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
br = lambda s: e(s).replace('\n', '<br>')

def freq(f): return '수시' if (not f or f == '수시') else '매' + f

# ── 검색용 단어 (앱의 Searcher와 같은 규칙) ──
SPLIT = re.compile(r'[\s·,()+→↔]+')
def terms(it):
    t = list(dict.fromkeys(list(it.get('tags', [])) + [w for w in SPLIT.split(it['title']) if len(w) > 1]))
    for k, vs in C.get('synonyms', {}).items():
        grp = [k] + vs
        if any(w in t or w in it['title'] for w in grp):
            for w in grp:
                if w not in t: t.append(w)
    return t

INDEX = [{'id': i['id'], 'title': i['title'], 'subtitle': i.get('subtitle', ''), 'category': i.get('category', ''),
          'difficulty': i.get('difficulty', ''), 'status': i.get('status', 'draft'),
          'before': i.get('timeBeforeMin', 0), 'after': i.get('timeAfterMin', 0), 'terms': terms(i)} for i in ITEMS]

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

NAV = [('home', '홈', 'index.html'), ('search', '찾기', 'search.html'), ('prompt', '프롬프트', 'prompts.html'), ('saved', '보관함', 'saved.html')]

def page(path, title, desc, body, active='', jsonld=None):
    """path: 사이트 루트 기준 경로 (예: m/x.html). 상대 경로로 링크해 어느 주소에서든 동작."""
    depth = path.count('/')
    R = '../' * depth
    canonical = f'{SITE_URL}/{path}'.replace('/index.html', '/') if SITE_URL else ''
    full_title = f'{title} | AI 좋소' if title != 'AI 좋소' else f'AI 좋소 — {TAGLINE}'
    nav = ''.join(f'<a href="{R}{href}" class="nav-{k}"{" aria-current=\"page\"" if active == k else ""}>{svg(k)}<span>{label}</span></a>' for k, label, href in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
{f'<link rel="canonical" href="{e(canonical)}">' if canonical else ''}
<meta property="og:type" content="website">
<meta property="og:site_name" content="AI 좋소">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
{f'<meta property="og:url" content="{e(canonical)}">' if canonical else ''}
<meta name="theme-color" content="#FFD23F">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Gothic+A1:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="{R}static/style.css">
{ld}
</head>
<body data-root="{R}">
<a class="skip" href="#main">본문 바로가기</a>
<header class="top"><div class="wrap topin">
  <a class="logo" href="{R}index.html"><b>AI 좋소</b><small>{TAGLINE}</small></a>
  <nav class="topnav" aria-label="주 메뉴">{nav}<a href="{R}about.html" class="nav-info"{' aria-current="page"' if active == 'info' else ''}>{svg('info')}<span>소개</span></a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <p><b>AI 좋소</b> · {TAGLINE}</p>
  <p>Claude 등 AI 도구 활용법을 안내하는 독립 서비스로, Anthropic·OpenAI·Google 등 AI 회사와 제휴하거나 승인받은 관계가 없습니다.</p>
  <p><a href="{R}about.html">소개·개인정보 안내</a> · 콘텐츠 버전 {e(C.get("contentVersion",""))}</p>
</div></footer>
<nav class="tabs" aria-label="하단 메뉴">{nav}</nav>
<div id="layer"></div>
<script src="{R}static/data.js"></script>
<script src="{R}static/app.js"></script>
</body>
</html>
'''

def card(it, R):
    pub = it.get('status') == 'published'
    href = f'{R}m/{it["id"]}.html' if pub else '#'
    meta = f'<span class="pill">{e(CAT.get(it.get("category"), ""))}</span><span class="pill">난이도 {e(DIFF.get(it.get("difficulty"), ""))}</span>'
    if pub:
        meta += f'<span class="pill save">{it.get("timeBeforeMin")}분 → {it.get("timeAfterMin")}분</span>'
        return f'<a class="card pub" href="{href}"><h3>{e(it["title"])}</h3><p>{br(it.get("subtitle", ""))}</p><div class="meta">{meta}</div></a>'
    meta += '<span class="pill draft" data-reqpill="' + e(it['id']) + '">준비 중</span>'
    return f'<button type="button" class="card draft" data-req="{e(it["id"])}"><h3>{e(it["title"])}</h3><div class="meta">{meta}</div></button>'

def cat_grid(R):
    out = []
    for c in CATS:
        n = sum(1 for i in ITEMS if i.get('category') == c['id'])
        name = e(c['name']).replace('·', '·<wbr>')
        out.append(f'<a class="cat" href="{R}c/{c["id"]}.html">{svg(c["id"])}<span>{name}</span><b>{n}개</b></a>')
    return '<div class="cats">' + ''.join(out) + '</div>'

def search_form(R, value='', big=False):
    return f'''<form class="searchbox{' big' if big else ''}" action="{R}search.html" method="get" role="search">
  <input name="q" id="q" value="{e(value)}" placeholder="예) 매달 급여 비교하는 게 오래 걸려요" autocomplete="off" aria-label="업무 검색" enterkeyhint="search">
  <button type="submit">찾기</button></form>'''

# ───────── 홈 ─────────
def build_home():
    R = ''
    chips = ''.join(f'<a class="chip" href="search.html?q={e(q)}">{e(q)}</a>' for q in ['지점 엑셀 합치기', '급여 전월 비교', '보고서 1장 요약'])
    news = ''.join(f'<li><span class="num">{e(x["date"][5:].replace("-", "."))}</span>{e(x["text"])}</li>' for x in C.get('changelog', []))
    drafts = [i for i in ITEMS if i.get('status') != 'published']
    feat = [BY[x] for x in C.get('featured', []) if x in BY and BY[x].get('status') == 'published'] or PUB[:6]
    side = (f'''<div><div class="sh"><h2>곧 올라올 매뉴얼</h2><span>{len(drafts)}개 준비 중</span></div>
      <p class="note">먼저 보고 싶은 매뉴얼을 눌러 요청해 주세요</p>
      <div class="grid narrow">{''.join(card(i, R) for i in drafts[:6])}</div></div>''' if drafts else
      f'''<div><div class="sh"><h2>분야별 매뉴얼 수</h2></div><ul class="news">{''.join(f'<li><span class="num">{sum(1 for i in PUB if i.get("category") == c["id"])}개</span><a href="c/{c["id"]}.html">{e(c["name"])}</a></li>' for c in CATS)}</ul></div>''')
    body = f'''
<section class="hero"><div class="wrap">
  <h1>사람은 없고<br>일은 많죠?</h1>
  <p>힘든 업무를 문장으로 적어 보세요</p>
  {search_form(R, big=True)}
  <div class="chips">{chips}</div>
</div></section>
<div class="wrap">
  <section><div class="sh"><h2>분야별로 찾기</h2><span>{len(CATS)}개 분야</span></div>{cat_grid(R)}</section>
  <section><div class="sh"><h2>바로 쓰는 매뉴얼</h2><span>전체 {len(PUB)}개 공개</span></div><div class="grid">{''.join(card(i, R) for i in feat)}</div><p><a class="more" href="search.html">매뉴얼 {len(PUB)}개 모두 보기</a></p></section>
  <section class="two">
    <div><div class="sh"><h2>여러분 의견으로 바뀌었어요</h2></div><ul class="news">{news}</ul></div>
    {side}
  </section>
</div>'''
    ld = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'AI 좋소', 'description': TAGLINE,
          **({'url': SITE_URL + '/'} if SITE_URL else {})}
    return page('index.html', 'AI 좋소', '중소기업 실무자를 위한 AI 업무 자동화 매뉴얼. 엑셀·인사·회계·보고서 등 매뉴얼 30개, 복사해서 바로 쓰는 프롬프트와 따라 하기.', body, 'home', ld)

# ───────── 찾기 ─────────
def build_search():
    body = f'''<div class="wrap">
  <section class="pagehead"><h1>업무 찾기</h1>{search_form('')}</section>
  <div class="filters" role="group" aria-label="분야"><button type="button" class="f" data-fcat="" aria-pressed="true">전체</button>{''.join(f'<button type="button" class="f" data-fcat="{c["id"]}" aria-pressed="false">{e(c["name"])}</button>' for c in CATS)}</div>
  <div class="filters" role="group" aria-label="난이도"><button type="button" class="f" data-fdiff="" aria-pressed="true">난이도 전체</button><button type="button" class="f" data-fdiff="easy" aria-pressed="false">쉬움</button><button type="button" class="f" data-fdiff="normal" aria-pressed="false">보통</button><button type="button" class="f" data-fdiff="hard" aria-pressed="false">어려움</button></div>
  <p class="count" id="count" aria-live="polite">전체 {len(ITEMS)}개</p>
  <div class="grid" id="results">{''.join(card(i, '') for i in sorted(ITEMS, key=lambda x: x.get('status') != 'published'))}</div>
</div>'''
    return page('search.html', '업무 찾기', '업무 이름이나 문장으로 AI 업무 자동화 매뉴얼을 찾아보세요.', body, 'search')

# ───────── 분야 ─────────
def build_category(c):
    R = '../'
    its = sorted([i for i in ITEMS if i.get('category') == c['id']], key=lambda x: x.get('status') != 'published')
    body = f'''<div class="wrap">
  <nav class="crumb"><a href="{R}index.html">홈</a> › {e(c["name"])}</nav>
  <section class="pagehead"><h1>{e(c["name"])} 자동화</h1><p class="note">{len([i for i in its if i.get("status") == "published"])}개 공개 · {len(its)}개 전체</p></section>
  <div class="grid">{''.join(card(i, R) for i in its)}</div>
</div>'''
    names = ', '.join(i['title'] for i in its[:5])
    return page(f'c/{c["id"]}.html', f'{c["name"]} 업무 자동화', f'{c["name"]} 실무자를 위한 AI 자동화 매뉴얼: {names}', body, '')

# ───────── 매뉴얼 ─────────
def prompt_block(it, p):
    vars_html = ''.join(f'''<div class="var"><label for="v-{e(p["id"])}-{i}">{e(v["label"])}</label>
      <input id="v-{e(p["id"])}-{i}" data-var="{e(it["id"])}.{e(v["key"])}" data-pid="{e(p["id"])}" placeholder="예) {e(v["example"])}" autocomplete="off"></div>''' for i, v in enumerate(p.get('variables', [])))
    body = e(p['body'])
    prev = re.sub(r'\{\{(.+?)\}\}', lambda m: f'<mark data-k="{m.group(1)}">{e(next((v["example"] for v in p["variables"] if v["key"] == html.unescape(m.group(1))), m.group(1)))}</mark>', body)
    return f'''<div class="prompt" id="p-{e(p["id"])}">
  <div class="ph"><h3>{e(p["title"])}</h3><small>{e(p.get("howTo", ""))}</small></div>
  {f'<div class="vars">{vars_html}</div>' if vars_html else ''}
  <div class="preview" data-prev="{e(p["id"])}">{prev}</div>
  <div class="pact"><button type="button" class="btn copy" data-copy="{e(p["id"])}">{svg('copy')} 복사하기</button>
  <a class="btn ghost" href="https://claude.ai/new" target="_blank" rel="noopener">{svg('ext')} Claude 열기</a></div>
</div>'''

def build_manual(it):
    R = '../'
    sec = []
    def block(sid, title, inner):
        sec.append((sid, title))
        return f'<section class="block" id="{sid}"><h2><span class="n">{len(sec)}</span>{e(title)}</h2>{inner}</section>'
    tools = ''.join(f'<li class="tool"><span class="tag {"free" if t.get("free") else "own"}">{"무료" if t.get("free") else "보유"}</span><div><b>{e(t["name"])}</b><small>{e(t.get("note", ""))}</small></div></li>' for t in it.get('tools', []))
    prep = ''.join(f'<li>{e(x)}</li>' for x in it.get('prepare', []))
    parts = [
        block('prob', '이런 문제, 있으시죠?', f'<p class="lead">{e(it.get("problem"))}</p>'),
        block('how', '이렇게 바뀝니다', f'<div class="ba"><div><b>지금 방식</b>{e(it.get("before"))}</div><div class="after"><b>AI 적용 후</b>{e(it.get("after"))}</div></div>'),
        block('prep', '필요한 것과 준비', f'<ul class="tools">{tools}</ul><ul class="check">{prep}</ul>'),
    ]
    pr = it.get('project')
    if pr:
        parts.append(block('proj', 'Claude 프로젝트로 만들어 두기', f'''<div class="projbox"><p>매달 반복된다면 <b>'{e(pr["name"])}'</b> 프로젝트를 만들고 아래 지침을 붙여넣으세요</p>
<pre id="projtext">{e(pr["instructions"])}</pre>
<p class="note">올릴 파일: {e(", ".join(pr.get("knowledge", [])))}</p>
<button type="button" class="btn ghost" data-copyproj="1">{svg('copy')} 지침 복사</button></div>'''))
    parts.append(block('prompt', '복사해서 쓰는 프롬프트', '<p class="note">빈칸을 채우면 바로 반영돼요. 입력값은 이 기기에 기억돼요.</p>' + ''.join(prompt_block(it, p) for p in it.get('prompts', []))))
    steps = ''.join(f'<li><div><b>{e(s["title"])}</b><span>{e(s.get("body", ""))}</span>{f"<em>확인 · {e(s["check"])}</em>" if s.get("check") else ""}</div></li>' for s in it.get('steps', []))
    parts.append(block('steps', '순서대로 따라 하기', f'<ol class="steps">{steps}</ol>'))
    r = it.get('result') or {}
    files = ''.join(f'<a class="file" href="{R}{e(f["path"])}" download="{e(f["name"])}">{svg("down")}<span><b>{e(f["name"])}</b><small>{e(f.get("note", ""))}</small></span></a>' for f in it.get('sampleFiles', []))
    res_inner = f'<p class="lead"><b>{br(r.get("summary", ""))}</b></p><div class="result">{br(r.get("example", ""))}</div>'
    if it.get('printSample'):
        res_inner += f'<div class="pact"><button type="button" class="btn copy" data-print="{e(it["id"])}">{svg("print")} A4 출력 미리보기·인쇄</button></div>'
    if files:
        res_inner += f'<div class="files"><p class="note">결과물 예시 파일 (가상 데이터)</p>{files}</div>'
    parts.append(block('result', '이런 결과가 나와요', res_inner))
    lg = it.get('legal')
    legal = f'<div class="legal"><b>법령 기준</b> {e(lg["note"])}<br>확인일 {e(lg["checkedAt"])} · {e(lg["disclaimer"])}</div>' if lg else ''
    parts.append(block('caution', '꼭 지켜 주세요', f'<ul class="caution">{"".join(f"<li>{e(c)}</li>" for c in it.get("cautions", []))}</ul>{legal}'))
    docs = ''.join(f'<a class="doc" href="{e(d["url"])}" target="_blank" rel="noopener"><b>{e(d["title"])}</b><small>{e(d.get("publisher", ""))} · 검증일 {e(d.get("verifiedAt", ""))}</small></a>' for d in it.get('docs', []))
    parts.append(block('ref', '더 알아보기', f'<p class="note">관련 영상은 내용 확인 후 올려요</p>{docs}'))
    parts.append(block('fb', '이 매뉴얼, 어땠나요?', f'''<div class="react" role="group" aria-label="평가"><button type="button" class="f" data-react="good" aria-pressed="false">도움 됐어요</button><button type="button" class="f" data-react="bad" aria-pressed="false">아쉬워요</button></div>
<button type="button" class="btn ghost wide" data-fbopen="1">틀린 내용 신고 · 추가 요청</button><p class="note" id="fbcount"></p>'''))
    toc = ''.join(f'<a href="#{sid}">{e(t)}</a>' for sid, t in sec)
    facts = f'''<div class="facts"><div><i>난이도</i>{e(DIFF.get(it.get("difficulty"), ""))}</div><div><i>반복</i>{e(freq(it.get("frequency")))}</div><div><i>무료 플랜</i>{"가능" if it.get("freePlanOk") else "유료"}</div></div>'''
    body = f'''<div data-item="{e(it["id"])}">
<section class="dhead"><div class="wrap">
  <nav class="crumb"><a href="{R}index.html">홈</a> › <a href="{R}c/{e(it["category"])}.html">{e(CAT.get(it["category"], ""))}</a></nav>
  <h1>{e(it["title"])}</h1>
  <p class="sub">{br(it.get("subtitle", ""))}</p>
  <div class="save-box num" aria-label="예상 소요 시간"><div><span>지금</span><b><s>{it.get("timeBeforeMin")}분</s></b></div><div aria-hidden="true">→</div><div><span>AI 적용 후</span><b>{it.get("timeAfterMin")}분</b></div></div>
  {facts}
  <p class="note">* 시간은 추정치 · 검증일 {e(it.get("verifiedAt", ""))}</p>
  <div class="hact"><button type="button" class="btn copy" data-fav="1">{svg('star')} <span>보관함에 담기</span></button><button type="button" class="btn ghost" data-share="1">{svg('share')} 공유</button></div>
</div></section>
<div class="wrap manual">
  <nav class="toc" aria-label="목차">{toc}</nav>
  <article class="content">{''.join(parts)}</article>
</div></div>'''
    desc = f'{it["title"]} — {it.get("problem", "")} {it.get("timeBeforeMin")}분 걸리던 일을 {it.get("timeAfterMin")}분으로. 복사해서 쓰는 Claude 프롬프트와 단계별 따라 하기.'
    ld = {'@context': 'https://schema.org', '@type': 'HowTo', 'name': it['title'], 'description': it.get('problem', ''),
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
        rows = ''.join(f'''<div class="pitem"><h3>{e(p["title"])}</h3><p>{e(it["title"])} · {e(p.get("howTo", ""))}</p>
<div class="pact"><button type="button" class="btn copy" data-qcopy="{e(it["id"])}|{e(p["id"])}">{svg('copy')} 복사</button><a class="btn ghost" href="m/{e(it["id"])}.html#p-{e(p["id"])}">빈칸 채우기</a></div></div>''' for it in its for p in it.get('prompts', []))
        out.append(f'<section><div class="sh"><h2>{e(c["name"])}</h2></div><div class="grid">{rows}</div></section>')
    n = sum(len(i.get('prompts', [])) for i in PUB)
    body = f'''<div class="wrap"><section class="pagehead"><h1>프롬프트 보관함</h1><p class="note">{n}개 · 빈칸은 입력한 값, 없으면 예시로 복사돼요</p></section>{''.join(out)}</div>'''
    return page('prompts.html', '프롬프트 보관함', '복사해서 Claude에 바로 붙여넣는 업무 자동화 프롬프트 모음.', body, 'prompt')

# ───────── 보관함 ─────────
def build_saved():
    body = '''<div class="wrap"><section class="pagehead"><h1>보관함</h1></section>
<div class="seg" role="group" aria-label="보관함 종류"><button type="button" data-seg="fav" aria-pressed="true">즐겨찾기</button><button type="button" data-seg="recent" aria-pressed="false">최근 본</button><button type="button" data-seg="fb" aria-pressed="false">내 의견</button></div>
<div class="grid" id="savedlist"></div>
<p class="note">보관함은 이 브라우저에만 저장돼요. 회원가입은 없어요.</p></div>'''
    return page('saved.html', '보관함', '즐겨찾기, 최근 본 매뉴얼, 내가 남긴 의견.', body, 'saved')

# ───────── 소개·개인정보 ─────────
def build_about():
    body = f'''<div class="wrap prose"><section class="pagehead"><h1>AI 좋소 소개</h1></section>
<p><b>{TAGLINE}.</b> AI 좋소는 직원 5~300명 규모 회사의 인사·총무·회계·영업·물류 실무자가 반복 업무를 AI로 줄일 수 있도록, 업무별 따라 하기 매뉴얼과 복사해서 쓰는 프롬프트를 제공합니다.</p>
<h2>이런 원칙으로 만듭니다</h2>
<ul><li>실제 업무 기준: 기술 설명보다 "내 일이 얼마나 줄어드는지"</li><li>무료 우선: 무료 플랜으로 가능한지 매뉴얼마다 표시</li><li>검증: 공식 문서 링크와 검증일, 법령은 확인일 표시</li><li>안전: 개인정보 삭제와 결과 검산 단계를 모든 매뉴얼에 포함</li></ul>
<h2>개인정보 처리 안내</h2>
<ul><li>회원가입과 로그인이 없습니다.</li><li>즐겨찾기, 최근 본 매뉴얼, 빈칸 입력값, 남긴 의견은 <b>이용자의 브라우저(이 기기)에만</b> 저장되며 서버로 전송되지 않습니다.</li><li>현재 광고와 이용 분석 도구를 사용하지 않습니다. 도입할 경우 이 안내를 먼저 갱신합니다.</li><li>브라우저의 사이트 데이터 삭제로 언제든 지울 수 있습니다.</li></ul>
<h2>제휴 관계 고지</h2>
<p>AI 좋소는 Claude 등 AI 도구의 활용법을 안내하는 독립 서비스이며, Anthropic·OpenAI·Google 등 AI 회사와 제휴하거나 승인받은 관계가 없습니다. 각 상표는 해당 회사의 소유입니다.</p>
<h2>콘텐츠 이용 시 유의사항</h2>
<p>매뉴얼은 일반적인 업무 기준으로 작성되었습니다. AI가 만든 결과물은 반드시 원본과 대조해 검토하세요. 노무·세무 등 법령 판단은 관계 기관이나 전문가 확인이 필요합니다.</p>
<p class="note">시행일 {e(C.get("updatedAt", ""))} · 콘텐츠 버전 {e(C.get("contentVersion", ""))}</p></div>'''
    return page('about.html', '소개·개인정보 안내', 'AI 좋소 소개, 개인정보 처리 안내, 제휴 관계 고지.', body, 'info')

def build_404():
    body = '''<div class="wrap"><div class="empty"><b>페이지를 찾을 수 없어요</b><p>주소가 바뀌었거나 아직 준비 중인 매뉴얼이에요.</p><p><a class="btn copy" href="./index.html">홈으로</a></p></div></div>'''
    return page('404.html', '페이지 없음', '페이지를 찾을 수 없습니다.', body)

# ───────── 쓰기 ─────────
if OUT.exists(): shutil.rmtree(OUT)
(OUT / 'm').mkdir(parents=True); (OUT / 'c').mkdir(); (OUT / 'static').mkdir()
def w(path, text): (OUT / path).write_text(text, encoding='utf-8')
w('index.html', build_home()); w('search.html', build_search()); w('prompts.html', build_prompts())
w('saved.html', build_saved()); w('about.html', build_about()); w('404.html', build_404())
for c in CATS: w(f'c/{c["id"]}.html', build_category(c))
for it in PUB: w(f'm/{it["id"]}.html', build_manual(it))
for f in ('style.css', 'app.js'): shutil.copy(WEB / 'static' / f, OUT / 'static' / f)
shutil.copytree(WEB / 'files', OUT / 'files')
DATA = {'contentVersion': C.get('contentVersion'), 'categories': CATS, 'index': INDEX,
        'items': {i['id']: {k: i.get(k) for k in ('title', 'prompts', 'project', 'printSample', 'subtitle')} for i in PUB},
        'feedback': C.get('feedback'), 'moderation': C.get('moderation'), 'resolvedFeedback': C.get('resolvedFeedback', [])}
w('static/data.js', 'window.AIJ=' + json.dumps(DATA, ensure_ascii=False, separators=(',', ':')) + ';\n')
w('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><rect width="108" height="108" rx="24" fill="#FFD23F"/><path fill="#1C1B17" d="M37,28 L63,28 L75,40 L75,76 Q75,80 71,80 L37,80 Q33,80 33,76 L33,32 Q33,28 37,28 Z"/><path d="M43,56 L51,64 L66,48" fill="none" stroke="#FFD23F" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
w('.nojekyll', '')
pages = ['index.html', 'search.html', 'prompts.html', 'about.html'] + [f'c/{c["id"]}.html' for c in CATS] + [f'm/{i["id"]}.html' for i in PUB]
if SITE_URL:
    w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      ''.join(f'  <url><loc>{SITE_URL}/{p.replace("index.html", "")}</loc><lastmod>{C.get("updatedAt", "")}</lastmod></url>\n' for p in pages) + '</urlset>\n')
    w('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
else:
    w('robots.txt', 'User-agent: *\nAllow: /\n')
print(f'site built: {len(pages)} pages → {OUT}')
