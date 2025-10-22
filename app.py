import streamlit as st
import anthropic
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Quiz App",
    page_icon="🎯",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .option-button {
        width: 100%;
        text-align: left;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        background-color: white;
        cursor: pointer;
        transition: all 0.3s;
    }
    .correct-answer {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .incorrect-answer {
        background-color: #f8d7da;
        border-color: #dc3545;
    }
    .score-box {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 10px;
        font-size: 1.5rem;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'grading_results' not in st.session_state:
    st.session_state.grading_results = None
if 'topic' not in st.session_state:
    st.session_state.topic = ""

def get_anthropic_client():
    """Get Anthropic client instance."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found in environment variables!")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

@st.cache_data(show_spinner=False)
def generate_questions(topic: str) -> list:
    """Generate questions using Claude API with caching to save API calls."""
    client = get_anthropic_client()

    prompt = f"""Generate 5 multiple-choice questions about {topic}.

For each question, provide:
1. The question text
2. Four answer options (A, B, C, D)
3. The correct answer (letter only)

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "A"
  }}
]

Make the questions interesting and educational. Ensure only one answer is correct for each question."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    start_idx = response_text.find('[')
    end_idx = response_text.rfind(']') + 1

    if start_idx != -1 and end_idx > start_idx:
        json_str = response_text[start_idx:end_idx]
        return json.loads(json_str)
    else:
        raise ValueError("Could not parse questions from Claude's response")

def grade_quiz(questions: list, user_answers: dict) -> list:
    """Grade the quiz using Claude API."""
    client = get_anthropic_client()

    quiz_data = []
    for i, question in enumerate(questions):
        user_answer = user_answers.get(i, "Not answered")
        quiz_data.append({
            "question_number": i + 1,
            "question": question['question'],
            "options": question['options'],
            "correct_answer": question['correct_answer'],
            "user_answer": user_answer
        })

    prompt = f"""Here is a quiz and the user's answers. Please grade the quiz and provide explanations.

Quiz data:
{json.dumps(quiz_data, indent=2)}

For each question, provide:
1. Whether the user's answer was correct or incorrect
2. A clear explanation of why the correct answer is correct
3. If the user was wrong, explain why their answer was incorrect

Format your response as a JSON array:
[
  {{
    "question_number": 1,
    "correct": true/false,
    "explanation": "Detailed explanation here"
  }}
]"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    start_idx = response_text.find('[')
    end_idx = response_text.rfind(']') + 1

    if start_idx != -1 and end_idx > start_idx:
        json_str = response_text[start_idx:end_idx]
        return json.loads(json_str)
    else:
        raise ValueError("Could not parse grading from Claude's response")

# Header
st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Quiz App</h1>
        <p>Test your knowledge on any topic!</p>
    </div>
""", unsafe_allow_html=True)

# Main app logic
if not st.session_state.questions:
    # Topic input phase
    st.markdown("### 📚 Choose Your Topic")
    topic = st.text_input(
        "Enter a topic for your quiz:",
        placeholder="e.g., Python Programming, World History, Physics...",
        key="topic_input"
    )

    if st.button("🚀 Generate Quiz", type="primary", use_container_width=True):
        if topic.strip():
            with st.spinner("🤔 Generating quiz questions... (This uses 1 API call)"):
                try:
                    questions = generate_questions(topic.strip())
                    st.session_state.questions = questions
                    st.session_state.topic = topic.strip()
                    st.session_state.user_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.grading_results = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating questions: {e}")
        else:
            st.warning("⚠️ Please enter a topic!")

elif not st.session_state.quiz_submitted:
    # Quiz taking phase
    st.markdown(f"### 📝 Quiz: {st.session_state.topic}")
    st.markdown("---")

    for i, question in enumerate(st.session_state.questions):
        st.markdown(f"**Question {i + 1}:** {question['question']}")

        # Radio buttons for options
        options = question['options']
        option_list = [f"{key}. {value}" for key, value in options.items()]

        selected = st.radio(
            "Select your answer:",
            options=option_list,
            key=f"q_{i}",
            index=None
        )

        if selected:
            st.session_state.user_answers[i] = selected[0]  # Store just the letter (A, B, C, D)

        st.markdown("---")

    # Submit button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📊 Submit Quiz", type="primary", use_container_width=True):
            if len(st.session_state.user_answers) == len(st.session_state.questions):
                with st.spinner("⏳ Grading your quiz... (This uses 1 API call)"):
                    try:
                        results = grade_quiz(st.session_state.questions, st.session_state.user_answers)
                        st.session_state.grading_results = results
                        st.session_state.quiz_submitted = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error grading quiz: {e}")
            else:
                st.warning(f"⚠️ Please answer all {len(st.session_state.questions)} questions!")

    with col2:
        if st.button("🔄 New Topic", use_container_width=True):
            st.session_state.questions = None
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.grading_results = None
            st.session_state.topic = ""
            st.rerun()

else:
    # Results phase
    st.markdown(f"### 📊 Quiz Results: {st.session_state.topic}")

    # Calculate score
    correct_count = sum(1 for result in st.session_state.grading_results if result['correct'])
    total_questions = len(st.session_state.grading_results)
    score_percentage = (correct_count / total_questions) * 100

    # Score display
    st.markdown(f"""
        <div class="score-box">
            <h2>Your Score: {correct_count}/{total_questions}</h2>
            <p>{score_percentage:.1f}%</p>
        </div>
    """, unsafe_allow_html=True)

    # Detailed results
    st.markdown("### 📝 Detailed Results")

    for i, result in enumerate(st.session_state.grading_results):
        question = st.session_state.questions[i]
        user_answer = st.session_state.user_answers.get(i, "Not answered")
        correct_answer = question['correct_answer']

        # Question header
        if result['correct']:
            st.success(f"✅ Question {result['question_number']}")
        else:
            st.error(f"❌ Question {result['question_number']}")

        # Question text
        st.markdown(f"**{question['question']}**")

        # Show all options with highlighting
        for key, value in question['options'].items():
            if key == correct_answer:
                st.markdown(f"✅ **{key}. {value}** (Correct Answer)")
            elif key == user_answer and not result['correct']:
                st.markdown(f"❌ **{key}. {value}** (Your Answer)")
            else:
                st.markdown(f"{key}. {value}")

        # Explanation
        st.info(f"**Explanation:** {result['explanation']}")
        st.markdown("---")

    # Action buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Try Another Quiz", type="primary", use_container_width=True):
            st.session_state.questions = None
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.grading_results = None
            st.session_state.topic = ""
            st.rerun()

    with col2:
        if st.button("🔁 Retake This Quiz", use_container_width=True):
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.grading_results = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>💡 Tip: Questions are cached to minimize API calls. Same topic = no new API call!</p>
        <p>Powered by Claude AI | Total API calls per quiz: 2 (generate + grade)</p>
    </div>
""", unsafe_allow_html=True)
