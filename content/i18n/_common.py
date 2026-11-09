# -*- coding: utf-8 -*-
"""언어 파일에서 쓰는 짧은 도우미. 프롬프트 빈칸 키는 원본(한국어)과 같게 둔다."""
def v(key, label, ex): return {'key': key, 'label': label, 'example': ex}
def pr(pid, title, how, body, *vars_): return {'id': pid, 'title': title, 'howTo': how, 'body': body, 'variables': list(vars_)}
def st(t, b, c=''): return {'title': t, 'body': b, 'check': c}
def proj(name, instr, knowledge): return (name, instr, knowledge)
def doc(t, pub, url, verified='2026-11-09'): return {'title': t, 'publisher': pub, 'url': url, 'verifiedAt': verified}
