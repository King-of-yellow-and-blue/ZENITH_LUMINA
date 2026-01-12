import streamlit as st
import google.generativeai as genai


# --- 1. CONFIGURATION & UI/UX REPAIR ---
st.set_page_config(page_title="LUMINA AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Fix for overlapping titles */
    .main-title {
        font-size: 3.2rem; 
        color: #2E86C1; 
        text-align: center; 
        font-weight: 800;
        padding-top: 30px; /* Increased top padding */
        padding-bottom: 50px; /* Added significant gap to inputs */
        margin-bottom: 20px;
    }
    
    /* Ensure Sidebar text is visible and spaced out */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Add space between sidebar radio options */
    div[getAttribute="data-testid"] > label {
        padding: 12px 0px; 
        font-weight: 500;
    }

    /* Fixed Button Styling */
    .stButton>button {
        width: 100%; 
        border-radius: 10px; 
        height: 50px; 
        font-weight: bold; 
        background-color: #2E86C1; 
        color: white;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background-color: #21618C;
        color: #FFD700 !important;
        transform: scale(1.02);
    }

    /* Inputs spacing */
    .stTextInput, .stSelectbox, .stTextArea {
        margin-bottom: 25px;
    }
    
    /* CBSE Topper's Tip Box */
    .topper-box {
        background-color: #fcf3cf;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #f1c40f;
        color: #7d6608;
        font-size: 0.9rem;
        margin-top: 15px;
    }

    .section-header {
        font-size: 1.6rem; 
        color: #2E86C1; 
        border-bottom: 2px solid #2E86C1; 
        padding-bottom: 10px; 
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.title("LUMINA 🧠")
    st.caption("Learning, Understanding & Mastery")
    
    # Secure API Key Input
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    if not api_key:
        st.warning("⚠️ Paste API Key to Start")
        st.stop()
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    st.markdown("---")
    mode = st.radio("Select Mode", [
        "📚 Learning Path", 
        "📝 Exam Generator", 
        "🔍 Thinking Debugger",
        "🗂️ Flashcards",
        "🧠 Concept Transfer Intelligence (CTI)"
    ])

# --- AI FUNCTION ---
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- MODE 1: LEARNING PATH (The Core) ---
if mode == "📚 Learning Path":
    st.markdown('<div class="main-title">LUMINA Learning Path</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    user_class = col1.text_input("Class", placeholder="e.g. 10th Grade")
    subject = col2.text_input("Subject", placeholder="e.g. Physics")
    chapter = col3.text_input("Chapter", placeholder="e.g. Optics")
    
    topic = st.text_input("Topic/Question", placeholder="Enter the specific concept...")
    
    # Cognitive Depth Control
    depth = st.select_slider("Cognitive Depth", options=["Default (Short)", "Long (Detailed)", "Guide (Exp + MCQs)"])

    if st.button("Generate Learning Path"):
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Analyzing Knowledge Graph..."):
                
                # 1. Prerequisite Check
                st.markdown('<div class="section-header">1. Foundations & Study Order</div>', unsafe_allow_html=True)
                prereq_prompt = f"""
                Act as an expert tutor.
                Student: {user_class}, {subject}, {chapter}. Topic: {topic}.
                1. List prerequisites needed to understand this.
                2. Provide a numbered study order for this topic.
                """
                st.info(ask_gemini(prereq_prompt))

                # 2. Adaptive Explanation (The "Three Ways")
                st.markdown('<div class="section-header">2. Adaptive Explanation</div>', unsafe_allow_html=True)
                
                # Check if Math is needed
                is_math = "math" in subject.lower() or "physic" in subject.lower() or "calculation" in topic.lower()
                
                expl_prompt = f"""
                Explain '{topic}' for {user_class}. Depth: {depth}.
                Format:
                1. **Analogy:** Real-world comparison (Text based).
                2. **Visual Description:** Describe a diagram that explains this.
                """
                if is_math:
                    expl_prompt += "\n3. **Mathematical Way:** Formula + Derivation + Solved Example."
                
                if depth == "Guide (Exp + MCQs)":
                    expl_prompt += "\n\nFinally, add 3 Multiple Choice Questions to test understanding."

                st.markdown(ask_gemini(expl_prompt))

                # 3. Misconception Detection
                st.markdown('<div class="section-header">3. Misconception Detection</div>', unsafe_allow_html=True)
                mis_prompt = f"What are common student doubts/misconceptions about '{topic}'? Provide corrections."
                st.warning(ask_gemini(mis_prompt))

# --- MODE 2: EXAM-AWARE (CBSE OPTIMIZED) ---
elif mode == "📝 Exam Generator":
    st.markdown('<div class="main-title">Exam Answer Engine</div>', unsafe_allow_html=True)
    
    q_exam = st.text_input("Enter Exam Question")
    marks = st.select_slider("Target Marks (CBSE Style)", options=["3 Marks", "5 Marks", "7 Marks"])
    
    if st.button("Generate CBSE Answer"):
        if not q_exam:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Drafting answer according to CBSE marking schemes..."):
                # REFINED PROMPT FOR CBSE STANDARDS & WORD LIMITS
                exam_prompt = f"""
                Act as a CBSE Board Examiner. Write a high-scoring answer for: '{q_exam}'.
                Target Marks: {marks}.
                
                STRICT STRUCTURE & WORD LIMITS:
                - If 3 Marks (Short Answer): Word limit 30-50 words. Provide a precise definition and 2 key points or a formula.
                - If 5 Marks (Long Answer I): Word limit 80-100 words. Use a 'Definition -> Key Points (Bullet points) -> Example' structure. 
                - If 7 Marks (Long Answer II): Word limit 150-200 words. Start with an introduction, follow with a detailed explanation/derivation (use LaTeX for math), and end with applications/conclusion.
                
                CBSE PRESENTATION RULES:
                1. Use bullet points for readability.
                2. Bold the most important keywords.
                3. If it is a science/eco question, include a 'Diagram Description' section.
                4. Do NOT combine mark categories. Only provide the {marks} version.
                """
                
                ans = ask_gemini(exam_prompt)
                st.success(f"CBSE Style {marks} Response:")
                st.markdown(ans)
                st.download_button("📂 Download CBSE Guide", ans, file_name=f"CBSE_{marks}_Ans.txt")


# =========================================================
# MODE 3: THINKING DEBUGGER (Diagnostic Version)
# =========================================================
elif mode == "🔍 Thinking Debugger":
    st.markdown('<div class="main-title">🧠 Thinking Debugger</div>', unsafe_allow_html=True)
    st.info("Input your understanding of a topic. LUMINA will analyze it for errors.")

    user_thought = st.text_area("Example: 'I think heavy objects fall faster than light objects because gravity pulls them harder.'")
    
    if st.button("Analyze & Debug"):
        if not user_thought:
            st.warning("Please enter your statement first!")
        else:
            with st.spinner("Analyzing logical consistency..."):
                debug_prompt = f"""
                User's Statement: "{user_thought}"
                
                Task: Perform a deep logical analysis.
                
                Format the output exactly like this:
                1. **STATUS:** [Declare 'TRUE' or 'FALSE' or 'PARTIALLY CORRECT']
                2. **THE FLAW:** Identify the specific part of the user's sentence that is scientifically or logically wrong.
                3. **THE REASON:** Explain why that specific part is wrong (the 'Logic Gap').
                4. **THE CORRECT CONCEPT:** Provide the scientifically accurate explanation.
                5. **VERDICT:** A 1-sentence wrap-up of what the user needs to change in their mental model.
                
                Tone: Professional, direct, and clinical.
                """
                
                response = ask_gemini(debug_prompt)
                
                # UI Display
                if "FALSE" in response.upper() or "PARTIALLY" in response.upper():
                    st.error("Diagnostic Result:")
                else:
                    st.success("Diagnostic Result:")
                    
                st.markdown(response)
# --- MODE 4: FLASHCARDS & MINDMAPS ---
elif mode == "🗂️ Flashcards":
    st.markdown('<div class="main-title">Revision Tools</div>', unsafe_allow_html=True)
    rev_topic = st.text_input("Enter Topic")
    
    col1, col2 = st.columns(2)
    if col1.button("Generate Flashcards"):
        if not rev_topic:
            st.warning("Enter a topic first!")
        else:
            with st.spinner("Creating Interactive Flashcards..."):
                # We force the AI to use a split character '|' between Q and A
                fc_prompt = f"""Create 5 flashcards for {rev_topic}. 
                Follow this format EXACTLY for each card:
                Q: [Question] | A: [Answer]
                Separate each card with '---'. 
                Do not include any introductory or concluding text."""
                
                raw_response = ask_gemini(fc_prompt)
                cards = raw_response.split('---')
                
                st.markdown("### 🗂️ Tap to Reveal Answers")
                
                for i, card in enumerate(cards):
                    if "|" in card:
                        # Split the single card into Question and Answer
                        parts = card.split("|")
                        question = parts[0].replace("Q:", "").strip()
                        answer = parts[1].replace("A:", "").strip()
                        
                        # Use an expander to hide the answer
                        with st.expander(f"🎴 Card {i+1}: {question}"):
                            st.success(f"**Answer:** {answer}")
 # --- MODE 5: CONCEPT TRANSFER INTELLIGENCE (CTI) ---
# --- MODE: CONCEPT TRANSFER INTELLIGENCE (CTI) - VIVA/INTERVIEW EDITION ---
elif mode == "🧠 Concept Transfer Intelligence (CTI)":
    st.markdown('<div class="main-title">Concept Transfer Intelligence</div>', unsafe_allow_html=True)
    
    # Initialize Session State
    if "cti_active" not in st.session_state:
        st.session_state.cti_active = False
        st.session_state.cti_finished = False
        st.session_state.cti_turn = 0
        st.session_state.cti_history = [] 
        st.session_state.cti_dna = ""      
        st.session_state.cti_evals = []    

    # 1. START SCREEN (The Waiting Room)
    if not st.session_state.cti_active:
        st.info("🎓 **The Examination Room:** You are entering a viva/interview. The examiner will test your logic, not your memory. Answer clearly and defend your reasoning.")
        
        topic_input = st.text_input("Candidate, what topic are we discussing today?", placeholder="e.g., Thermodynamics, Market Equilibrium, Data Structures...")
        
        if st.button("Enter Viva Room"):
            if topic_input:
                st.session_state.cti_active = True
                with st.spinner("Examiner is reviewing the concept..."):
                    # LAYER 1: INTERNAL DNA (Hidden)
                    dna_p = f"Analyze '{topic_input}'. Core Principle, Hidden Assumptions, Comfort Zone. Focus on technical accuracy."
                    st.session_state.cti_dna = ask_gemini(dna_p)
                    
                    # LAYER 2: THE OPENING QUESTION
                    start_p = f"""
                    Topic: {topic_input}
                    DNA: {st.session_state.cti_dna}
                    Persona: Act as a Senior Professor or a Technical Job Interviewer.
                    Tone: Formal, inquisitive, and firm.
                    Task: Set up a practical, real-world scenario where {topic_input} applies. 
                    Ask the candidate to explain how the core principle works in this specific case.
                    RULE: No textbook examples. Do NOT explain the answer. 
                    Stop after the question.
                    """
                    first_q = ask_gemini(start_p)
                    st.session_state.cti_history.append({"role": "assistant", "content": first_q})
                    st.session_state.cti_turn = 1
                    st.rerun()

    # 2. THE INTERROGATION (The Viva Loop)
    elif not st.session_state.cti_finished:
        st.progress(min(st.session_state.cti_turn / 12, 1.0), text=f"Interview Progress: Level {st.session_state.cti_turn}")

        for msg in st.session_state.cti_history:
            role_icon = "👨‍🏫" if msg["role"] == "assistant" else "🎓"
            with st.chat_message(msg["role"], avatar=role_icon):
                st.write(msg["content"])

        user_reply = st.chat_input("State your reasoning, candidate...")
        
        if user_reply:
            st.session_state.cti_history.append({"role": "user", "content": user_reply})
            
            with st.spinner("Examiner is evaluating your logic..."):
                loop_p = f"""
                DNA: {st.session_state.cti_dna}
                History: {st.session_state.cti_history}
                Persona: Senior Interviewer. 
                
                TASK 1 (Hidden Debug): Analyze the candidate's answer. Are they using jargon to hide a lack of understanding? Is their logic sound?
                TASK 2 (Follow-up): 
                - If they are correct, challenge an assumption or move to a harder edge-case.
                - If they are wrong, ask a 'cross-question' that forces them to see their own mistake.
                - If turn >= 10 or they've proven mastery, respond with [TERMINATE].
                
                FORMAT:
                EVAL: [Hidden Thinking Debugger Analysis]
                NEXT: [Interviewer's next question or [TERMINATE]]
                """
                res = ask_gemini(loop_p)
                
                if "NEXT:" in res:
                    parts = res.split("NEXT:")
                    st.session_state.cti_evals.append(parts[0].replace("EVAL:", "").strip())
                    next_step = parts[1].strip()
                else:
                    next_step = res

                if "[TERMINATE]" in next_step:
                    st.session_state.cti_finished = True
                    st.rerun()
                else:
                    st.session_state.cti_turn += 1
                    st.session_state.cti_history.append({"role": "assistant", "content": next_step})
                    st.rerun()

    # 3. FINAL EVALUATION (The Feedback Session)
    else:
        st.subheader("🏛️ Interview Concluded")
        st.write("The examiner has finished the questioning. Review your performance below.")
        
        if st.button("📂 Review Examiner's Feedback"):
            st.markdown("### 🔍 Internal Logic Evaluation")
            user_msgs = [m for m in st.session_state.cti_history if m["role"] == "user"]
            for i, msg in enumerate(user_msgs):
                with st.expander(f"Question {i+1} - Candidate Response Analysis"):
                    st.write(f"**Your Argument:** {msg['content']}")
                    st.info(f"**Examiner's Internal Note:** {st.session_state.cti_evals[i]}")
            
            st.markdown("### 📊 Final Concept Competency Map")
            final_p = f"""
            Based on these evaluations: {st.session_state.cti_evals}, provide:
            1. Strong Concepts (Logic was robust)
            2. Fragile Logic (Where they struggled or guessed)
            3. Interview Readiness (Verdict on deep understanding vs rote learning)
            """
            st.success(ask_gemini(final_p))

        if st.button("Reset for New Interview"):
            st.session_state.clear()
            st.rerun()