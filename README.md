# 🧠 Hiring Intelligence System

> **Capstone Project 2 — Applied Agentic AI **  
> A production-grade, multi-agent AI platform that transforms raw engineering hiring data into structured, evidence-backed insights — in under 2 minutes, for ~$0.015 per run.

---

## 📌 Overview

The **Hiring Intelligence System** is a fully functional agentic AI pipeline built on **n8n Cloud**, **OpenAI GPT-4o**, **Pinecone RAG**, and **Streamlit**. It analyses 550 engineering candidates across 3 years and 5 hiring domains, surfacing actionable recommendations that engineering managers can act on immediately.

A single webhook call triggers the entire pipeline:

```
Streamlit UI  →  n8n Webhook  →  Google Sheets  →  Pinecone RAG  →  5 GPT-4o Agents  →  Evaluation  →  Dashboard
```

No API keys are required in the UI. All AI inference runs inside n8n.

---

## 🎯 The Problem It Solves

Engineering hiring is **data-rich but insight-poor**. Most teams make hiring decisions on gut feeling, not evidence. This system addresses five specific failure modes:

| Problem | What the System Does |
|---|---|
| **Sourcing Blind Spots** | Ranks channels by hire rate, recommends budget reallocation |
| **Rejection Pattern Invisibility** | Identifies stage/role failure patterns, surfaces root causes |
| **Panel Load Imbalance** | Flags overloaded interviewers, recommends equitable redistribution |
| **Offer Leakage** | Analyses decline reasons, compensation gaps, and competing offers |
| **Pipeline Bottlenecks** | Monitors time-in-stage vs SLA targets, flags at-risk candidates |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT DASHBOARD                       │
│              (localhost:8501 · no API keys needed)               │
└──────────────────────────┬──────────────────────────────────────┘
                           │  POST /webhook/hiring-rag-agent
┌──────────────────────────▼──────────────────────────────────────┐
│                         n8n CLOUD                                │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────┐ │
│  │Google Sheets│───▶│ RAG Retrieval│───▶│  5 Insight Agents   │ │
│  │ (5 sheets)  │    │  (Pinecone)  │    │  GPT-4o / 4o-mini   │ │
│  └─────────────┘    └──────────────┘    └──────────┬──────────┘ │
│                                                     │            │
│                      ┌──────────────────────────────▼──────────┐ │
│                      │  Evaluation Agent (GPT-4o · LLM-judge)  │ │
│                      │  Optimization Agent (cost tracking)      │ │
│                      └──────────────────────────────┬──────────┘ │
└─────────────────────────────────────────────────────┼────────────┘
                                                       │  JSON
┌─────────────────────────────────────────────────────▼────────────┐
│              Insight Cards · Eval Scores · Cost Breakdown         │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🤖 The 8 Agents

### Insight Agents
| Agent | Model | Domain |
|---|---|---|
| 🎯 Sourcing Quality | GPT-4o | Best channels per role |
| 🔍 Rejection Pattern | GPT-4o | Stage & role failure analysis |
| ⚖️ Panel Load Balancer | GPT-4o-mini | Interviewer rebalancing |
| 💼 Offer Insights | GPT-4o | Decline reasons & compensation gaps |
| 🚦 Pipeline Health | GPT-4o-mini | SLA monitoring & funnel speed |

### Supporting Agents
| Agent | Role |
|---|---|
| 🔀 Routing Agent | n8n workflow logic — directs queries to the right specialist |
| 🛡️ Evaluation Agent | LLM-as-judge — scores all 5 outputs for quality (0–10) |
| ⚡ Optimization Agent | Calculates per-agent token costs and savings opportunities |

---

## 📤 Shared Output Contract

Every agent returns the same 5-field JSON structure:

```json
{
  "recommendation":   "Primary insight for the engineering manager",
  "evidence":         ["Supporting data point 1", "Data point 2"],
  "confidence_score": 0.91,
  "cost_of_insight":  { "model": "gpt-4o", "tokens": 1450, "usd": "0.00420" },
  "alternative":      "Secondary recommendation if primary is blocked"
}
```

This contract enables consistent evaluation, routing, and dashboard rendering across all agents.

---

## 🗂️ Repository Structure

```
Capstone_Project_VijayMisra/
│
├── 📄  README.md                              # This file
│
├── 🔄  n8n Workflow
│   └── Hiring_Agent_RAG_v2_Webhook.json      # Main n8n workflow (import this into n8n)
│
├── 🖥️  Dashboard
│   ├── streamlit_app.py                       # Streamlit dashboard
│   └── requirements.txt                       # Python dependencies
│
├── 📚  RAG Knowledge Base
│   ├── sourcing_benchmarks.docx
│   ├── rejection_patterns_guide.docx
│   ├── panel_load_standards.docx
│   ├── offer_compensation_policy.docx
│   ├── pipeline_sla_targets.docx
│   ├── interview_calibration.docx
│   ├── hiring_reference_v1.pdf
│   ├── technical_screen_rubric.pdf
│   └── diversity_sourcing_guide.pdf
│
├── 🐍  RAG Scripts
│   ├── pinecone_ingest.py                     # Ingest documents into Pinecone
│   └── pinecone_retrieve.py                   # Test retrieval from Pinecone
│
├── 📊  Data
│   └── hiring_intelligence_dataset.xlsx       # 550 candidates · 3 years · 7 sheets
│
├── 📑  Presentation
│   └── Hiring_Intelligence_Capstone_v3.pptx  # 14-slide presentation (Ocean Command design)
│
└── 📝  Write-up
    └── Hiring_Intelligence_Writeup.docx       # Full project write-up (18 pages)
```

---

## 🚀 Quick Start

### Prerequisites
- [n8n Cloud account](https://app.n8n.cloud) (free tier works)
- OpenAI API key
- Pinecone account (free tier)
- Google Sheets with the hiring dataset (see `/Data`)
- Python 3.9+

### Step 1 — Set up Pinecone

```bash
# Install dependencies
pip install -r requirements.txt

# Ingest documents into Pinecone
python pinecone_ingest.py

# Verify retrieval works
python pinecone_retrieve.py
```

### Step 2 — Import and configure n8n workflow

1. Log in to your n8n Cloud instance
2. Click **Import from file** → select `Hiring_Agent_RAG_v2_Webhook.json`
3. Set the following **n8n Variables** (Settings → Variables):

| Variable | Value |
|---|---|
| `OPENAI_API_KEY` | `sk-proj-...` |
| `PINECONE_API_KEY` | Your Pinecone API key |
| `PINECONE_HOST_DOCS` | Host URL for `hiring` index |
| `PINECONE_HOST_EXCEL` | Host URL for `v1` index |

4. Connect **Google Sheets OAuth2** credentials in the workflow nodes
5. Click the **Inactive** toggle → workflow becomes **Published** (green dot)
6. Copy the **Production URL** from the Webhook Trigger node:
   ```
   https://YOUR-INSTANCE.app.n8n.cloud/webhook/hiring-rag-agent
   ```

### Step 3 — Launch the Streamlit dashboard

```bash
streamlit run streamlit_app.py
```

1. Open `http://localhost:8501`
2. Paste your n8n Production webhook URL in the sidebar
3. Click **Test Connection** → should show ✅ Connected
4. Click **▶ Run Full Pipeline**

The pipeline takes **60–120 seconds** and returns structured insights for all 5 domains.

---

## 📊 Dataset

The `hiring_intelligence_dataset.xlsx` file contains 7 structured sheets:

| Sheet | Contents |
|---|---|
| Candidates Master | Core candidate record — role, source, status, dates |
| Interview Stages | Per-stage timestamps, interviewers, outcomes |
| Rejection Reasons | Structured rejection codes per stage and role |
| Offer Details | Offer amounts, competing offers, accept/decline |
| Panel Assignments | Interviewer utilisation and feedback scores |
| Source Channels | Channel spend and hire counts per quarter |
| Pipeline Events | Stage transition log for SLA calculation |

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| Orchestration | [n8n Cloud](https://n8n.io) |
| Primary LLM | OpenAI GPT-4o |
| Efficiency LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-large (1024 dims) |
| Vector Store | [Pinecone](https://pinecone.io) — dual indexes |
| Data Source | Google Sheets (OAuth2, live read) |
| Dashboard | [Streamlit](https://streamlit.io) |
| RAG Scripts | Python 3.9+ |

---

## 💡 Key Design Decisions

**1. Cloud-native data only**  
n8n Cloud has no filesystem access. Google Sheets via native OAuth2 nodes is the only reliable data source pattern for n8n Cloud deployments.

**2. Shared output contract**  
Defining a single 5-field JSON contract before building any agent was the highest-leverage decision. It makes evaluation, routing, and dashboard rendering consistent across all agents.

**3. Dual Pinecone indexes**  
Separating policy documents (`hiring` index) from structured data (`v1` index) keeps RAG retrieval clean and allows independent reindexing of each data type.

**4. LLM-as-judge evaluation**  
GPT-4o evaluates GPT-4o outputs, scoring each insight for actionability, grounding, and hallucination risk. No golden dataset required for baseline quality control.

**5. Inline cost calculation**  
The Final Results Summary node calculates costs directly using a hardcoded `AGENT_MODELS` map, ensuring cost transparency is never dependent on a downstream node succeeding.

---

## 📈 Sample Output

```
✅ Evaluation Passed — Overall quality score: 70% · All insights approved

🎯 Sourcing Quality          [95% confidence]
   Increase LinkedIn investment; LinkedIn hire rate (0.57) is 2.5×
   higher than Indeed (0.23). Reduce Indeed spend by 30%.

🔍 Rejection Patterns        [87% confidence]
   Revise Software Engineer JD — Technical Interview stage shows
   48% rejection rate, highest across all roles.

🚦 Pipeline Health           [93% confidence]
   Implement 48-hr offer SLA. Current average: 9.4 days.
   79% of declined offers had a competing offer pending.

💰 Total pipeline cost: ~$0.015 USD  |  Runtime: ~90 seconds
```

---

## 📋 n8n Workflow Nodes

The workflow (`Hiring_Agent_RAG_v2_Webhook.json`) contains 41 nodes:

```
Webhook Trigger
    └── Read: Sourcing Quality ──┐
    └── Read: Candidates         │
    └── Read: Interviewer Load   ├──▶ Combine All Sheets ──▶ RAG Retrieval
    └── Read: Offer Outcomes     │         ┌──────────────────────┘
    └── Read: Pipeline Events ───┘         │
                                    ┌──────▼──────┐
                         ┌──────────┤ 5 Agents    ├──────────┐
                         │          │ (parallel)  │          │
                    Parse Outputs ◀─┴─────────────┘          │
                         │                                    │
                    Merge All Outputs                         │
                         │                                    │
                    Bundle Results ──────────────────────────┤
                         │                                    │
                    Evaluation Agent                   Optimization Agent
                         │                                    │
                    Parse Eval Output                         │
                         └──────────────┬─────────────────────┘
                                        │
                               Final Results Summary
                                        │
                               Webhook Response ──▶ Streamlit
```

---

## 🗺️ Roadmap

- [ ] Live ATS integration (Greenhouse / Lever API)
- [ ] Scheduled weekly runs with Slack/email delivery
- [ ] Streaming dashboard (SSE) for real-time agent output
- [ ] Candidate-level risk flagging
- [ ] Automated Pinecone re-ingestion on new data
- [ ] Role-based access control in Streamlit
- [ ] Historical cost tracking dashboard

---

## 👤 Author

**Vijay Misra**  
Capstone Project 2 · Applied Agentic AI

---

## 📄 License

This project was built as a capstone submission. All dataset values are synthetic. No real candidate data is included in this repository.

---

<p align="center">
  Built with n8n · OpenAI · Pinecone · Streamlit<br>
  <em>"Turning hiring data into engineering-grade decisions."</em>
</p>
