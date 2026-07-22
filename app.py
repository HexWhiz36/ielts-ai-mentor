import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION ---
# Replace with your actual Gemini API key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# --- APP LAYOUT & SIDEBAR ---
st.set_page_config(page_title="My IELTS AI Mentor", layout="wide")
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Daily Routine & Vocab", "Writing Evaluator", "Speaking Practice", "Free Video Masterclasses"])

# --- SECTION 1: DAILY ROUTINE & VOCAB ---
if menu == "Daily Routine & Vocab":
    st.header(f"📅 Your Plan for {datetime.date.today()}")
    st.write("Let Gemini generate your personalized daily tasks and vocabulary.")
    
    if st.button("Generate Today's Plan"):
        with st.spinner("Consulting your AI Mentor..."):
            prompt = """Act as an expert IELTS tutor. Generate: 
            1. A 3-step daily study routine for today (1 hour total). 
            2. 5 advanced IELTS vocabulary words with their meanings, an example sentence, and synonyms. 
            Keep it structured and encouraging."""
            response = model.generate_content(prompt)
            st.markdown(response.text)

# --- SECTION 2: WRITING EVALUATOR ---
elif menu == "Writing Evaluator":
    st.header("✍️ AI Writing Grader (Task 1 & Task 2)")
    task_type = st.selectbox("Select Task Type", ["Task 1 (Report/Letter)", "Task 2 (Essay)"])
    question = st.text_area("Paste the Question Here:")
    essay = st.text_area("Paste your Answer Here:", height=250)
    
    if st.button("Evaluate My Writing"):
        if essay and question:
            with st.spinner("Analyzing your writing against IELTS rubrics..."):
                prompt = f"""Act as a strict IELTS examiner. Grade the following {task_type}.
                Question: {question}
                Essay: {essay}
                
                Provide a Band Score (1-9) for:
                1. Task Achievement / Task Response
                2. Coherence and Cohesion
                3. Lexical Resource (Vocabulary)
                4. Grammatical Range and Accuracy
                
                Give an overall band score. Then, provide 3 specific areas for improvement and rewrite one poorly phrased paragraph to make it band 8+."""
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.warning("Please enter both the question and your essay.")

# --- SECTION 3: SPEAKING PRACTICE ---
elif menu == "Speaking Practice":
    st.header("🗣️ Speaking Simulator")
    st.write("Get a random IELTS Speaking topic to practice.")
    
    if st.button("Give me a Mock Test"):
        with st.spinner("Generating questions..."):
            prompt = "Act as an IELTS examiner. Give me a full Mock test: 3 questions for Part 1 (familiar topics), a cue card for Part 2 with 1 minute prep instructions, and 3 analytical questions for Part 3 based on the cue card theme."
            response = model.generate_content(prompt)
            st.markdown(response.text)
    
    st.info("Tip: Record yourself on your phone while answering, then listen back to check your fluency and hesitation!")

# --- SECTION 4: FREE VIDEO MASTERCLASSES ---
elif menu == "Free Video Masterclasses":
    st.header("📺 Top YouTube Playlists for Band 8+")
    st.markdown("""
    You don't need a paid course. Watch these channels in this specific order:
    
    ### 1. Understanding the Basics (Foundation)
    *   **Channel:** [IELTS Liz](https://www.youtube.com/user/ieltsliz)
    *   **Focus:** Watch her foundational videos on Task 1 and Task 2 structures. She breaks down exactly what the examiners want.
    
    ### 2. Advanced Writing & Reading
    *   **Channel:** [IELTS Advantage](https://www.youtube.com/c/IELTSAdvantage)
    *   **Focus:** Watch his "Task 2 Framework" videos. He is the best for teaching you how to write complex sentences simply and accurately. 
    
    ### 3. Speaking Fluency
    *   **Channel:** [English Speaking Success (Keith)](https://www.youtube.com/c/EnglishSpeakingSuccess)
    *   **Focus:** Best channel for speaking. He teaches natural vocabulary, phrasal verbs, and how to sound conversational rather than robotic.
    
    ### 4. Listening Practice
    *   **Channel:** [Crack IELTS with Rob](https://www.youtube.com/) (or search "IELTS Listening Practice Tests")
    *   **Focus:** Do one full listening test every day. Note down your mistakes and figure out *why* you misheard the answer.
    """)
