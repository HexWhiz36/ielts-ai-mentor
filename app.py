import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. PAGE SETUP & MEMORY ---
st.set_page_config(page_title="AI IELTS Mentor", layout="wide")

# This is the memory logic to update file records dynamically so the plan survives page clicks
if "daily_plan" not in st.session_state:
    st.session_state.daily_plan = None
if "last_date" not in st.session_state:
    st.session_state.last_date = None

# --- 2. SIDEBAR & SECURE API CONNECTION ---
st.sidebar.title("⚙️ Setup")
st.sidebar.write("To prevent crashes, paste your Gemini API key below:")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

if not api_key:
    st.title("Welcome to your IELTS AI Mentor 🎓")
    st.warning("👈 Please enter your Gemini API Key in the sidebar to activate the AI. You can get one for free at aistudio.google.com")
    st.stop() # Halts the app here so it doesn't crash trying to run AI without a key

# Connect to AI securely
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Failed to connect: {e}")
    st.stop()

# --- 3. NAVIGATION ---
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["📅 Auto-Generated Daily Plan", "✍️ AI Writing Grader", "🗣️ Speaking Simulator", "📺 Masterclass Playlists"])

# ==========================================
# PAGE 1: AUTO-GENERATED DAILY PLAN
# ==========================================
if menu == "📅 Auto-Generated Daily Plan":
    st.header("🎯 Your Daily Study Routine")
    today = str(datetime.date.today())
    
    # The AI checks if it has already built a plan for today. If not, it builds it automatically.
    if st.session_state.last_date != today:
        with st.spinner("🤖 AI is analyzing requirements and generating today's routine..."):
            try:
                prompt = """Act as an expert IELTS Mentor. Generate today's study plan for a student aiming for a Band 7.5 to 8. 
                Include:
                1. 'Today's Targets': 3 highly specific tasks (e.g., 'Do Cambridge Test 14 Reading Passage 1', 'Write a Task 2 essay on Technology').
                2. 'Daily Vocabulary': 5 advanced words with their meaning, a Band 8 example sentence, and synonyms.
                3. 'Examiner Secret': One advanced tip for scoring high.
                Format clearly using Markdown."""
                
                response = model.generate_content(prompt)
                
                # Save to memory so it doesn't regenerate until tomorrow
                st.session_state.daily_plan = response.text
                st.session_state.last_date = today
            except Exception as e:
                st.error(f"Error generating plan: {e}")
                st.stop()
                
    # Display the plan seamlessly
    st.markdown(st.session_state.daily_plan)
    st.success("✅ Your plan is locked in for today. Come back tomorrow for a new one!")

# ==========================================
# PAGE 2: WRITING GRADER (Upgraded)
# ==========================================
elif menu == "✍️ AI Writing Grader":
    st.header("✍️ AI Writing Grader (Task 1 & 2)")
    st.write("Paste your essay below. The AI will mark it exactly like a human examiner.")
    
    task_type = st.selectbox("Select Task", ["Task 1 (Academic/General)", "Task 2 (Essay)"])
    question = st.text_area("The Question Prompt:")
    essay = st.text_area("Your Essay:", height=250)
    
    if st.button("Grade My Essay"):
        if essay and question:
            with st.spinner("Evaluating against the 4 IELTS criteria..."):
                try:
                    prompt = f"""Act as a strict, official IELTS examiner. Grade this {task_type}.
                    Question: {question}
                    Essay: {essay}
                    
                    Format your response with Markdown headers:
                    1. **Overall Band Score** (bold and clear)
                    2. **Criteria Breakdown**: Give a score and 1 sentence reason for:
                       - Task Response/Achievement
                       - Coherence & Cohesion
                       - Lexical Resource
                       - Grammatical Range & Accuracy
                    3. **Major Weaknesses**: List the top 2 things dragging the score down.
                    4. **Band 8 Rewrite**: Rewrite one poorly phrased paragraph from the essay to show how a Band 8+ candidate would write it."""
                    
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error grading essay: {e}")
        else:
            st.warning("Please provide both the question and your essay.")

# ==========================================
# PAGE 3: SPEAKING SIMULATOR
# ==========================================
elif menu == "🗣️ Speaking Simulator":
    st.header("🗣️ Interactive Speaking Coach")
    st.write("Generate a random speaking test. Record yourself on your phone, then evaluate your fluency.")
    
    if st.button("Generate Random Mock Test"):
        with st.spinner("Creating test..."):
            try:
                prompt = """Act as an IELTS examiner. Generate a full speaking mock test:
                - Part 1: 3 questions on a common topic (e.g., hometown, work, hobbies).
                - Part 2: A cue card with bullet points. Include instructions to speak for 2 minutes.
                - Part 3: 3 analytical questions related to the Part 2 topic.
                Do not provide the answers, just the questions and instructions."""
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error generating test: {e}")

# ==========================================
# PAGE 4: CURATED MASTERCLASSES
# ==========================================
elif menu == "📺 Masterclass Playlists":
    st.header("📺 Structured YouTube Curriculum")
    st.markdown("""
    Stop wandering around YouTube. Follow this specific sequence for free:
    
    ### Phase 1: The Blueprint (Learn the Rules)
    *   **IELTS Liz:** Search her channel for "Task 1 Line Graph" and "Task 2 Essay Structures." Memorize her templates.
    *   **E2 IELTS (Jay):** Search for "IELTS Reading Super Methods."
    
    ### Phase 2: Advanced Execution (Band 7 to 8+)
    *   **IELTS Advantage:** Watch his "Task 2 Framework" and "Complex Sentences" videos. He teaches you how to write clearly, not confusingly.
    *   **English Speaking Success (Keith):** Watch his videos on "Idioms for IELTS" and "Part 2 Cue Cards." Focus on his intonation.
    
    ### Phase 3: Daily Grinding
    *   **Crack IELTS with Rob:** Search this channel and do one full Listening and Reading test every single day under timed conditions.
    """)
