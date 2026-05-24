<div align="center">

# CXO Copilot

**Ask any business question in plain English.**
**Get answers, charts, and slide decks — instantly.**

[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude%20API-7C3AED?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Day%201%20Demo-F59E0B?style=flat-square)]()
[![Owner](https://img.shields.io/badge/Owner-IntelliBridge-0EA5E9?style=flat-square)]()

<br/>

> A CEO shouldn't need a data analyst to answer a business question.  
> CXO Copilot federates your data, writes the answer, and builds the deck — in under 15 seconds.

</div>

---

## What Is This?

CXO Copilot is a chat interface for business leaders. Type a question. Get a written answer with real numbers, an inline chart, and an optional 10-slide deck — all pulled from your actual data sources simultaneously.

No SQL. No dashboards. No waiting for the BI team.

```
CEO types: "Did we hit our Q1 sales target? Where did we miss and by how much?"

  → CXO Copilot queries your Snowflake DB, Salesforce CRM, and marketing CSV at the same time
  → Synthesises a clear written answer with exact figures and % variance
  → Renders an inline bar chart
  → Optionally exports a clean executive deck via Gamma
  → All in under 15 seconds
```

---

## The Problem It Solves

In most companies, data is fragmented across teams and tools:

| Team | Where Their Data Lives | The Problem |
|------|------------------------|-------------|
| Finance | Snowflake database | Needs an analyst to extract it |
| Sales | Salesforce CRM | Locked inside a tool only sales can access |
| Marketing | Excel / CSV files | Emailed around, always out of date |

Getting a single cross-functional answer means someone manually pulls from all three, pastes into Excel, and writes a summary. That takes **1–2 days**.

CXO Copilot does it in **under 15 seconds**.

---

## Who It's For

| User | Description | What They Gain |
|------|-------------|----------------|
| **Primary** | CEOs, CFOs, VPs who make decisions but don't write SQL or use BI tools | Instant answers — no analyst needed |
| **Secondary** | Data / BI teams spending 60% of their time on ad-hoc executive requests | That queue disappears entirely |
| **Best-fit company** | Mid-sized org (500–2000 people) using Snowflake + Salesforce + spreadsheets | Replaces 3 tools with 1 conversation |

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| F1 | **Chat Interface** | One text box. Plain English. No menus, filters, or SQL required. |
| F2 | **Multi-Source Querying** | Reads YAML config files to know where data lives, then queries all relevant sources in parallel. |
| F3 | **Plain-English Answer** | Returns a written response with specific figures, % changes, and clear attribution — not a raw table. |
| F4 | **Inline Charts** | Automatically renders a bar or line chart alongside the answer when the data suits it. Same screen. |
| F5 | **Slide Deck Export** | One-click export as a clean 10-slide deck via Gamma API. Triggered by any summary question. |
| F6 | **Follow-up Questions** | Conversation state is preserved. Ask *"Now break that by region"* — no re-entering context needed. |

### Out of Scope (Day 1)

- User accounts or login
- Role-based access control
- Scheduled reports or alerts
- Mobile app
- Live Snowflake / Salesforce connections *(Day 1 uses realistic mock data)*

---

## How It Works

```
1  User types a question          →  Plain text chat input
2  App reads config files         →  Knows what data lives where (YAML per source)
3  AI decides which sources       →  Claude API — reasoning core
4  Queries all sources at once    →  Parallel calls to SQLite, JSON, CSV
5  AI combines all results        →  Cross-source synthesis + answer writing
6  App displays answer + chart    →  Prose + st.bar_chart inline
7  Optional: slide deck export    →  Gamma API — 10 slides max
8  User asks a follow-up          →  Conversation state preserved in session
```

---

## Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| App screen | Streamlit (Python) | Simple, no web design needed |
| AI brain | Claude API (Anthropic) | Reasoning + writing the answer |
| Data config | YAML (one per source) | Easy to edit, no database needed |
| Mock data | SQLite + JSON + CSV | Realistic, works fully offline |
| Charts | Streamlit built-in | Fast, zero extra setup |
| Slide export | Gamma API | Clean decks, 10 slides max |
| Conversation memory | Streamlit session state | Keeps chat history in-session |
| Run locally | `streamlit run app.py` | One command, no server needed |
| Deploy | Streamlit Cloud | Free tier, shareable URL |

---

## File Structure

```
CXO-Copilot/
│
├── app.py                    # Chat UI, charts, layout — what the user sees
├── orchestrator.py           # Claude API call + routing logic — the brain
├── tools.py                  # Functions that query each data source
│
├── registry/
│   ├── snowflake.yaml        # Config: orders database schema
│   ├── salesforce.yaml       # Config: pipeline / CRM data
│   └── marketing.yaml        # Config: campaigns CSV
│
├── data/
│   ├── glowkart.db           # Fake orders, actuals, and forecast data (SQLite)
│   ├── pipeline.json         # Fake CRM deals and pipeline stages
│   └── campaigns.csv         # Fake campaign spend and results
│
├── requirements.txt          # Python packages — one command installs all
└── secrets.toml.example      # API key template (not committed to git)
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/akv803101/CXO-Co-pilot.git
cd CXO-Co-pilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your Claude API key

# 4. Run
streamlit run app.py
```

---

## Demo Scenario — GlowKart

The Day 1 demo uses **GlowKart**, a fictional D2C brand. All mock data covers GlowKart's sales, marketing campaigns, and pipeline. The build is considered complete when all 5 questions below return correct, clear answers.

| # | Type | Question | Sources |
|---|------|----------|---------|
| Q1 | Revenue vs forecast | *"Did GlowKart hit its Q1 revenue target? Where did we miss and by how much?"* | Snowflake + CSV |
| Q2 | Campaign ROI | *"Which Diwali campaign drove the most revenue per rupee spent? Show me by channel."* | CSV + Snowflake |
| Q3 | Pipeline health | *"How healthy is our Q2 pipeline? What's at risk of slipping?"* | CRM (JSON) |
| Q4 | CEO morning brief ⭐ | *"Give me a CEO morning brief — revenue, pipeline, and top campaign performance."* | All 3 sources |
| Q5 | Drill-down follow-up | *"You said South region missed. What drove that — was it volume or pricing?"* | Snowflake |

> Q4 is the **slide deck trigger** — it tests full data federation and Gamma export.

---

## Definition of Done — Day 1

- [ ] App runs locally with `streamlit run app.py`
- [ ] All 5 demo questions return correct, clear answers
- [ ] At least 2 questions pull from more than one data source
- [ ] Charts appear inline alongside the answer
- [ ] Q4 (CEO brief) generates and opens a Gamma slide deck
- [ ] Q5 (follow-up) works without re-entering context
- [ ] A non-technical person can use it with zero instructions
- [ ] `requirements.txt` is clean — one command installs everything

---

## Roadmap

```
Phase 0 ── Day 1 Demo        Mock data, GlowKart scenario, full UI      ● Today
Phase 1 ── Real Connectors   Live Snowflake + Salesforce via MCP        ○ Weeks 2–4
Phase 2 ── Product           Login, access control, usage analytics     ○ Month 2–3
Phase 3 ── GTM               Consulting pilots → self-serve SaaS        ○ Month 4+
```

---

## Built By

**IntelliBridge** — *Don't just learn AI. Sell AI.*

---

<div align="center">
<sub>CXO Copilot · PRD v0.1 · Confidential</sub>
</div>
