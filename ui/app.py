import streamlit as st
import sys
sys.path.append(".")

from retrieval.answer_generator import answer, concept_timeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lecture Memory | AI Learning Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Lecture Memory")
st.caption("Query across all your lectures. Find contradictions. Track how concepts evolved.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Search Settings")
    check_contradictions = st.toggle("Detect contradictions", value=True)
    use_session_filter = st.toggle("Filter by sessions range", value=False)

    session_from, session_to = None, None
    if use_session_filter:
        col1, col2 = st.columns(2)
        session_from = col1.number_input("From session", min_value=1, max_value=20, value=1)
        session_to = col2.number_input("To session", min_value=1, max_value=20, value=10)

    st.divider()
    st.header("📊 Concept Timeline")
    timeline_concept = st.text_input("Track concept:", placeholder="e.g. attention mechanism")
    show_timeline = st.button("Show Timeline")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🔍 Search & Ask", "📤 Add Lecture"])

with tab1:
    # ── Main query area ───────────────────────────────────────────────────────────
    query = st.text_input(
        "Ask a question about your lectures:",
        placeholder="How was backpropagation explained? Did it change over the course?",
    )
    search_btn = st.button("Search", type="primary")

    # ── Answer ────────────────────────────────────────────────────────────────────
    if search_btn and query:
        with st.spinner("Searching lectures..."):
            result = answer(
                query=query,
                session_from=session_from,
                session_to=session_to,
                check_for_contradictions=check_contradictions,
            )

        st.subheader("💬 Answer")
        st.write(result.answer)

        # Contradiction alert
        if result.contradiction_found:
            st.error(
                f"⚠️ **Contradiction detected across sessions**\n\n"
                f"{result.contradiction_explanation}"
            )
        elif check_contradictions:
            st.success("✅ No contradictions detected across sessions.")

        # Citations
        st.subheader("📍 Sources")
        for i, source in enumerate(result.sources, 1):
            with st.expander(
                f"Source {i} — Session {source.session_number} | {source.timestamp_label}",
                expanded=(i == 1),
            ):
                st.write(source.excerpt)

                # The demo-maker: timestamp deep link
                if source.video_url:
                    st.markdown(
                        f"[▶️ Jump to this moment in the lecture]({source.video_url})",
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption(f"Session: {source.session_id} | {source.timestamp_label}")

    # ── Concept Timeline ──────────────────────────────────────────────────────────
    if show_timeline and timeline_concept:
        with st.spinner(f"Building timeline for '{timeline_concept}'..."):
            timeline = concept_timeline(timeline_concept)

        if timeline:
            st.subheader(f"📈 How '{timeline_concept}' evolved across lectures")

            for entry in timeline:
                col1, col2 = st.columns([1, 4])
                col1.metric("Session", entry["session_number"])
                with col2:
                    st.write(entry["summary"])
                    if entry.get("timestamp_url"):
                        st.markdown(f"[▶️ {entry['timestamp_label']}]({entry['timestamp_url']})")
                st.divider()
        else:
            st.warning(f"No content found for '{timeline_concept}'.")

with tab2:
    st.header("📥 Ingest New Lecture")
    st.write("Enter a YouTube URL to transcribe and add it to your library.")
    
    with st.form("ingest_form"):
        yt_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        col1, col2 = st.columns(2)
        s_num = col1.number_input("Session Number", min_value=1, value=1)
        s_label = col2.text_input("Session Label", placeholder="e.g. Intro to Neural Networks")
        
        ingest_btn = st.form_submit_button("🚀 Start Ingestion")
        
    if ingest_btn:
        if not yt_url:
            st.error("Please provide a YouTube URL.")
        else:
            from ingest import ingest_youtube
            with st.status("Processing lecture...", expanded=True) as status:
                st.write("📥 Downloading and transcribing (this may take a few minutes)...")
                try:
                    ingest_youtube(yt_url, s_num, s_label, whisper_model="tiny", use_llm_topics=False)
                    status.update(label="✅ Ingestion Complete!", state="complete", expanded=False)
                    st.success(f"Lecture '{s_label}' (Session {s_num}) is now searchable!")
                except Exception as e:
                    status.update(label="❌ Ingestion Failed", state="error")
                    st.error(f"Error: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Built with Whisper · sentence-transformers · Qdrant · GPT-4o · Streamlit")
