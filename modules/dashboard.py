import streamlit as st
from utils.api_client import ask_claude
from utils.helpers import show_header, show_info_card

SYSTEM_PROMPT = """You are MicroMind AI — an expert microbiology educator and quiz master.

Your task is to create educational quiz questions and provide learning guidance.

When asked to generate quiz questions:
1. Create clear, accurate multiple choice questions
2. Provide 4 options — one correct and three plausible distractors
3. After the answer is revealed — explain why the correct answer is right
4. Explain why each wrong answer is incorrect
5. Provide a learning tip related to the topic

When asked for a study plan:
1. Assess the weak areas provided
2. Create a structured, practical study plan
3. Suggest specific topics to focus on
4. Recommend a logical study sequence

Format quiz questions exactly like this:
QUESTION: [question text]
A) [option]
B) [option]
C) [option]
D) [option]
CORRECT: [letter]
EXPLANATION: [detailed explanation]

Be educational, encouraging, and practical."""

QUIZ_TOPICS = [
    "Gram staining and bacterial morphology",
    "Biochemical identification tests",
    "Culture media — types and uses",
    "Antimicrobial resistance mechanisms",
    "PCR and molecular techniques",
    "Clinical microbiology — UTI pathogens",
    "Clinical microbiology — respiratory pathogens",
    "Clinical microbiology — bloodstream infections",
    "Mycology — fungal infections",
    "Virology — common viral infections",
    "Parasitology — common parasites",
    "Infection control and biosafety",
    "Sterilization and disinfection",
    "Laboratory safety",
    "Public health microbiology",
]

DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced"]

def parse_quiz_question(text):
    lines = text.strip().split('\n')
    question = ""
    options = {}
    correct = ""
    explanation = ""

    for line in lines:
        line = line.strip()
        if line.startswith("QUESTION:"):
            question = line.replace("QUESTION:", "").strip()
        elif line.startswith("A)"):
            options["A"] = line.replace("A)", "").strip()
        elif line.startswith("B)"):
            options["B"] = line.replace("B)", "").strip()
        elif line.startswith("C)"):
            options["C"] = line.replace("C)", "").strip()
        elif line.startswith("D)"):
            options["D"] = line.replace("D)", "").strip()
        elif line.startswith("CORRECT:"):
            correct = line.replace("CORRECT:", "").strip()
        elif line.startswith("EXPLANATION:"):
            explanation = line.replace("EXPLANATION:", "").strip()

    return question, options, correct, explanation

def show_dashboard_module():
    show_header(
        "Learning Dashboard",
        "Track your progress, test your knowledge, and identify areas for improvement"
    )

    # Initialize session state
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = {"correct": 0, "total": 0}
    if "quiz_history" not in st.session_state:
        st.session_state.quiz_history = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "answer_revealed" not in st.session_state:
        st.session_state.answer_revealed = False
    if "selected_answer" not in st.session_state:
        st.session_state.selected_answer = None

    # Progress overview
    if st.session_state.quiz_score["total"] > 0:
        score = st.session_state.quiz_score
        percentage = int((score["correct"] / score["total"]) * 100)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style="background:#1A2B3C; border:1px solid #25B89A;
                            padding:16px; border-radius:10px; text-align:center;">
                    <h2 style="color:#25B89A; margin:0;">{score["total"]}</h2>
                    <p style="color:#B0C4CE; margin:4px 0 0 0; font-size:12px;">Questions Attempted</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="background:#1A2B3C; border:1px solid #25B89A;
                            padding:16px; border-radius:10px; text-align:center;">
                    <h2 style="color:#25B89A; margin:0;">{score["correct"]}</h2>
                    <p style="color:#B0C4CE; margin:4px 0 0 0; font-size:12px;">Correct Answers</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            color = "#25B89A" if percentage >= 70 else "#F5A623" if percentage >= 50 else "#E05252"
            st.markdown(f"""
                <div style="background:#1A2B3C; border:1px solid {color};
                            padding:16px; border-radius:10px; text-align:center;">
                    <h2 style="color:{color}; margin:0;">{percentage}%</h2>
                    <p style="color:#B0C4CE; margin:4px 0 0 0; font-size:12px;">Score</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

    mode = st.radio(
        "Select Mode",
        ["🧠 Quiz Mode", "📊 Progress Report", "📚 Study Planner", "🔖 Review Wrong Answers"],
        horizontal=False,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Mode 1 — Quiz Mode
    if "Quiz" in mode:
        st.markdown("### 🧠 Quiz Mode")

        col1, col2 = st.columns(2)
        with col1:
            topic = st.selectbox(
                "Select Topic",
                options=["Random — mixed topics"] + QUIZ_TOPICS,
                key="quiz_topic"
            )
        with col2:
            difficulty = st.selectbox(
                "Difficulty Level",
                options=DIFFICULTY_LEVELS,
                key="difficulty"
            )

        generate_clicked = st.button("🎲 Generate New Question", use_container_width=True)

        if generate_clicked:
            topic_text = topic if topic != "Random — mixed topics" else "any microbiology topic"
            prompt = f"""Generate one {difficulty} level multiple choice quiz question about: {topic_text}

The question must be about microbiology, laboratory science, or life sciences.
Follow the exact format specified."""

            with st.spinner("Generating question..."):
                raw_question = ask_claude(
                    system_prompt=SYSTEM_PROMPT,
                    user_message=prompt
                )

            st.session_state.current_question = raw_question
            st.session_state.answer_revealed = False
            st.session_state.selected_answer = None
            st.rerun()

        # Display current question
        if st.session_state.current_question:
            question, options, correct, explanation = parse_quiz_question(
                st.session_state.current_question
            )

            if question and options:
                st.markdown("---")
                st.markdown(f"""
                    <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                                padding:16px; border-radius:10px; margin-bottom:16px;">
                        <p style="color:#E2E8F0; font-size:15px; margin:0; font-weight:bold;">
                            {question}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                if not st.session_state.answer_revealed:
                    answer_cols = st.columns(2)
                    for i, (letter, option_text) in enumerate(options.items()):
                        with answer_cols[i % 2]:
                            if st.button(f"{letter}) {option_text}", key=f"opt_{letter}", use_container_width=True):
                                st.session_state.selected_answer = letter
                                st.session_state.answer_revealed = True
                                st.session_state.quiz_score["total"] += 1
                                if letter == correct:
                                    st.session_state.quiz_score["correct"] += 1
                                st.session_state.quiz_history.append({
                                    "question": question,
                                    "selected": letter,
                                    "correct": correct,
                                    "correct_text": options.get(correct, ""),
                                    "explanation": explanation,
                                    "is_correct": letter == correct,
                                    "topic": topic
                                })
                                st.rerun()

                if st.session_state.answer_revealed and st.session_state.selected_answer:
                    selected = st.session_state.selected_answer
                    is_correct = selected == correct

                    if is_correct:
                        st.markdown(f"""
                            <div style="background:#0D2B1A; border-left:4px solid #25B89A;
                                        padding:16px; border-radius:10px; margin-bottom:12px;">
                                <h4 style="color:#25B89A; margin:0;">✅ Correct! Well done.</h4>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="background:#2D1515; border-left:4px solid #E05252;
                                        padding:16px; border-radius:10px; margin-bottom:12px;">
                                <h4 style="color:#E05252; margin:0;">❌ Incorrect</h4>
                                <p style="color:#FCA5A5; margin:8px 0 0 0;">
                                    You selected: {selected}) {options.get(selected, '')}<br>
                                    Correct answer: {correct}) {options.get(correct, '')}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

                    if explanation:
                        st.markdown(f"""
                            <div style="background:#1A2B3C; border-left:4px solid #1B7F7F;
                                        padding:16px; border-radius:10px;">
                                <h4 style="color:#25B89A; margin:0 0 8px 0;">📖 Explanation</h4>
                                <p style="color:#E2E8F0; margin:0; font-size:13px; line-height:1.7;">
                                    {explanation}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

    # Mode 2 — Progress Report
    elif "Progress" in mode:
        st.markdown("### 📊 Your Progress Report")

        if not st.session_state.quiz_history:
            show_info_card("No quiz attempts yet. Go to Quiz Mode to start testing your knowledge.", "📝")
        else:
            total = st.session_state.quiz_score["total"]
            correct = st.session_state.quiz_score["correct"]
            percentage = int((correct / total) * 100) if total > 0 else 0

            if percentage >= 80:
                level = "🌟 Excellent"
                color = "#25B89A"
                message = "Outstanding performance! You have strong microbiology knowledge."
            elif percentage >= 60:
                level = "👍 Good"
                color = "#F5A623"
                message = "Good progress! Focus on your weak areas to improve further."
            else:
                level = "📚 Keep Studying"
                color = "#E05252"
                message = "Keep practicing. Review the topics where you got wrong answers."

            st.markdown(f"""
                <div style="background:#1A2B3C; border:2px solid {color};
                            padding:20px; border-radius:12px; text-align:center; margin-bottom:20px;">
                    <h2 style="color:{color}; margin:0;">{level}</h2>
                    <p style="color:#B0C4CE; margin:8px 0 0 0;">{message}</p>
                </div>
            """, unsafe_allow_html=True)

            # Topic breakdown
            topic_performance = {}
            for item in st.session_state.quiz_history:
                t = item["topic"]
                if t not in topic_performance:
                    topic_performance[t] = {"correct": 0, "total": 0}
                topic_performance[t]["total"] += 1
                if item["is_correct"]:
                    topic_performance[t]["correct"] += 1

            st.markdown("### 📈 Performance by Topic")
            for topic_name, perf in topic_performance.items():
                pct = int((perf["correct"] / perf["total"]) * 100)
                bar_color = "#25B89A" if pct >= 70 else "#F5A623" if pct >= 50 else "#E05252"
                st.markdown(f"""
                    <div style="background:#1A2B3C; padding:12px; border-radius:8px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                            <span style="color:#E2E8F0; font-size:13px;">{topic_name[:50]}</span>
                            <span style="color:{bar_color}; font-weight:bold;">{pct}%</span>
                        </div>
                        <div style="background:#0D1B2A; border-radius:4px; height:8px;">
                            <div style="background:{bar_color}; width:{pct}%; height:8px; border-radius:4px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # Mode 3 — Study Planner
    elif "Study" in mode:
        st.markdown("### 📚 Personalized Study Planner")

        st.markdown("Tell us about yourself and we'll create a study plan:")

        col1, col2 = st.columns(2)
        with col1:
            level = st.selectbox(
                "Your current level",
                ["-- Select --", "First year student", "Second year student", "Final year student", "Junior lab technician", "Preparing for exams"],
                key="student_level"
            )
            available_time = st.selectbox(
                "Daily study time available",
                ["-- Select --", "30 minutes", "1 hour", "2 hours", "3+ hours"],
                key="study_time"
            )
        with col2:
            exam_date = st.text_input(
                "Exam or goal date (optional)",
                placeholder="e.g. In 2 weeks, June 15...",
                key="exam_date"
            )
            weak_areas = st.multiselect(
                "Your weak areas (select all that apply)",
                options=QUIZ_TOPICS,
                key="weak_areas"
            )

        goal = st.text_area(
            "What is your main goal?",
            placeholder="e.g. Pass my microbiology practical exam, prepare for lab job interview, understand clinical microbiology better...",
            height=80,
            key="study_goal"
        )

        plan_clicked = st.button("📚 Generate My Study Plan", use_container_width=True)

        if plan_clicked:
            if level == "-- Select --":
                st.warning("⚠️ Please select your current level.")
            else:
                prompt = f"""Create a personalized microbiology study plan for:
Level: {level}
Daily time available: {available_time}
{f'Exam/goal date: {exam_date}' if exam_date else ''}
{f'Weak areas: {", ".join(weak_areas)}' if weak_areas else ''}
{f'Main goal: {goal}' if goal else ''}

Create a practical, structured study plan with daily or weekly topics, 
recommended resources, and specific advice for their weak areas."""

                with st.spinner("📚 Creating your study plan..."):
                    plan = ask_claude(
                        system_prompt=SYSTEM_PROMPT,
                        user_message=prompt
                    )

                st.markdown("---")
                st.markdown("### 📋 Your Personalized Study Plan")
                st.markdown(f"""
                    <div style="background:#1A2B3C; border-left:4px solid #25B89A;
                                padding:20px; border-radius:10px;
                                color:#E2E8F0; line-height:1.8; font-size:14px;">
                        {plan.replace(chr(10), '<br>')}
                    </div>
                """, unsafe_allow_html=True)

    # Mode 4 — Review Wrong Answers
    elif "Review" in mode:
        st.markdown("### 🔖 Review Wrong Answers")

        wrong_answers = [item for item in st.session_state.quiz_history if not item["is_correct"]]

        if not wrong_answers:
            show_info_card("No wrong answers to review yet — either you haven't attempted any questions or you got them all correct!", "🎉")
        else:
            st.markdown(f"**{len(wrong_answers)} questions to review:**")
            for i, item in enumerate(wrong_answers, 1):
                with st.expander(f"Question {i} — {item['topic'][:40]}"):
                    st.markdown(f"**Question:** {item['question']}")
                    st.markdown(f"**Your answer:** {item['selected']}")
                    st.markdown(f"**Correct answer:** {item['correct']}) {item['correct_text']}")
                    if item['explanation']:
                        st.markdown(f"**Explanation:** {item['explanation']}")

        if st.session_state.quiz_score["total"] > 0:
            if st.button("🔄 Reset All Progress"):
                st.session_state.quiz_score = {"correct": 0, "total": 0}
                st.session_state.quiz_history = []
                st.session_state.current_question = None
                st.session_state.answer_revealed = False
                st.session_state.selected_answer = None
                st.rerun()