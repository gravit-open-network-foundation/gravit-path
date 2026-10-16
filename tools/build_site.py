#!/usr/bin/env python3
"""Build the Gravit Path website into site/ from the shared Gravit layout and the rule packs.
The rules page is generated from rules/*/*.yaml, so the site always shows exactly the rules the agent uses."""
import html
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
COUNTRY = {"uk": "United Kingdom", "ch": "Switzerland"}
TAG = {"verified": ("t-ok", "VERIFIED"), "secondary": ("t-warn", "CONFIRM BEFORE USE"), "needs_review": ("t-warn", "NEEDS REVIEW")}
E = html.escape


def packs():
    out = {}
    for f in sorted((ROOT / "rules").glob("*/*.yaml")):
        out[f.parent.name] = yaml.safe_load(f.read_text())
    return out


def page(title, desc, root, nav, body):
    head = (SITE / "_head.html").read_text().replace("{{TITLE}}", E(title)).replace("{{DESC}}", E(desc)).replace("{{ROOT}}", root)
    foot = (SITE / "_foot.html").read_text().replace("{{ROOT}}", root or "./")
    items = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in nav)
    header = f'''<div class="page">
  <header>
    <a class="logo" href="{root or './'}" aria-label="Gravit Path, home">
    <img class="astra" src="{root}img/logo-gon-162.webp" srcset="{root}img/logo-gon-162.webp 1x, {root}img/logo-gon-324.webp 2x, {root}img/logo-gon-486.webp 3x" width="108" height="162" alt="" decoding="async" fetchpriority="high" />
    <span class="logo-word">Gravit Path</span>
    </a>
    <nav aria-label="Main"><ul>{items}</ul></nav>
  </header>
  <main><div class="gv">
'''
    return head + header + body + "\n  </div></main>\n\n" + foot


def index(p):
    n = sum(len(v) for v in p.values())
    v = sum(1 for rs in p.values() for r in rs if r["status"] == "verified")
    countries = "".join(
        f'<div class="card"><span class="rule">{k.upper()}</span><h3>{COUNTRY[k]}</h3><p>{len(rs)} rules, '
        f'{sum(1 for r in rs if r["status"] == "verified")} verified against official sources. '
        f'<a href="rules/#{k}">See them</a></p></div>' for k, rs in p.items())
    sample = [r for rs in p.values() for r in rs if r["status"] == "verified"][:3]
    rules = "".join(f'<div class="card"><span class="rule">{E(r["id"])}</span><p>{E(r["statement"])} '
                    f'<a href="{E(r["source"])}">Official source</a></p></div>' for r in sample)
    return f'''
<div class="hero">
  <div>
    <p class="kicker">Open source · every rule with its official source · preview v0.1</p>
    <h1>Your lawful route, <em>step by step.</em></h1>
    <p class="lead">Gravit Path is a verified route from who you are to what you are legally allowed to do, today.
      Tell us your situation in your own words. We show where you cannot go, the lawful paths you can take, and prepare
      the documents, with the official source next to every rule.</p>
    <div class="btns"><a class="btn btn1" href="#paths">See the paths</a><a class="btn btn2" href="rules/">Check our rules</a></div>
  </div>
  <div class="states">
    <div class="state"><b>Mandatory</b><span class="tag t-bad">must be done now</span></div>
    <div class="state"><b>Optional</b><span class="tag t-plan">your choice</span></div>
    <div class="state"><b>Not required now</b><span class="tag t-ok">relax, later</span></div>
    <p>Every step of every path carries one of these three labels, so you know what really matters today.</p>
  </div>
</div>

<section id="how">
  <h2>How it works</h2>
  <div class="grid">
    <div class="card"><span class="rule">1 · TALK</span><h3>Your situation, your words</h3><p>By voice or text: where you live, what you want to do, what you already have. No legal language needed.</p></div>
    <div class="card"><span class="rule">2 · LIMITS</span><h3>Where you cannot go now</h3><p>We say it first, with the reason and the source. It saves time, money and false hope.</p></div>
    <div class="card"><span class="rule">3 · PATHS</span><h3>Two to four lawful routes</h3><p>Country, legal form, cost, time and documents for each, every rule with its official source.</p></div>
    <div class="card"><span class="rule">4 · DOCUMENTS</span><h3>One questionnaire, all documents</h3><p>Articles, resolutions, registers and forms. Your draft is saved; continue any time, on any device.</p></div>
    <div class="card"><span class="rule">5 · YOU DECIDE</span><h3>Nothing happens without you</h3><p>Before anything is filed, the documents are checked and you approve. Where the law requires it, a licensed partner files.</p></div>
    <div class="card"><span class="rule">6 · RECORD</span><h3>A history nobody can rewrite</h3><p>Every step is recorded with independent timestamps: a clean trail for your bank and the authorities.</p></div>
  </div>
</section>

<section id="paths">
  <h2>Paths</h2>
  <p class="muted">A path is a route from your situation to a lawful action. These are the first ones.</p>
  <div class="grid">
    <div class="card"><span class="rule">BUSINESS START</span><h3>Start trading the right way</h3><p>When you can start before registering, when a company becomes necessary, and which form fits. <span class="tag t-plan">rules v0</span></p></div>
    <div class="card"><span class="rule">CLUB, EDUCATION, NON-PROFIT</span><h3>Bring people together</h3><p>Clubs, associations, charities: when registration is optional and when it is required. <span class="tag t-plan">rules v0</span></p></div>
    <div class="card"><span class="rule">BANKING</span><h3>Get to a bank account</h3><p>What banks usually ask for and how to prepare a clean file. <span class="tag t-warn">planned</span></p></div>
    <div class="card"><span class="rule">TAX AWARENESS</span><h3>Know when tax starts</h3><p>The events that create obligations, and what to track from day one. Not tax advice. <span class="tag t-warn">planned</span></p></div>
    <div class="card"><span class="rule">INTERNATIONAL</span><h3>Grow across borders</h3><p>Living in one country, clients in another: what to check and whom to ask. <span class="tag t-warn">planned</span></p></div>
    <div class="card"><span class="rule">FOR WHOM</span><h3>Especially for those systems serve badly</h3><p>Displaced people, complex residence histories, skilled people from countries with weak access to banking, and founders restructuring a business.</p></div>
  </div>
</section>

<section id="countries">
  <h2>Countries</h2>
  <p class="muted">A country goes live only when every statement about it is a rule with a dated official source.
    Next: Germany, Estonia, United States.</p>
  <div class="grid">{countries}</div>
</section>

<section id="rules">
  <h2>Rules you can check yourself</h2>
  <p class="muted">The agent answers only from published rules: {n} today, {v} verified against official sources.
    Each rule shows its source, a quote and the date it was read. When we are not sure, we say so.</p>
  <div class="grid">{rules}</div>
  <p style="margin-top:16px"><a class="btn btn2" href="rules/">All {n} rules with sources</a></p>
</section>

<section id="principles">
  <h2>Six principles</h2>
  <div class="grid">
    <div class="card"><h3>Limits first</h3><p>We say where you cannot go before we say where you can.</p></div>
    <div class="card"><h3>Three labels</h3><p>Mandatory, optional, not required now: on every step.</p></div>
    <div class="card"><h3>A source for every rule</h3><p>Official, dated, linked. Free for everyone, never behind a paywall.</p></div>
    <div class="card"><h3>Lawful paths only</h3><p>No ways around identity checks, anti money laundering rules, sanctions or tax. Where no lawful path exists, we say so.</p></div>
    <div class="card"><h3>Minimum data</h3><p>Only what your path needs, with your consent, deleted on request. Never sold or shared.</p></div>
    <div class="card"><h3>You decide</h3><p>We prepare; you approve. Advice on your specific case comes from licensed professionals.</p></div>
  </div>
</section>

<section id="trust">
  <h2>Why you can trust the result</h2>
  <p class="muted">Gravit Path runs on the open tools of the Gravit Open Network Foundation.</p>
  <div class="grid">
    <div class="card"><h3>Gravit Verifier</h3><p>Checks that evidence and documents are complete and signed before a step counts as done. <a href="https://gravitverifier.space">Learn more</a></p></div>
    <div class="card"><h3>Capability Gate</h3><p>The assistant may draft, but filing and paying need verified evidence and your approval. <a href="https://github.com/gravit-open-network-foundation/capability-gate">Specification</a></p></div>
    <div class="card"><h3>History Keeper</h3><p>Your path is recorded with timestamps from independent authorities. <a href="https://github.com/gravit-open-network-foundation/history-keeper">How it works</a></p></div>
  </div>
</section>

<section id="plans">
  <h2>Plans <span class="tag t-plan" style="vertical-align:middle">PREVIEW</span></h2>
  <div class="plans" style="grid-template-columns:repeat(2,1fr)">
    <div class="plan"><h3>For people</h3><div class="price">Free</div>
      <ul><li>The assistant, every path and every source</li><li>Your saved draft and documents, deleted on request</li><li>A complete document package to file yourself or through a partner</li></ul></div>
    <div class="plan" style="border-color:var(--glow)"><h3>For professionals</h3><div class="price">Corporate</div>
      <ul><li>For formation agents, notaries, lawyers and accountants</li><li>The path under your own brand, through an API</li><li>A signed case record for every client, independent backups, a trail banks accept</li><li>Shared, dated country rules for the whole team</li></ul></div>
  </div>
</section>

<section id="partners">
  <h2>Partners</h2>
  <p class="muted">We work with licensed professionals: formation agents, notaries, lawyers, accountants and banks. They
    file where the law requires a licensed party, and they give advice on individual cases. If you are one of them, write to
    <a href="mailto:web@gravit.world">web@gravit.world</a>.</p>
</section>

<section id="status">
  <h2>Honest status</h2>
  <div class="tablewrap"><table>
    <tr><th>Item</th><th>Today</th></tr>
    <tr><td>Rule packs with official sources</td><td><span class="tag t-ok">YES</span> {n} rules, {v} verified, United Kingdom and Switzerland</td></tr>
    <tr><td>Canonical principles</td><td><span class="tag t-ok">YES</span> <a href="https://github.com/gravit-open-network-foundation/gravit-path/blob/main/CANON.md">CANON.md</a></td></tr>
    <tr><td>Assistant (voice and text)</td><td><span class="tag t-warn">IN DEVELOPMENT</span> first prototype answers only from the rules</td></tr>
    <tr><td>Filing on your behalf</td><td><span class="tag t-bad">NO</span> only through licensed partners, once agreements exist</td></tr>
    <tr><td>Paid plans</td><td><span class="tag t-plan">PLANNED</span> nothing is sold yet</td></tr>
  </table></div>
  <div class="notice">Gravit Path gives general information and navigation, not legal, tax or financial advice. Laws change:
    check the linked source and confirm with the authority before you act.</div>
</section>
'''


def rules_page(p):
    blocks = []
    for k, rs in p.items():
        rows = "".join(
            f'<tr><td><code>{E(r["id"])}</code></td><td>{E(r["form"])}</td><td>{E(r["statement"])}'
            + (f'<br><span class="muted" style="font-size:14px">&ldquo;{E(r["quote"])}&rdquo;</span>' if r.get("quote") else "")
            + (f'<br><span class="muted" style="font-size:14px">{E(r["note"])}</span>' if r.get("note") else "")
            + f'</td><td><span class="tag {TAG[r["status"]][0]}">{TAG[r["status"]][1]}</span><br><a href="{E(r["source"])}">source</a></td></tr>'
            for r in rs)
        blocks.append(f'<section id="{k}"><style>.gv td code{{white-space:nowrap}}</style><h2>{COUNTRY[k]}</h2><div class="tablewrap"><table>'
                      f'<tr><th>Rule</th><th>Form</th><th>Statement</th><th>Status</th></tr>{rows}</table></div></section>')
    manifest = json.loads((ROOT / "rules" / "MANIFEST.json").read_text())
    fp = "".join(f'<li><code>{E(f)}</code> sha256 <code>{m["sha256"][:16]}</code></li>' for f, m in manifest.items())
    return f'''
<div class="hero" style="grid-template-columns:1fr">
  <div>
    <p class="kicker">Rule packs · read on 16 October 2026</p>
    <h1>Every rule, <em>with its source.</em></h1>
    <p class="lead">The Gravit Path assistant answers only from these rules. Verified rules quote an official source.
      Rules marked otherwise must be confirmed before anyone relies on them.</p>
  </div>
</div>
{"".join(blocks)}
<section><h2>Versions</h2><p class="muted">Each pack has a fingerprint, so an answer can name the exact version of the rules it used.
  The source files are on <a href="https://github.com/gravit-open-network-foundation/gravit-path/tree/main/rules">GitHub</a>.</p><ul>{fp}</ul></section>
'''


if __name__ == "__main__":
    p = packs()
    nav = [("How it works", "#how"), ("Paths", "#paths"), ("Countries", "#countries"), ("Rules", "rules/"),
           ("Principles", "#principles"), ("Plans", "#plans"), ("Status", "#status")]
    (SITE / "index.html").write_text(page("Gravit Path: your lawful route, step by step",
        "Gravit Path shows the lawful routes open to you, from your situation to a company, club or non-profit, with the official source next to every rule.",
        "", nav, index(p)))
    (SITE / "rules").mkdir(exist_ok=True)
    nav2 = [(t, ("../" + h) if h.startswith("#") else "./") for t, h in nav]
    (SITE / "rules" / "index.html").write_text(page("Gravit Path rules: every rule with its source",
        "The rule packs behind Gravit Path, each rule with its official source, quote and status.", "../", nav2, rules_page(p)))
    print("built site/index.html and site/rules/index.html")
