#!/usr/bin/env python3
"""Build the Gravit Path website into site/ in every language, from the shared Gravit layout, the texts in
tools/texts_<lang>.py and the rule packs. English lives at /, the other languages at /<lang>/. The rules page
is generated from rules/*/*.yaml, so the site always shows exactly the rules the assistant uses; rule
statements stay in English, the language of their official sources."""
import html
import importlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
sys.path.insert(0, str(Path(__file__).resolve().parent))
LANGS = ["en", "es", "pt", "zh", "uk", "ru"]
HTML_LANG = {"zh": "zh-Hans"}
SHORT = {"en": "EN", "es": "ES", "pt": "PT", "zh": "中文", "uk": "УКР", "ru": "РУС"}
TAGCLS = {"verified": "t-ok", "secondary": "t-warn", "needs_review": "t-warn"}
GH = "https://github.com/gravit-open-network-foundation/gravit-path"
E = html.escape

# Sends a first-time visitor to the language of their browser, if we have it. No cookies, no tracking:
# the choice made with the language links is remembered in this browser only.
AUTO = """<script>(function(){try{if(localStorage.getItem('gp-lang'))return}catch(e){}
var have=%s,ls=navigator.languages||[navigator.language||''];
for(var i=0;i<ls.length;i++){var c=(ls[i]||'').toLowerCase().slice(0,2);if(c==='en')return;
if(have.indexOf(c)>-1){location.replace('/'+c+location.pathname+location.hash);return}}})();</script>"""


def texts(lang):
    return importlib.import_module(f"texts_{lang}").T


def packs():
    return {f.parent.name: yaml.safe_load(f.read_text()) for f in sorted((ROOT / "rules").glob("*/*.yaml"))}


def prefix(lang):
    return "" if lang == "en" else f"{lang}/"


def page(lang, sub, title, desc, nav, body):
    depth = (0 if lang == "en" else 1) + (1 if sub else 0)
    root = "../" * depth
    head = (SITE / "_head.html").read_text().replace("{{TITLE}}", E(title)).replace("{{DESC}}", E(desc)).replace("{{ROOT}}", root)
    head = head.replace('<html lang="en">', f'<html lang="{HTML_LANG.get(lang, lang)}">')
    alt = "".join(f'<link rel="alternate" hreflang="{HTML_LANG.get(l, l)}" href="https://gravitpath.world/{prefix(l)}{sub}">' for l in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="https://gravitpath.world/{sub}">'
    head = head.replace("</head>", alt + (AUTO % json.dumps(LANGS[1:]) if lang == "en" else "") + "\n</head>", 1)
    foot = (SITE / "_foot.html").read_text().replace("{{ROOT}}", root or "./")
    home = root + prefix(lang)
    items = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in nav)
    langs = "".join(
        (f'<b>{SHORT[l]}</b>' if l == lang else
         f'<a href="{root}{prefix(l)}{sub}" onclick="try{{localStorage.setItem(\'gp-lang\',\'{l}\')}}catch(e){{}}">{SHORT[l]}</a>')
        for l in LANGS)
    items += f'<li class="langs">{langs}</li>'
    header = f'''<div class="page">
  <header>
    <a class="logo" href="{home or './'}" aria-label="Gravit Path">
    <img class="astra" src="{root}img/logo-gon-162.webp" srcset="{root}img/logo-gon-162.webp 1x, {root}img/logo-gon-324.webp 2x, {root}img/logo-gon-486.webp 3x" width="108" height="162" alt="" decoding="async" fetchpriority="high" />
    <span class="logo-word">Gravit Path</span>
    </a>
    <nav aria-label="Main"><ul>{items}</ul></nav>
  </header>
  <style>nav li.langs{{display:flex;gap:10px;margin-left:8px;padding-left:14px;border-left:1px solid rgba(100,180,255,.25)}}
  nav li.langs a{{opacity:.6;text-decoration:none}} nav li.langs a:hover{{opacity:1}} nav li.langs b{{color:#4fc3f7}}</style>
  <main><div class="gv">
'''
    return head + header + body + "\n  </div></main>\n\n" + foot


def index(p, T, lang):
    n = sum(len(v) for v in p.values())
    v = sum(1 for rs in p.values() for r in rs if r["status"] == "verified")
    f = lambda s: s.format(n=n, v=v)  # noqa: E731
    labels = "".join(f'<div class="state"><b>{E(a)}</b><span class="tag {c}">{E(b)}</span></div>'
                     for (a, b), c in zip(T["labels"], ["t-bad", "t-plan", "t-ok"]))
    steps = "".join(f'<div class="card"><span class="rule">{E(a)}</span><h3>{E(b)}</h3><p>{E(c)}</p></div>' for a, b, c in T["steps"])
    tag = {"rules": f' <span class="tag t-plan">{E(T["tag_rules"])}</span>', "planned": f' <span class="tag t-warn">{E(T["tag_planned"])}</span>', "": ""}
    paths = "".join(f'<div class="card"><span class="rule">{E(a)}</span><h3>{E(b)}</h3><p>{E(c)}{tag[s]}</p></div>' for a, b, c, s in T["paths"])
    countries = "".join(
        f'<div class="card"><span class="rule">{k.upper()}</span><h3>{E(T["country_names"][k])}</h3><p>'
        f'{E(T["country_card"].format(n=len(rs), v=sum(1 for r in rs if r["status"] == "verified")))} '
        f'<a href="rules/#{k}">{E(T["see_them"])}</a></p></div>' for k, rs in p.items())
    sample = [r for rs in p.values() for r in rs if r["status"] == "verified"][:3]
    rules = "".join(f'<div class="card"><span class="rule">{E(r["id"])}</span><p>{E(r["statement"])} '
                    f'<a href="{E(r["source"])}">{E(T["official_source"])}</a></p></div>' for r in sample)
    princ = "".join(f'<div class="card"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in T["principles"])
    links = ["https://gravitverifier.space", "https://github.com/gravit-open-network-foundation/capability-gate",
             "https://github.com/gravit-open-network-foundation/history-keeper"]
    trust = "".join(f'<div class="card"><h3>{E(a)}</h3><p>{E(b)} <a href="{u}">{E(c)}</a></p></div>' for (a, b, c), u in zip(T["trust"], links))
    ul = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)  # noqa: E731
    pp, pr = T["plan_people"], T["plan_pro"]
    mail = '<a href="mailto:web@gravit.world">web@gravit.world</a>'
    canon = f'<a href="{GH}/blob/main/CANON.md">CANON.md</a>'
    tcls = {"ok": "t-ok", "warn": "t-warn", "bad": "t-bad", "plan": "t-plan"}
    status = "".join(f'<tr><td>{E(a)}</td><td><span class="tag {tcls[c]}">{E(t)}</span> '
                     f'{E(f(d)).replace("{canon}", canon) if d != "{canon}" else canon}</td></tr>' for a, c, t, d in T["status"])
    return f'''
<div class="hero">
  <div>
    <p class="kicker">{E(T["kicker"])}</p>
    <h1>{E(T["h1"])}<em>{E(T["h1_em"])}</em></h1>
    <p class="lead">{E(T["lead"])}</p>
    <div class="btns"><a class="btn btn1" href="#paths">{E(T["btn_paths"])}</a><a class="btn btn2" href="rules/">{E(T["btn_rules"])}</a></div>
  </div>
  <div class="states">{labels}<p>{E(T["labels_note"])}</p></div>
</div>
<section id="how"><h2>{E(T["how_h"])}</h2><div class="grid">{steps}</div></section>
<section id="paths"><h2>{E(T["paths_h"])}</h2><p class="muted">{E(T["paths_lead"])}</p><div class="grid">{paths}</div></section>
<section id="countries"><h2>{E(T["countries_h"])}</h2><p class="muted">{E(T["countries_lead"])}</p><div class="grid">{countries}</div></section>
<section id="rules"><h2>{E(T["rules_h"])}</h2><p class="muted">{E(f(T["rules_lead"]))}</p><div class="grid">{rules}</div>
  <p style="margin-top:16px"><a class="btn btn2" href="rules/">{E(f(T["all_rules"]))}</a></p></section>
<section id="principles"><h2>{E(T["principles_h"])}</h2><div class="grid">{princ}</div></section>
<section id="trust"><h2>{E(T["trust_h"])}</h2><p class="muted">{E(T["trust_lead"])}</p><div class="grid">{trust}</div></section>
<section id="plans"><h2>{E(T["plans_h"])} <span class="tag t-plan" style="vertical-align:middle">{E(T["preview"])}</span></h2>
  <div class="plans" style="grid-template-columns:repeat(2,1fr)">
    <div class="plan"><h3>{E(pp[0])}</h3><div class="price">{E(pp[1])}</div><ul>{ul(pp[2])}</ul></div>
    <div class="plan" style="border-color:var(--glow)"><h3>{E(pr[0])}</h3><div class="price">{E(pr[1])}</div><ul>{ul(pr[2])}</ul></div>
  </div></section>
<section id="partners"><h2>{E(T["partners_h"])}</h2><p class="muted">{E(T["partners_text"]).replace("{mail}", mail)}</p></section>
<section id="status"><h2>{E(T["status_h"])}</h2>
  <div class="tablewrap"><table><tr><th>{E(T["status_item"])}</th><th>{E(T["status_today"])}</th></tr>{status}</table></div>
  <div class="notice">{E(T["notice"])}</div></section>
'''


def rules_page(p, T):
    blocks = []
    for k, rs in p.items():
        rows = "".join(
            f'<tr><td><code>{E(r["id"])}</code></td><td>{E(r["form"])}</td><td>{E(r["statement"])}'
            + (f'<br><span class="muted" style="font-size:14px">&ldquo;{E(r["quote"])}&rdquo;</span>' if r.get("quote") else "")
            + (f'<br><span class="muted" style="font-size:14px">{E(r["note"])}</span>' if r.get("note") else "")
            + f'</td><td><span class="tag {TAGCLS[r["status"]]}">{E(T["rp_status"][r["status"]])}</span><br>'
              f'<a href="{E(r["source"])}">{E(T["rp_source"])}</a></td></tr>'
            for r in rs)
        c = T["rp_cols"]
        blocks.append(f'<section id="{k}"><style>.gv td code{{white-space:nowrap}}</style><h2>{E(T["country_names"][k])}</h2>'
                      f'<div class="tablewrap"><table><tr><th>{E(c[0])}</th><th>{E(c[1])}</th><th>{E(c[2])}</th><th>{E(c[3])}</th></tr>'
                      f'{rows}</table></div></section>')
    manifest = json.loads((ROOT / "rules" / "MANIFEST.json").read_text())
    fp = "".join(f'<li><code>{E(f)}</code> sha256 <code>{m["sha256"][:16]}</code></li>' for f, m in manifest.items())
    gh = f'<a href="{GH}/tree/main/rules">GitHub</a>'
    note = f'<div class="notice">{E(T["rp_lang_note"])}</div>' if T["rp_lang_note"] else ""
    return f'''
<div class="hero" style="grid-template-columns:1fr">
  <div>
    <p class="kicker">{E(T["rp_kicker"])}</p>
    <h1>{E(T["rp_h1"])}<em>{E(T["rp_h1_em"])}</em></h1>
    <p class="lead">{E(T["rp_lead"])}</p>{note}
  </div>
</div>
{"".join(blocks)}
<section><h2>{E(T["rp_versions_h"])}</h2><p class="muted">{E(T["rp_versions"]).replace("{gh}", gh)}</p><ul>{fp}</ul></section>
'''


if __name__ == "__main__":
    p = packs()
    keys = set(texts("en"))
    for lang in LANGS:
        T = texts(lang)
        missing = keys - set(T)
        if missing:
            raise SystemExit(f"texts_{lang}.py lacks {sorted(missing)}")
        anchors = ["#how", "#paths", "#countries", "rules/", "#principles", "#plans", "#status"]
        nav = list(zip(T["nav"], anchors))
        out = SITE / prefix(lang)
        (out / "rules").mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page(lang, "", T["title"], T["desc"], nav, index(p, T, lang)))
        nav2 = [(t, ("../" + h) if h.startswith("#") else "./") for t, h in nav]
        (out / "rules" / "index.html").write_text(page(lang, "rules/", T["rp_title"], T["rp_desc"], nav2, rules_page(p, T)))
    print("built", ", ".join(LANGS))
