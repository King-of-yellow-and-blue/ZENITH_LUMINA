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
# --- MODE 1: LEARNING PATH (The Final Optimized Master Rebuild) ---
if mode == "📚 Learning Path":
    st.markdown('<div class="main-title">LUMINA Learning Path</div>', unsafe_allow_html=True)
    
    # 1. Input Section
    col1, col2, col3 = st.columns(3)
    user_class = col1.text_input("Class", placeholder="e.g. 10th Grade")
    subject = col2.text_input("Subject", placeholder="e.g. Physics")
    chapter = col3.text_input("Chapter", placeholder="e.g. Optics")
    topic = st.text_input("Topic/Question", placeholder="Enter the specific concept...")
    
    # Cognitive Depth Control
    depth = st.select_slider("Cognitive Depth", options=["Default (Short)", "Guide (Exp + Quiz + Questions)", "Long (Detailed)"])

    if st.button("Generate Learning Path"):
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Analyzing Knowledge Graph & Scaling Math..."):
                # Define constraints based on depth
                word_limit = "120 words" if depth == "Default (Short)" else "450 words"
                include_extras = "YES" if depth == "Guide (Exp + Quiz + Questions)" else "NO"
                
                # MASTER PROMPT: Strictly forcing Math formatting and Easy Analogies
                master_prompt = f"""
                Act as an expert tutor for {user_class}. Topic: {topic} ({subject} - {chapter}).
                
                STRICT RULES:
                1. ANALOGY: Use a very simple, everyday relatable example (like a car, kitchen items, or sports).
                2. MATH FORMAT: You must provide a solved example. Use this structure exactly:
                   **The Problem:** [Scenario]
                   **The Formula:** [LaTeX Formula]
                   **Step-by-Step Solution:** [Numbered LaTeX steps]
                   **Final Result:** [LaTeX answer]
                
                STRICT TAGS FOR PARSING:
                [FOUNDATION]: List 2 prerequisites and a 3-step study order.
                [EXPLANATION]: Provide the easy analogy and simple concept explanation (under {word_limit}).
                [VISUAL]: Describe a diagram or mental image.
                [MATH]: Provide the mathematical breakdown in the strict format mentioned above.
                [MISCONCEPTIONS]: List 2 common mistakes and their corrections.
                [QUIZ]: (Only if {include_extras} == YES) 3 MCQs. Format: Q: [Quest] | A: [Opt] | B: [Opt] | C: [Opt] | D: [Opt] | Correct: [Ans]. Separate with '---'.
                [PRACTICE]: (Only if {include_extras} == YES) Provide 3 open-ended conceptual/numerical questions. Format: PQ: [Question] | Ans: [Answer]. Separate with '###'.
                """
                
                full_response = ask_gemini(master_prompt)

                # 2. PARSING & DISPLAY LOGIC
                try:
                    def get_section(content, start, end):
                        return content.split(start)[1].split(end)[0].strip()

                    foundations = get_section(full_response, "[FOUNDATION]", "[EXPLANATION]")
                    explanation = get_section(full_response, "[EXPLANATION]", "[VISUAL]")
                    visual_desc = get_section(full_response, "[VISUAL]", "[MATH]")
                    math_way = get_section(full_response, "[MATH]", "[MISCONCEPTIONS]")
                    
                    if "[QUIZ]" in full_response and include_extras == "YES":
                        misconceptions = get_section(full_response, "[MISCONCEPTIONS]", "[QUIZ]")
                        quiz_raw = get_section(full_response, "[QUIZ]", "[PRACTICE]")
                        practice_raw = full_response.split("[PRACTICE]")[1].strip()
                    else:
                        misconceptions = full_response.split("[MISCONCEPTIONS]")[1].strip()
                        quiz_raw, practice_raw = "", ""

                    # --- UI DISPLAY ---
                    st.markdown('### 🏛️ 1. Foundations')
                    st.info(foundations)

                    st.markdown('### 📖 2. The Concept')
                    st.markdown(explanation)

                    col_v, col_m = st.columns(2)
                    with col_v:
                        with st.container(border=True):
                            st.subheader("🖼️ The Visual Way")
                            
                            # INTEGRATED: Live Diagram Integration
                            img_topic = topic.replace(" ", "_")
                            diagram_url = f"https://pollinations.ai/p/educational_scientific_diagram_of_{img_topic}_{subject}_labeled_clear_background?width=800&height=600&seed=42"
                            
                            st.image(diagram_url, caption=f"Visualization: {topic}")
                            
                            # INTEGRATED: Zoom Feature
                            with st.expander("🔍 Click to Zoom / View Full Diagram"):
                                st.image(diagram_url, use_container_width=True)
                            
                            st.write(visual_desc)

                    with col_m:
                        with st.container(border=True):
                            st.subheader("🔢 The Mathematical Way")
                            st.markdown(math_way)
                    
                    with st.expander("🔍 3. Common Pitfalls & Corrections"):
                        st.warning(misconceptions)

                    # Assessment Section (Quiz + 3 Practice Questions)
                    if include_extras == "YES":
                        st.markdown('### ✍️ 4. Assessment Zone')
                        tab_mcq, tab_practice = st.tabs(["Multiple Choice Quiz", "3 Practice Questions"])
                        
                        with tab_mcq:
                            if quiz_raw:
                                for i, q_item in enumerate(quiz_raw.split('---')):
                                    if "|" in q_item:
                                        m = q_item.split("|")
                                        st.write(f"**Q{i+1}: {m[0].replace('Q:', '').strip()}**")
                                        c1, c2 = st.columns(2)
                                        c1.write(f"**A)** {m[1].replace('A:', '').strip()}")
                                        c2.write(f"**B)** {m[2].replace('B:', '').strip()}")
                                        c1.write(f"**C)** {m[3].replace('C:', '').strip()}")
                                        c2.write(f"**D)** {m[4].replace('D:', '').strip()}")
                                        with st.expander("Reveal Answer"):
                                            st.success(f"Correct: {m[5].replace('Correct:', '').strip()}")
                                        st.markdown("---")
                        
                        with tab_practice:
                            if practice_raw:
                                for i, p_item in enumerate(practice_raw.split('###')[:3]):
                                    if "|" in p_item:
                                        p_parts = p_item.split("|")
                                        st.write(f"**Question {i+1}:** {p_parts[0].replace('PQ:', '').strip()}")
                                        with st.expander("Check Solution"):
                                            st.success(p_parts[1].replace('Ans:', '').strip())

                except Exception as e:
                    st.error("Structure error. Displaying raw response:")
                    st.markdown(full_response)

# --- MODE 2: EXAM-AWARE (CBSE OPTIMIZED) ---
elif mode == "📝 Exam Generator":
    st.markdown('<div class="main-title">Exam Answer Engine</div>', unsafe_allow_html=True)
    
    q_exam = st.text_input("Enter Exam Question")
    # Updated Marks options to include 2 Marks
    marks = st.select_slider("Target Marks (CBSE Style)", options=["2 Marks", "3 Marks", "5 Marks", "7 Marks"])
    
    if st.button("Generate CBSE Answer"):
        if not q_exam:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Drafting textbook-accurate answer..."):
                # REFINED PROMPT WITH STRICT WORD LIMITS, KEYWORDS, AND FORMULAS
                exam_prompt = f"""
                Act as a strict CBSE Board Examiner. Write a high-scoring, school-level answer for: '{q_exam}'.
                Target Marks: {marks}.
                
                STRICT CONTENT RULES:
                1. TEXTBOOK ONLY: Use only standard school level textbook knowledge. NO external "extra" information.
                2. KEYWORDS: You MUST **bold** every critical technical keyword essential for scoring marks.
                3. FORMULAS: Include standard formulas using LaTeX where applicable.
                4. LANGUAGE: Use formal, proper school-level English suitable for board exams.
                
                STRICT STRUCTURE & WORD LIMITS:
                - If 2 Marks: 50–80 words. Provide one clear definition + one factual statement + two distinct points.
                - If 3 Marks: 100–150 words. Present three distinct points or logical steps. Do NOT use an unnecessary introduction.
                - If 5 Marks: 150–200 words. Start with a brief introduction followed by 4 to 5 key explanatory bullet points.
                - If 7 Marks: 200–300 words. Include a short introduction, a detailed structured explanation or derivation, and a diagram description or formula.
                
                OUTPUT FORMAT:
                1. The Answer (with bold keywords).
                2. A section at the end called [MARKING SCHEME] showing how the {marks} are awarded.
                3. A final section called [EXAM TIP] for a topper-style presentation.
                """
                
                full_response = ask_gemini(exam_prompt)
                
                # Parsing logic to separate marking scheme and tips for better UI
                main_ans = full_response.split("[MARKING SCHEME]")[0].strip()
                
                scheme_tip = ""
                if "[MARKING SCHEME]" in full_response:
                    scheme_tip = full_response.split("[MARKING SCHEME]")[1].strip()

                # Display Section
                st.success(f"Generated {marks} CBSE Response (Textbook Standard):")
                
                # Answer Box
                with st.container(border=True):
                    st.markdown(main_ans)
                
                # Extra Exam Insights
                if scheme_tip:
                    with st.expander("📊 Examiner Insights: Marking Scheme & Tips"):
                        st.info(scheme_tip.replace("[EXAM TIP]", "\n\n**💡 EXAM TIP:**"))
                
                # Download Button
                st.download_button(
                    label="📂 Download CBSE Answer Guide",
                    data=full_response,
                    file_name=f"CBSE_{marks.replace(' ', '_')}_Solution.txt",
                    mime="text/plain"
                )

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
# --- MODE 4: FLASHCARDS  ---
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
 
# --- MODE 5: CONCEPT TRANSFER INTELLIGENCE (CTI) - VIVA/INTERVIEW EDITION ---
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
                    
                    # LAYER 2: THE OPENING QUESTION (Updated for Student Level)
                    start_p = f"""
                    Topic: {topic_input}
                    DNA: {st.session_state.cti_dna}
                    Persona: Act as a Senior School Teacher or a Technical Interviewer for College Freshmen.
                    Tone: Formal, inquisitive, and firm.
                    
                    Task: Set up a practical, real-world scenario where {topic_input} applies.
                    DIFFICULTY RULE: Match the level of a Class 9 to College 1st Year student.
                    SCENARIO RULE: Use relatable examples (e.g., sports, household objects, simple gadgets). 
                    NO textbook examples. DO NOT explain the answer. 
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
                # LAYER 3 & 4 (Updated for Student Level)
                loop_p = f"""
                DNA: {st.session_state.cti_dna}
                History: {st.session_state.cti_history}
                Persona: Senior School/College Interviewer. 
                
                TASK 1 (Hidden Debug): Analyze the candidate's answer. Are they using jargon to hide a lack of understanding? Is their logic sound?
                TASK 2 (Follow-up): 
                - Difficulty must remain at Class 9 - College 1st Year level. 
                - Use simple, direct vocabulary.
                - If they are correct, challenge an assumption or move to a harder RELATABLE edge-case.
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
                if i < len(st.session_state.cti_evals): # Safety check
                    with st.expander(f"Question {i+1} - Candidate Response Analysis"):
                        st.write(f"**Your Argument:** {msg['content']}")
                        st.info(f"**Examiner's Internal Note:** {st.session_state.cti_evals[i]}")
            
            st.markdown("### 📊 Final Concept Competency Map")
            final_p = f"""
            Based on these evaluations: {st.session_state.cti_evals}, provide:
            1. Strong Concepts (Logic was robust)
            2. Fragile Logic (Where they struggled or guessed)
            3. Weak  (Verdict on deep understanding vs rote learning for their grade level)
            """
            st.success(ask_gemini(final_p))

        if st.button("Reset for New Interview"):
            st.session_state.clear()
            st.rerun()