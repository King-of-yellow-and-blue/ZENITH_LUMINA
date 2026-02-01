import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION & UI ---
st.set_page_config(page_title="LUMINA AI", page_icon="🧠", layout="wide")

# Custom CSS for "Systematic UI/UX"
st.markdown("""
<style>
    .main-title {font-size: 3rem; color: #2E86C1; text-align: center; font-weight: 700;}
    .section-header {font-size: 1.5rem; color: #111; border-bottom: 2px solid #2E86C1; padding-bottom: 10px; margin-top: 20px;}
    .stButton>button {width: 100%; border-radius: 5px; height: 50px; font-weight: bold;}
    .info-box {background-color: #e8f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #2E86C1;}
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
        "1. Learning Path (Default)", 
        "2. Exam-Aware Generator", 
        "3. Thinking Debugger",
        "4. Flashcards & MindMaps"
    ])

# --- AI FUNCTION ---
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- MODE 1: LEARNING PATH (The Core) ---
if mode == "1. Learning Path (Default)":
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

# --- MODE 2: EXAM-AWARE ---
elif mode == "2. Exam-Aware Generator":
    st.markdown('<div class="main-title">Exam Answers</div>', unsafe_allow_html=True)
    st.caption("⚠️ Skips concepts. Focuses on Marks.")
    
    q_exam = st.text_input("Exam Question")
    marks = st.select_slider("Marks", options=["3 Marks", "5 Marks", "7 Marks"])
    
    if st.button("Generate Answer"):
        exam_prompt = f"""
        Write an exam answer for: '{q_exam}'.
        Marks: {marks}.
        
        RULES:
        - 3 Marks: Definition + Formula only.
        - 5 Marks: Explanation + Example.
        - 7 Marks: Detailed Theory + Derivation + Applications.
        
        Tone: Academic, exam-oriented.
        """
        st.success(ask_gemini(exam_prompt))

# --- MODE 3: THINKING DEBUGGER ---
# =========================================================
# MODE 3: THINKING DEBUGGER (Diagnostic Version)
# =========================================================
elif mode == "3. Thinking Debugger":
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
elif mode == "4. Flashcards & MindMaps":
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