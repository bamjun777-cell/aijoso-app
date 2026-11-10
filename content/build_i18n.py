# -*- coding: utf-8 -*-
"""다국어 콘텐츠 만들기.
원본 app/src/main/assets/content.json(한국어) + content/i18n/<언어>.py(번역·나라별 법령) →
app/src/main/assets/content.<언어>.json, ui.json (앱·웹 공통 화면 문구)
번체(zh-Hant)는 간체를 대만식으로 자동 변환한 뒤, 대만 법령 매뉴얼만 zh_Hant.py로 덮어쓴다.
사용: python3 content/build_i18n.py"""
import copy, importlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'app/src/main/assets'
sys.path.insert(0, str(ROOT / 'content/i18n'))
from opencc import OpenCC
S2TW = OpenCC('s2twp')
TW_FIX = [('新元', '元'), ('S$', 'NT$'), ('新加坡', '台灣'), ('來原始檔', '來源檔案'), ('工資表', '薪資表'), ('工資環比', '薪資環比'), ('賬', '帳'), ('髮', '發'), ('單元格', '儲存格'), ('批註', '註解'), ('合並', '合併'), ('第一行', '第一列')]
# 대만 엑셀 용어: 行(가로줄)→列, 列(세로줄)→欄. 먼저 '열'을 바꾸고(A) 다음에 '행'을 바꾼다(B). 엑셀 문맥만 골라 바꿈
TW_EXCEL_A = [(r'行列合計', '各列與各欄合計'), (r'記下行、列、值', '記下列、欄、值'), (r'列名', '欄名'), (r'列順序', '欄順序'), (r'列位置', '欄位置'), (r'列結構', '欄位結構'),
  (r'\b([A-Z]) 列', r'\1 欄'), (r'(關鍵|金額|數字|區域|司機|品號|狀態|內容|資訊|敏感|庫存)列', r'\1欄'), (r'」列', '」欄'), (r'(加|旁邊)一列', r'\1一欄'),
  (r'三列', '三欄'), (r'(比較|要比|相同|傳送)的列', r'\1的欄位'), (r'所有列', '所有欄'), (r'(\d+) 列就', r'\1 欄就'), (r'"列"', '"欄"'), (r'- 列：', '- 欄：'), (r'列是 ', '欄位是 ')]
TW_EXCEL_B = [(r'(空|重複|合計|標題)行', r'\1列'), (r'行數', '列數'), (r'行號', '列號'), (r'(文字|裡|為空|變了|重複)的行', r'\1的列'),
  (r'([\d,]{3,}) 行', r'\1 列'), (r'(\d) 行 ·', r'\1 列 ·'), (r'\}\} 行。', '}} 列。'), (r'- 行：', '- 列：'), (r'"行"', '"列"'), (r'一行標題', '一列標題'), (r'一行行', '一列列')]

def to_tw(x):
    if isinstance(x, str):
        s = S2TW.convert(x)
        for a, b in TW_FIX: s = s.replace(a, b)
        for a, b in TW_EXCEL_A + TW_EXCEL_B: s = re.sub(a, b, s)
        s = {'行': '列', '列': '欄'}.get(s, s)   # 피벗 '행/열' 칸 이름
        # 빈칸 키(한국어)는 그대로 둠
        return re.sub(r'\{\{(.+?)\}\}', lambda m: m.group(0), s)
    if isinstance(x, list): return [to_tw(i) for i in x]
    if isinstance(x, tuple): return tuple(to_tw(i) for i in x)
    if isinstance(x, dict): return {k if k in ('key', 'id') else k: (v if k in ('key', 'id', 'url', 'verifiedAt') else to_tw(v)) for k, v in x.items()}
    return x

MASTER = json.load(open(ASSETS / 'content.json', encoding='utf-8'))
VAR = re.compile(r'\{\{(.+?)\}\}')
HANGUL = re.compile(r'[가-힣]')
errors = []

def lang_module(code):
    if code == 'zh-Hant':
        base = importlib.import_module('zh_Hans'); tw = importlib.import_module('zh_Hant')
        m = type('M', (), {})()
        for k in ('CATEGORIES', 'FEEDBACK', 'CHANGELOG', 'SYNONYMS', 'MODERATION', 'ITEMS'):
            setattr(m, k, to_tw(copy.deepcopy(getattr(base, k))))
        m.SYNONYMS = {to_tw(k): v for k, v in m.SYNONYMS.items()}
        m.MODERATION = {'banned': list(dict.fromkeys(base.MODERATION['banned'] + m.MODERATION['banned'])), 'allow': m.MODERATION['allow']}
        for k, v in tw.ITEMS.items(): m.ITEMS[k] = {**m.ITEMS[k], **v}
        m.PENDING = tw.PENDING
        return m
    return importlib.import_module(code.replace('-', '_'))

def build(code):
    L = lang_module(code)
    C = copy.deepcopy(MASTER)
    C['lang'] = code
    for c in C['categories']: c['name'] = L.CATEGORIES[c['id']]
    C['synonyms'] = L.SYNONYMS
    for t in C['feedback']['types']: t['label'] = L.FEEDBACK[t['id']]
    C['moderation']['banned'] = list(dict.fromkeys(MASTER['moderation']['banned'] + L.MODERATION['banned']))
    C['moderation']['allow'] = list(dict.fromkeys(MASTER['moderation']['allow'] + L.MODERATION['allow']))
    # 업데이트 소식: 번역된 것만 (오래된 것부터 맞춤, 새 소식은 번역되면 추가)
    n = len(L.CHANGELOG)
    C['changelog'] = [dict(ch, text=t) for ch, t in zip(MASTER['changelog'][len(MASTER['changelog']) - n:], L.CHANGELOG)]
    out, missing = [], []
    for m in MASTER['items']:
        o = L.ITEMS.get(m['id'])
        if o is None: missing.append(m['id']); continue   # 아직 번역 안 된 매뉴얼은 그 언어에서 빼고 공개
        it = {k: m[k] for k in ('id', 'status', 'category', 'difficulty', 'frequency', 'timeBeforeMin', 'timeAfterMin', 'freePlanOk', 'verifiedAt', 'updatedAt')}
        it.update({'lang': code, 'title': o['t'], 'subtitle': o['s'], 'tags': o['tags'],
                   'tools': [{'name': n, 'free': mt['free'], 'note': note} for (n, note), mt in zip(o['tools'], m['tools'])],
                   'problem': o['p'], 'before': o['b'], 'after': o['a'], 'prepare': o['prep'],
                   'prompts': o['pr'], 'steps': o['st'], 'result': {'summary': o['r'][0], 'example': o['r'][1]},
                   'cautions': o['c'], 'videos': [], 'docs': o['docs']})
        if len(o['tools']) != len(m['tools']): errors.append(f'{code}/{m["id"]}: 도구 개수 다름')
        if m.get('project'):
            if not o.get('proj'): errors.append(f'{code}/{m["id"]}: 프로젝트 번역 없음')
            else: it['project'] = {'recommended': True, 'name': o['proj'][0], 'instructions': o['proj'][1], 'knowledge': o['proj'][2]}
        if m.get('legal'):
            if not o.get('legal'): errors.append(f'{code}/{m["id"]}: 법령 기준 없음')
        it['legal'] = {'note': o['legal'][0], 'checkedAt': o['legal'][1], 'disclaimer': o['legal'][2]} if o.get('legal') else None
        if [p['id'] for p in it['prompts']] != [p['id'] for p in m['prompts']] and code not in getattr(L, 'PROMPT_ID_EXCEPTIONS', []):
            errors.append(f'{code}/{m["id"]}: 프롬프트 구성 다름 {[p["id"] for p in it["prompts"]]}')
        for p in it['prompts']:
            keys = set(VAR.findall(p['body'])); vk = {x['key'] for x in p['variables']}
            if keys != vk: errors.append(f'{code}/{m["id"]}/{p["id"]}: 빈칸 불일치 {keys ^ vk}')
        # 한국어가 남아 있으면 오류 (빈칸 키는 제외)
        chk = {k: v for k, v in it.items() if k not in ('id', 'frequency')}
        flat = VAR.sub('', re.sub(r'"key": "[^"]*"', '', json.dumps(chk, ensure_ascii=False)))
        hit = HANGUL.search(flat)
        if hit: errors.append(f'{code}/{m["id"]}: 한국어 남음 → {flat[max(0, hit.start()-40):hit.start()+20]}')
        if code == 'zh-Hant' and re.search(r'新加坡|新元|S\$|人力部|MOM', flat): errors.append(f'zh-Hant/{m["id"]}: 싱가포르 표현 남음')
        out.append(it)
    C['items'] = out
    if missing: print(f'  {code}: 번역 대기 {len(missing)}개 (한국어판에만 공개)')
    (ASSETS / f'content.{code}.json').write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding='utf-8')
    return C

def build_ui():
    import ui
    out = {}
    for key, vals in ui.UI.items():
        d = dict(zip(['ko', 'en', 'ja', 'zh-Hans'], vals))
        d['zh-Hant'] = ui.ZH_HANT.get(key) or to_tw(d['zh-Hans'])
        for l in d:   # 앱 이름 넣기 (중국어는 이름 뒤 띄어쓰기 없앰)
            v = d[l].replace('AI 좋소', ui.APP_NAMES[l]).replace('AI Joso', ui.APP_NAMES[l])
            if l.startswith('zh'): v = re.sub(r'(秘笈) (?=[\u4e00-\u9fff])', r'\1', v)
            d[l] = v
        out[key] = d
    chips = dict(ui.CHIPS); chips['zh-Hant'] = to_tw(chips['zh-Hans'])
    (ASSETS / 'ui.json').write_text(json.dumps({'langs': ui.LANGS, 'names': ui.LANG_NAMES, 'chips': chips, 'strings': out}, ensure_ascii=False, indent=1), encoding='utf-8')
    return out

if __name__ == '__main__':
    langs = sys.argv[1:] or ['en', 'ja', 'zh-Hans', 'zh-Hant']
    build_ui()
    for code in langs:
        C = build(code); print(code, len(C['items']), 'items')
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    print('ok')
