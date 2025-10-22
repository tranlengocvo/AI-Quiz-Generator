import anthropic
import json
import os
import sys
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fix Windows encoding issue
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class QuizApp:
    def __init__(self):
        """Initialize the quiz app with Claude API client."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.questions = []
        self.user_answers = []

    def generate_questions(self, topic: str) -> List[Dict]:
        """Generate 5 multiple-choice questions on the given topic using Claude."""
        print(f"\n🤔 Generating quiz questions about '{topic}'...\n")

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

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the response to extract JSON
        response_text = message.content[0].text

        # Try to find JSON in the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1

        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            self.questions = json.loads(json_str)
        else:
            raise ValueError("Could not parse questions from Claude's response")

        return self.questions

    def display_question(self, question_num: int, question_data: Dict):
        """Display a single question with its options."""
        print(f"\nQuestion {question_num + 1}:")
        print(f"{question_data['question']}\n")

        for letter, option in question_data['options'].items():
            print(f"  {letter}. {option}")
        print()

    def take_quiz(self):
        """Present questions to the user and collect their answers."""
        print("\n" + "="*60)
        print("QUIZ TIME! Answer each question by entering A, B, C, or D")
        print("="*60)

        self.user_answers = []

        for i, question in enumerate(self.questions):
            self.display_question(i, question)

            while True:
                answer = input("Your answer: ").strip().upper()
                if answer in ['A', 'B', 'C', 'D']:
                    self.user_answers.append(answer)
                    break
                else:
                    print("Invalid input. Please enter A, B, C, or D.")

    def grade_quiz(self):
        """Send answers to Claude for grading and explanations."""
        print("\n📊 Grading your quiz and generating explanations...\n")

        # Prepare quiz data for grading
        quiz_data = []
        for i, (question, user_answer) in enumerate(zip(self.questions, self.user_answers)):
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

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=3000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the grading response
        response_text = message.content[0].text
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1

        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            grading_results = json.loads(json_str)
        else:
            raise ValueError("Could not parse grading from Claude's response")

        return grading_results

    def display_results(self, grading_results: List[Dict]):
        """Display the quiz results with explanations."""
        print("\n" + "="*60)
        print("QUIZ RESULTS")
        print("="*60)

        correct_count = sum(1 for result in grading_results if result['correct'])
        total_questions = len(grading_results)
        score_percentage = (correct_count / total_questions) * 100

        for i, result in enumerate(grading_results):
            question = self.questions[i]
            user_answer = self.user_answers[i]
            correct_answer = question['correct_answer']

            print(f"\nQuestion {result['question_number']}: {question['question']}")

            if result['correct']:
                print(f"✓ CORRECT! Your answer: {user_answer}")
            else:
                print(f"✗ INCORRECT. Your answer: {user_answer}, Correct answer: {correct_answer}")

            print(f"\nExplanation: {result['explanation']}")
            print("-" * 60)

        print(f"\n{'='*60}")
        print(f"FINAL SCORE: {correct_count}/{total_questions} ({score_percentage:.1f}%)")
        print(f"{'='*60}\n")

        if score_percentage >= 80:
            print("🎉 Excellent work!")
        elif score_percentage >= 60:
            print("👍 Good job!")
        else:
            print("📚 Keep studying!")

    def run(self):
        """Main method to run the quiz app."""
        print("\n" + "="*60)
        print("WELCOME TO THE AI QUIZ APP")
        print("="*60)

        topic = input("\nEnter a topic for your quiz: ").strip()

        if not topic:
            print("No topic provided. Exiting.")
            return

        try:
            # Generate questions
            self.generate_questions(topic)

            # Take the quiz
            self.take_quiz()

            # Grade and get explanations
            grading_results = self.grade_quiz()

            # Display results
            self.display_results(grading_results)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return


def main():
    """Entry point for the quiz app."""
    try:
        app = QuizApp()
        app.run()
    except ValueError as e:
        print(f"\n❌ {e}")
        print("Please set your ANTHROPIC_API_KEY environment variable.")
    except KeyboardInterrupt:
        print("\n\nQuiz cancelled by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
