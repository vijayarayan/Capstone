"""
Hiring Intelligence System — Streamlit Dashboard
Capstone Project 2 · Applied Agentic AI for Engineering Managers
All AI runs inside n8n (GPT-4o · Pinecone RAG). No API keys needed here.
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hiring Intelligence System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Global background ── */
.stApp {
    background: #0A1628;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080F1E !important;
    border-right: 1px solid #1A3F6F;
}
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background: #0E2240 !important;
    border: 1px solid #1A3F6F !important;
    color: #FFFFFF !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: #00A896 !important;
    box-shadow: 0 0 0 2px rgba(0,168,150,0.2) !important;
}

/* ── Main content ── */
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px;
}

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, #0E2240 0%, #0A1628 60%, #051020 100%);
    border: 1px solid #1A3F6F;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 5px; height: 100%;
    background: linear-gradient(180deg, #00A896, #02C39A);
    border-radius: 16px 0 0 16px;
}
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.hero-title span { color: #00A896; }
.hero-subtitle {
    font-size: 0.9rem;
    color: #64748B;
    margin: 0 0 1rem 0;
}
.hero-badges {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.3px;
}
.badge-teal  { background: rgba(0,168,150,0.15); color: #02C39A; border: 1px solid rgba(0,168,150,0.3); }
.badge-gold  { background: rgba(245,166,35,0.15); color: #F5A623; border: 1px solid rgba(245,166,35,0.3); }
.badge-blue  { background: rgba(99,102,241,0.15); color: #818CF8; border: 1px solid rgba(99,102,241,0.3); }
.badge-green { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }

/* ── KPI Strip ── */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #0E2240;
    border: 1px solid #1A3F6F;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 12px 12px;
}
.kpi-card.teal::after  { background: #00A896; }
.kpi-card.gold::after  { background: #F5A623; }
.kpi-card.violet::after{ background: #8B5CF6; }
.kpi-card.green::after { background: #10B981; }

.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.teal  { color: #00A896; }
.kpi-value.gold  { color: #F5A623; }
.kpi-value.violet{ color: #A78BFA; }
.kpi-value.green { color: #34D399; }
.kpi-label {
    font-size: 0.75rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 500;
}

/* ── Section header ── */
.section-header {
    font-size: 0.7rem;
    font-weight: 600;
    color: #00A896;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #1A3F6F;
}

/* ── Agent card ── */
.agent-card {
    background: #0E2240;
    border: 1px solid #1A3F6F;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.agent-card:hover { border-color: #00A896; }
.agent-card-accent {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    border-radius: 12px 12px 0 0;
}
.agent-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.8rem;
}
.agent-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #FFFFFF;
}
.agent-emoji { margin-right: 6px; }
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.score-high   { background: rgba(16,185,129,0.2); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }
.score-mid    { background: rgba(245,166,35,0.2);  color: #F5A623; border: 1px solid rgba(245,166,35,0.3); }
.score-low    { background: rgba(239,68,68,0.2);   color: #F87171; border: 1px solid rgba(239,68,68,0.3); }

.rec-label {
    font-size: 0.65rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
}
.rec-text {
    font-size: 0.88rem;
    color: #CBD5E1;
    line-height: 1.6;
    margin-bottom: 0.8rem;
}
.evidence-chip {
    display: inline-block;
    background: rgba(0,168,150,0.08);
    border: 1px solid rgba(0,168,150,0.2);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 0.73rem;
    color: #94A3B8;
    margin: 2px 3px 2px 0;
}
.alt-text {
    font-size: 0.78rem;
    color: #64748B;
    font-style: italic;
    margin-top: 6px;
    padding-top: 8px;
    border-top: 1px solid #132B52;
}

/* ── Evaluation panel ── */
.eval-panel {
    background: #0E2240;
    border: 1px solid #1A3F6F;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    margin-bottom: 12px;
}
.eval-score-big {
    font-size: 3rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.flag-chip {
    display: inline-block;
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 0.73rem;
    color: #F87171;
    margin: 2px 3px 2px 0;
}

/* ── Cost panel ── */
.cost-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #132B52;
    font-size: 0.82rem;
}
.cost-row:last-child { border-bottom: none; }
.cost-agent { color: #94A3B8; }
.cost-val   { color: #F5A623; font-family: 'JetBrains Mono', monospace; font-weight: 500; }

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #00A896, #028090) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #02C39A, #00A896) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,168,150,0.4) !important;
}

/* ── Status boxes ── */
.status-box {
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.85rem;
    margin: 0.5rem 0;
}
.status-error   { background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.3);  color: #F87171; }
.status-success { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #34D399; }
.status-warn    { background: rgba(245,166,35,0.1); border: 1px solid rgba(245,166,35,0.3); color: #F5A623; }
.status-info    { background: rgba(0,168,150,0.1);  border: 1px solid rgba(0,168,150,0.3);  color: #02C39A; }

/* ── How it works ── */
.how-step {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 8px 0;
}
.how-num {
    min-width: 24px; height: 24px;
    background: #00A896;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700; color: white;
}
.how-text { font-size: 0.83rem; color: #94A3B8; line-height: 1.5; }
.how-text strong { color: #CBD5E1; }

/* ── Approved banner ── */
.approved-banner {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    color: #34D399;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.rejected-banner {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    color: #F87171;
    margin-bottom: 12px;
}

/* ── Tip box ── */
.tip-box {
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.78rem;
    color: #A78BFA;
    margin: 4px 0;
}

/* ── Monospace ── */
.mono { font-family: 'JetBrains Mono', monospace; }

/* ── Hide streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Divider ── */
hr { border-color: #1A3F6F !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper functions ──────────────────────────────────────────────────────────

def confidence_class(score):
    if score is None: return "score-mid", "–"
    pct = float(score) * 100
    cls = "score-high" if pct >= 80 else ("score-mid" if pct >= 60 else "score-low")
    return cls, f"{pct:.0f}%"

def agent_meta(name):
    """Return emoji, accent color, and display name per agent."""
    name_lower = (name or "").lower()
    if "sourc"   in name_lower: return "🎯", "#00A896", "Sourcing Quality"
    if "reject"  in name_lower: return "🔍", "#8B5CF6", "Rejection Patterns"
    if "panel"   in name_lower: return "⚖️",  "#F59E0B", "Panel Load Balancer"
    if "offer"   in name_lower: return "💼", "#10B981", "Offer Insights"
    if "pipeline"in name_lower: return "🚦", "#EF4444", "Pipeline Health"
    return "🤖", "#00A896", name or "Agent"

def call_webhook(url: str, timeout: int = 180):
    """POST empty body to n8n webhook, return (data, elapsed, error)."""
    t0 = time.time()
    try:
        resp = requests.post(
            url,
            json={},
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        elapsed = time.time() - t0
        if resp.status_code == 200:
            try:
                return resp.json(), elapsed, None
            except Exception:
                return None, elapsed, f"Response is not valid JSON:\n{resp.text[:400]}"
        else:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:300]
            return None, elapsed, f"HTTP {resp.status_code}: {json.dumps(detail) if isinstance(detail, dict) else detail}"
    except requests.exceptions.Timeout:
        return None, time.time() - t0, f"Request timed out after {timeout}s. The pipeline may still be running — check n8n Executions."
    except requests.exceptions.ConnectionError as e:
        return None, time.time() - t0, f"Connection error: {e}"
    except Exception as e:
        return None, time.time() - t0, f"Unexpected error: {e}"


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🧠 Hiring Intelligence")
    st.markdown("<p style='font-size:0.75rem;color:#64748B;margin-top:-8px'>n8n · OpenAI GPT-4o · Pinecone RAG</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**n8n Webhook URL**")
    webhook_url = st.text_input(
        label="webhook_url",
        label_visibility="collapsed",
        placeholder="https://YOUR-INSTANCE.app.n8n.cloud/webhook/hiring-rag-agent",
        key="webhook_url",
    )

    # Test connection button
    if st.button("🔗 Test Connection", use_container_width=True):
        if not webhook_url:
            st.markdown('<div class="status-box status-warn">⚠️ Paste your webhook URL first.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Testing…"):
                try:
                    r = requests.post(webhook_url, json={}, timeout=10)
                    if r.status_code in (200, 202):
                        st.markdown('<div class="status-box status-success">✅ Connected! Webhook is live.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="status-box status-error">❌ HTTP {r.status_code}<br><small>{r.text[:120]}</small></div>', unsafe_allow_html=True)
                except requests.exceptions.Timeout:
                    st.markdown('<div class="status-box status-success">✅ Webhook reachable (pipeline is running).</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="status-box status-error">❌ {str(e)[:150]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    timeout_val = st.slider("Timeout (seconds)", 60, 300, 180, 10)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem;color:#64748B;line-height:1.8'>
    <strong style='color:#94A3B8'>Stack</strong><br>
    🔀 n8n Cloud (orchestration)<br>
    🤖 GPT-4o / GPT-4o-mini<br>
    📚 Pinecone RAG (2 indexes)<br>
    📊 Google Sheets (live data)<br><br>
    <strong style='color:#94A3B8'>Workflow file</strong><br>
    <span class='mono' style='font-size:0.68rem;color:#00A896'>Hiring_Agent_RAG_v2_Webhook.json</span><br><br>
    <em style='color:#475569'>All AI runs inside n8n.<br>No API keys needed here.</em>
    </div>
    """, unsafe_allow_html=True)


# ── Hero header ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-header">
  <p class="hero-title">Hiring Intelligence <span>System</span></p>
  <p class="hero-subtitle">Capstone Project 2 · Applied Agentic AI for Engineering Managers</p>
  <div class="hero-badges">
    <span class="badge badge-teal">🤖 5 Insight Agents</span>
    <span class="badge badge-gold">⚡ RAG Grounded</span>
    <span class="badge badge-blue">🛡️ LLM-as-Judge</span>
    <span class="badge badge-green">📊 550 Candidates · 3 Years</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI strip (static baseline) ───────────────────────────────────────────────

st.markdown("""
<div class="kpi-strip">
  <div class="kpi-card teal">
    <div class="kpi-value teal">550</div>
    <div class="kpi-label">Total Candidates</div>
  </div>
  <div class="kpi-card gold">
    <div class="kpi-value gold">47%</div>
    <div class="kpi-label">Overall Offer Rate</div>
  </div>
  <div class="kpi-card violet">
    <div class="kpi-value violet">8</div>
    <div class="kpi-label">AI Agents Running</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-value green">3 yrs</div>
    <div class="kpi-label">Data Coverage</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── How it works ─────────────────────────────────────────────────────────────

with st.expander("ℹ️ How this works", expanded=False):
    st.markdown("""
    <p style='font-size:0.85rem;color:#94A3B8;margin-bottom:12px'>
    Click <strong style='color:#FFFFFF'>Run Full Pipeline</strong> →
    Streamlit POSTs to your n8n webhook → n8n does everything:
    </p>
    """, unsafe_allow_html=True)
    steps = [
        ("Reads live data from <strong>Google Sheets</strong>", "Candidates, Pipeline Events, Offers, Interviewer Load, Sourcing Quality"),
        ("Queries <strong>Pinecone</strong> for RAG context per agent", "<code>hiring</code> index → policy docs, benchmarks &nbsp;|&nbsp; <code>v1</code> index → historical Excel data"),
        ("Runs <strong>5 GPT-4o / GPT-4o-mini agents</strong>", "Each receives live data + RAG context → returns structured insight"),
        ("Runs <strong>GPT-4o Evaluation Agent</strong>", "LLM-as-judge scores all 5 outputs for quality and flags issues"),
        ("Returns <strong>complete JSON</strong>", "Displayed as insight cards below with confidence, evidence, and cost"),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="how-step">
          <div class="how-num">{i}</div>
          <div class="how-text"><strong>{title}</strong><br>{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:0.8rem;color:#475569;margin-top:12px'>
    <strong style='color:#94A3B8'>No API keys are needed in this app.</strong>
    Everything runs inside n8n.<br>
    Webhook path: <code style='color:#00A896'>POST /webhook/hiring-rag-agent</code>
    &nbsp;·&nbsp; Expected runtime: <strong>~60–120 seconds</strong>
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Run button ────────────────────────────────────────────────────────────────

col_btn, col_hint = st.columns([1, 2])
with col_btn:
    run_clicked = st.button("▶ Run Full Pipeline", use_container_width=True)
with col_hint:
    st.markdown("""
    <p style='font-size:0.8rem;color:#475569;padding-top:10px'>
    Reads Google Sheets → queries Pinecone → runs 5 GPT-4o agents + eval · ~60–120 sec
    </p>
    """, unsafe_allow_html=True)

# ── Guard: no URL ─────────────────────────────────────────────────────────────
if run_clicked and not webhook_url:
    st.markdown("""
    <div class="status-box status-warn">
    ⚠️ &nbsp;Paste your n8n Production webhook URL in the sidebar to continue.<br>
    <small style='color:#64748B'>Format: https://YOUR-INSTANCE.app.n8n.cloud/webhook/hiring-rag-agent</small>
    </div>
    """, unsafe_allow_html=True)
    run_clicked = False

# ── Execute pipeline ──────────────────────────────────────────────────────────
if run_clicked and webhook_url:
    progress_bar = st.progress(0)
    status_ph    = st.empty()

    stages = [
        (10, "📊 Reading Google Sheets (5 sheets)…"),
        (25, "📚 Querying Pinecone RAG indexes…"),
        (40, "🎯 Running Sourcing Quality Agent…"),
        (52, "🔍 Running Rejection Pattern Agent…"),
        (64, "⚖️  Running Panel Load Agent…"),
        (74, "💼 Running Offer Insights Agent…"),
        (84, "🚦 Running Pipeline Health Agent…"),
        (92, "🛡️  Running Evaluation Agent…"),
        (97, "⚡ Optimizing outputs…"),
    ]

    status_ph.markdown('<div class="status-box status-info">🔄 &nbsp;Pipeline started — this takes 60–120 seconds…</div>', unsafe_allow_html=True)

    # Start the actual call in the background sense — we animate progress while waiting
    import threading
    result_holder = {}

    def fetch():
        data, elapsed, err = call_webhook(webhook_url, timeout=timeout_val)
        result_holder["data"]    = data
        result_holder["elapsed"] = elapsed
        result_holder["error"]   = err

    thread = threading.Thread(target=fetch)
    thread.start()

    stage_idx = 0
    while thread.is_alive():
        pct = stages[stage_idx][0] if stage_idx < len(stages) else 97
        msg = stages[stage_idx][1] if stage_idx < len(stages) else "⏳ Finalising results…"
        progress_bar.progress(pct)
        status_ph.markdown(f'<div class="status-box status-info">{msg}</div>', unsafe_allow_html=True)
        time.sleep(8)
        if stage_idx < len(stages) - 1:
            stage_idx += 1

    thread.join()
    progress_bar.progress(100)

    data    = result_holder.get("data")
    elapsed = result_holder.get("elapsed", 0)
    error   = result_holder.get("error")

    # ── Error ──
    if error:
        status_ph.markdown(f"""
        <div class="status-box status-error">
        ❌ <strong>Error ({elapsed:.1f}s):</strong> {error}
        </div>
        """, unsafe_allow_html=True)
        with st.expander("🔧 Troubleshooting", expanded=True):
            st.markdown("""
            <div style='font-size:0.85rem;color:#94A3B8;line-height:2'>
            <strong style='color:#FFFFFF'>Common fixes:</strong><br>
            1. Make sure workflow is <strong>Published / Active</strong> in n8n (green dot, top-right)<br>
            2. Use the <strong>Production URL</strong> (not the Test URL with <code>/webhook-test/</code>)<br>
            3. Check the workflow has no <strong>red error nodes</strong> before running<br>
            4. Verify <strong>Google Sheets credentials</strong> are connected in n8n<br>
            5. Check <strong>OpenAI API key</strong> is valid in n8n variables<br>
            6. Try increasing the <strong>Timeout</strong> slider in the sidebar
            </div>
            """, unsafe_allow_html=True)
        st.stop()

    # ── Success ──
    status_ph.markdown(f'<div class="status-box status-success">✅ &nbsp;Pipeline completed in <strong>{elapsed:.1f}s</strong> · {data.get("agents_run", 0)} agents ran</div>', unsafe_allow_html=True)

    st.session_state["last_result"] = data
    st.session_state["last_elapsed"] = elapsed

# ── Display results (from session state) ─────────────────────────────────────

data = st.session_state.get("last_result")

if data:
    elapsed   = st.session_state.get("last_elapsed", 0)
    insights  = data.get("insights", [])
    evaluation= data.get("evaluation", {})
    cost_sum  = data.get("cost_summary", {})
    run_id    = data.get("run_id", "–")
    completed = data.get("completed_at", "")

    # Run metadata strip
    ts = ""
    if completed:
        try:
            ts = datetime.fromisoformat(completed.replace("Z", "+00:00")).strftime("%b %d %Y, %H:%M UTC")
        except Exception:
            ts = completed[:16]

    st.markdown(f"""
    <div style='display:flex;gap:16px;margin-bottom:1.2rem;font-size:0.75rem;color:#475569;align-items:center'>
      <span>🆔 <span class='mono' style='color:#64748B'>{run_id[:20] if run_id else '–'}</span></span>
      <span>🕐 {ts}</span>
      <span>⏱️ {elapsed:.1f}s</span>
      <span>🤖 {len(insights)} agents</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Evaluation banner ──
    approved = evaluation.get("approved")
    # n8n eval agent returns 0-10 scale; normalize to 0-1 for display
    raw_quality = evaluation.get("overall_quality", 0) or 0
    quality = float(raw_quality) / 10.0 if float(raw_quality) > 1 else float(raw_quality)
    if approved is True:
        st.markdown(f'<div class="approved-banner">✅ &nbsp;<strong>Evaluation Passed</strong> — Overall quality score: <strong>{quality:.0%}</strong> · All insights approved for engineering managers</div>', unsafe_allow_html=True)
    elif approved is False:
        flags = evaluation.get("flags", [])
        st.markdown(f'<div class="rejected-banner">⚠️ <strong>Evaluation flagged issues</strong> — Quality: {quality:.0%} &nbsp;|&nbsp; Flags: {", ".join(flags) if flags else "see details below"}</div>', unsafe_allow_html=True)

    # ── Main layout: insights left, eval+cost right ──
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.markdown('<div class="section-header">Agent Insights</div>', unsafe_allow_html=True)

        if not insights:
            st.markdown('<div class="status-box status-warn">No insights returned. Check n8n execution logs.</div>', unsafe_allow_html=True)

        for agent in insights:
            emoji, color, display_name = agent_meta(agent.get("agent",""))
            conf_score = agent.get("confidence_score")
            score_cls, score_txt = confidence_class(conf_score)
            evidence   = agent.get("evidence", [])
            if isinstance(evidence, str):
                evidence = [evidence]
            rec  = agent.get("recommendation", "No recommendation returned.")
            alt  = agent.get("alternative", "")

            st.markdown(f"""
            <div class="agent-card">
              <div class="agent-card-accent" style="background:{color}"></div>
              <div class="agent-header">
                <span class="agent-name"><span class="agent-emoji">{emoji}</span>{display_name}</span>
                <span class="score-badge {score_cls}">⬤ {score_txt} confidence</span>
              </div>
              <div class="rec-label">Recommendation</div>
              <div class="rec-text">{rec}</div>
              {'<div class="rec-label">Evidence</div>' if evidence else ''}
              {''.join(f'<span class="evidence-chip">📌 {e}</span>' for e in evidence[:4]) if evidence else ''}
              {'<div class="alt-text">💡 Alternative: ' + alt + '</div>' if alt else ''}
            </div>
            """, unsafe_allow_html=True)

    with right_col:
        # ── Evaluation detail ──
        st.markdown('<div class="section-header">Evaluation</div>', unsafe_allow_html=True)
        per_agent = evaluation.get("per_agent", {})
        flags     = evaluation.get("flags", [])
        notes     = evaluation.get("notes", "")

        # Build eval panel HTML safely without nested f-strings
        quality_color = "#34D399" if quality >= 0.8 else ("#F5A623" if quality >= 0.6 else "#F87171")
        quality_pct   = f"{quality:.0%}"

        if per_agent:
            per_agent_rows = ""
            for k, v in per_agent.items():
                # normalize 0-10 to 0-1
                v_norm  = float(v) / 10.0 if float(v) > 1 else float(v)
                v_color = "#34D399" if v_norm >= 0.8 else ("#F5A623" if v_norm >= 0.6 else "#F87171")
                v_pct   = f"{v_norm:.0%}"
                k_label = k.replace("_", " ").title()
                per_agent_rows += (
                    f"<div style='display:flex;justify-content:space-between;font-size:0.75rem;"
                    f"padding:3px 0;border-bottom:1px solid #132B52'>"
                    f"<span style='color:#64748B'>{k_label}</span>"
                    f"<span class='mono' style='color:{v_color}'>{v_pct}</span>"
                    f"</div>"
                )
        else:
            per_agent_rows = "<span style='font-size:0.78rem;color:#475569'>No per-agent scores returned.</span>"

        if flags:
            flag_chips = "".join(f"<span class='flag-chip'>⚑ {fl}</span>" for fl in flags)
            flags_html = (
                "<div style='margin-top:8px'>"
                "<div style='font-size:0.7rem;color:#64748B;text-transform:uppercase;"
                "letter-spacing:1px;margin-bottom:4px'>Flags</div>"
                + flag_chips + "</div>"
            )
        else:
            flags_html = ""

        notes_html = (
            f"<div style='font-size:0.78rem;color:#64748B;margin-top:10px;font-style:italic'>{notes}</div>"
            if notes else ""
        )

        st.markdown(
            f"""
            <div class="eval-panel">
              <div style='display:flex;align-items:center;gap:16px;margin-bottom:12px'>
                <div>
                  <div class="eval-score-big" style='color:{quality_color}'>{quality_pct}</div>
                  <div style='font-size:0.72rem;color:#64748B;text-transform:uppercase;letter-spacing:1px'>Overall Quality</div>
                </div>
                <div style='flex:1'>
                  <div style='font-size:0.78rem;color:#94A3B8;margin-bottom:6px'>Per-Agent Scores</div>
                  {per_agent_rows}
                </div>
              </div>
              {flags_html}
              {notes_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Cost summary ──
        st.markdown('<div class="section-header">Cost Transparency</div>', unsafe_allow_html=True)
        total_usd  = cost_sum.get("total_usd", 0) or 0
        haiku_usd  = cost_sum.get("haiku_equiv_usd", 0) or 0
        savings    = cost_sum.get("potential_savings", 0) or 0
        per_agent_costs = cost_sum.get("per_agent", []) or []
        tips       = cost_sum.get("tips", []) or []

        # Safe-cast cost values (n8n returns them as strings)
        try:
            total_usd_f = float(total_usd) if total_usd else 0.0
        except (ValueError, TypeError):
            total_usd_f = 0.0
        try:
            savings_f = float(savings) if savings else 0.0
        except (ValueError, TypeError):
            savings_f = 0.0

        st.markdown(f"""
        <div class="eval-panel">
          <div style='display:flex;gap:16px;margin-bottom:14px'>
            <div>
              <div style='font-size:1.6rem;font-weight:700;color:#F5A623;font-family:JetBrains Mono,monospace'>${total_usd_f:.4f}</div>
              <div style='font-size:0.7rem;color:#64748B;text-transform:uppercase;letter-spacing:1px'>Total Cost</div>
            </div>
            <div>
              <div style='font-size:1.6rem;font-weight:700;color:#34D399;font-family:JetBrains Mono,monospace'>${savings_f:.4f}</div>
              <div style='font-size:0.7rem;color:#64748B;text-transform:uppercase;letter-spacing:1px'>Potential Savings</div>
            </div>
          </div>
        """, unsafe_allow_html=True)

        if per_agent_costs:
            for row in per_agent_costs[:6]:
                name = row.get("agent", row.get("name", "–"))
                cost_raw = row.get("cost_usd", row.get("actual_usd", 0)) or 0
                try:
                    cost = float(cost_raw)
                except (ValueError, TypeError):
                    cost = 0.0
                st.markdown(f"""
                <div class="cost-row">
                  <span class="cost-agent">{name}</span>
                  <span class="cost-val">${cost:.4f}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if tips:
            st.markdown('<div class="section-header">Optimization Tips</div>', unsafe_allow_html=True)
            for tip in tips[:3]:
                st.markdown(f'<div class="tip-box">💡 {tip}</div>', unsafe_allow_html=True)

    # ── Raw JSON expander ──
    st.markdown("---")
    with st.expander("🗂 Raw JSON Response", expanded=False):
        st.code(json.dumps(data, indent=2), language="json")

else:
    # ── Empty state ──
    st.markdown("""
    <div style='text-align:center;padding:3rem 1rem'>
      <div style='font-size:3rem;margin-bottom:1rem'>🧠</div>
      <div style='font-size:1.1rem;font-weight:600;color:#CBD5E1;margin-bottom:0.5rem'>Ready to analyse your hiring pipeline</div>
      <div style='font-size:0.85rem;color:#475569'>
        Paste your n8n webhook URL in the sidebar, then click <strong style='color:#00A896'>Run Full Pipeline</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)
