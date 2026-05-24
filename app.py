import streamlit as st
from master_agent import MasterAgent

st.set_page_config(page_title="CXO Copilot", page_icon="🧠", layout="wide")

st.markdown("""<style>
  .stApp{background:#Ffa500;color:#000000;}
  .badge{background:#FF6B35;color:#fff;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:800;}
  .agent-tag{background:#FFFAFA;color:#00D4AA;padding:2px 8px;border-radius:4px;font-size:10px;margin-right:4px;font-family:monospace;}
</style>""", unsafe_allow_html=True)

if "master" not in st.session_state:
    st.session_state.master   = MasterAgent()
    st.session_state.messages = []

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("## 🧠 CXO Copilot")
    st.markdown("*Ask any business question in plain English*")
with col2:
    st.markdown('<span class="badge">Intellibridge</span>', unsafe_allow_html=True)

st.divider()
st.markdown("**Quick questions:**")
demo_qs = [
    "Did GlowKart hit Q1 revenue target?",
    "Which Diwali campaign had the best ROI?",
    "How healthy is our Q2 pipeline?",
    "Give me a CEO morning brief",
]
cols = st.columns(4)
for i, q in enumerate(demo_qs):
    with cols[i]:
        if st.button(q, use_container_width=True):
            st.session_state.pending = q

st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("agents_used"):
            tags = " ".join([f'<span class="agent-tag">{a}</span>' for a in msg["agents_used"]])
            st.markdown(f"<small>Sources: {tags}</small>", unsafe_allow_html=True)

question = st.chat_input("Ask your business question...")
if "pending" in st.session_state:
    question = st.session_state.pop("pending")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"): st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Querying data sources..."): result = st.session_state.master.ask(question)
        st.markdown(result["answer"])
        if result["agents_used"]:
            tags = " ".join([f'<span class="agent-tag">{a}</span>' for a in result["agents_used"]])
            st.markdown(f"<small>Sources: {tags}</small>", unsafe_allow_html=True)
    st.session_state.messages.append({"role":"assistant","content":result["answer"],"agents_used":result["agents_used"]})
13