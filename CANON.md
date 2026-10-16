# Gravit Path: canonical document, v0.1

Gravit Open Network Foundation · 16 October 2026 · draft v0.1

> **Gravit Path is a verified route from who you are to what you are legally allowed to do, today.**

## 1. What it is
An AI navigator that listens to a person (voice or text) and shows the lawful paths open to them:
- to start a business, a club or a non-profit;
- where and in which legal form;
- what is mandatory, what is optional and what is not needed yet.

It then prepares the documents for the chosen path. It does not replace the state, a notary or a lawyer.
It returns to the person the ability to act among them.

**For whom:** people whom standard systems serve badly but who are among the most productive:
- refugees and displaced people;
- people with a complex residence or banking history;
- skilled professionals from countries with weak access to banking;
- experienced founders who want to restructure an existing business correctly.

**Patterns we build on**, known from inside:
- UK formation services (1st Formations; founders from Companies House): the funnel and the standard processes;
- IT-offshores.com: work with non-standard clients;
- the Swiss online counter EasyGov.swiss: an identity-first state process.

## 2. The six principles
1. **Constraint first.** First say where the person can NOT go now, then where they can. This removes most false hopes.
2. **Mandatory / Optional / Not required now.** Every step carries one of these three labels.
3. **Every legal statement has a dated official source.** The agent answers only from the rule packs in this repository.
   - Each rule names its source, the date it was read and its status: *verified*, *secondary* (confirm before use) or *needs review*.
   - Anything else is marked "ask a professional".
4. **Lawful paths only.** Gravit Path never suggests ways around identity checks, anti-money-laundering rules, sanctions or tax. It shows the lawful options a person has, and where none exists, it says so plainly.
5. **Minimum data, with consent.** Preparing documents needs names and addresses. We collect only what the chosen path needs, with consent, and delete on request. We never sell or share data.
6. **The person decides; the agent prepares.** Filing, paying or acting on someone's behalf happens only after the person approves. Legal advice comes from licensed partners, not from the agent.

## 3. How a path works
1. **Entry state.** Where the person lives, which documents they have, their aim and their limits. Each fact is a claim with its source.
2. **Constraint map.** Where they cannot go now, and why, with sources.
3. **Solution space.** Two to four lawful paths, each with jurisdiction, legal form, cost, time, risks and required documents.
4. **Path assembly.** The chosen path as steps, each labelled mandatory, optional or not required now.
5. **Action package.** The documents, checklists, the questions to ask a bank or a notary, and the points of responsibility.

## 4. Where Gravit makes it trustworthy
- **Rule packs** (`rules/`) carry the source and date of every rule.
  - `tools/check_rules.py` refuses a *verified* rule without an official source.
  - It writes a manifest with the SHA-256 of each pack, so that every answer can name the exact version of the rules it used.
- **Gravit Verifier** checks before a step counts as done:
  - the person's evidence is complete and signed;
  - the documents meet the rules of the chosen path.
- **Capability Gate**: the agent may draft, but filing and paying are frontier actions. They need a Verified Fact and the person's approval.
- **History Keeper** keeps the record of the path with independent timestamps. Banks and authorities value this trail in their checks.

## 5. Legal guardrails
- **United Kingdom.** A business that forms companies for others must register with HMRC as a trust or company service provider before trading (rule UK-AML-001). Gravit Path either registers itself or works through a supervised partner (an Authorised Corporate Service Provider). Until then it prepares documents only for the person to file themselves.
- **Switzerland.** A GmbH or AG needs a notary (CH-GMBH-002). Gravit Path prepares the mandate for the notary; it does not replace one.
- **Legal advice.** Gravit Path explains rules and options and prepares documents. Advice on a specific legal or tax position comes from a licensed lawyer or tax adviser, whom the agent helps to choose and brief.

## 6. What Gravit Path will not do
- **Rank countries by weak checks.** It never answers "where is KYC weakest" with a list; it shows the lawful paths and what banks usually ask for.
- **Promise "no personal data".** Preparing documents needs some data. Principle 5 applies instead.
- **State a figure without a source.** Every fee, threshold or deadline is a rule with an official source and a date.
- **Sell concealment.** No nominee arrangements to hide the real owner.

## 7. Path modules, first set
| Path | Jurisdictions in v0 | Status |
|---|---|---|
| Education, club, non-profit | UK (unincorporated association, charity, CIO), CH (Verein) | rules v0 |
| Business start | UK (Ltd), CH (GmbH, sole proprietorship via EasyGov) | rules v0 |
| Banking | | after the rule packs |
| Tax awareness (not advice) | | later |

## 8. Free and Guided Depth
- **Always free:** asking, every path, the three labels, and the official source of every legal statement. A free answer must be checkable, so sources are never behind a paywall.
- **Guided Depth (later, about 10 CHF):** depth, not rights.
  - comparisons between countries;
  - what changed recently;
  - detailed decision trees.
- **Rules for the offer:** the agent mentions it at most once and only when a case spans several countries or thresholds; it never blocks an answer.

## 9. Adding a country
Every country module covers the same seven blocks, and every statement in them is a rule with a dated official source:
1. right of association;
2. when obligations start;
3. business forms;
4. tax awareness;
5. banking reality;
6. local red flags;
7. sources.

A country is ready when all seven blocks have verified rules and the QA cases for it pass.

## 10. Disclaimers (shown with every answer)
- This is general information and navigation, not legal, tax or financial advice, and it does not replace licensed professionals.
- Sources are given so that you can check them; laws change, so confirm with the authority before acting.
- Gravit Path does not act, file or pay on your behalf without your explicit approval, and guarantees no outcome.
- We keep only what your chosen path needs, with your consent, and delete it on request.

## 11. Next steps
1. A prototype agent that answers only from the rule packs, with links and the label "verified" or "ask a professional".
2. Five to ten real cases from Dr. Konviser's experience, added to `qa/cases.yaml` next to the 23 behaviour tests.
3. Review of the *secondary* and *needs review* rules against the official texts.
