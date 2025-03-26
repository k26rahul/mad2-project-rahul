from flask import Blueprint, jsonify, request
from flask_security import current_user, roles_required
from db.models import db, QuizAttempt, Quiz
from app.celery_tasks import send_email_task
from datetime import datetime

user_bp = Blueprint('user', __name__)


def _construct_attempt_dict(attempt):
  attempt_dict = attempt.as_dict()
  total_questions = len(attempt.quiz.questions)
  correct_questions = attempt.score  # since each question is 1 mark
  attempt_dict.update({
      'total_questions': total_questions,
      'correct_questions': correct_questions,
      'incorrect_questions': total_questions - correct_questions,
      'percentage': (attempt.score / total_questions) * 100 if total_questions > 0 else 0,
      'quiz_title': attempt.quiz.title,
      'chapter_name': attempt.quiz.chapter.name,
      'subject_name': attempt.quiz.chapter.subject.name
  })
  return attempt_dict


@user_bp.route('/quiz-attempts', methods=['GET'])
@roles_required('user')
def get_quiz_attempts():
  attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
  result = [_construct_attempt_dict(attempt) for attempt in attempts]
  return jsonify(success=True, attempts=result)


"""
Sample request payload for creating an attempt:

{
  "answers": {
    "1": 2,
    "2": 1,
    "3": 4
    // ... where keys are question IDs and values are selected options (1-4)
  }
}

Sample response:

{
  "answer_feedback": {
    "2": {
      "correct": false,
      "submitted": 2
    },
    "3": {
      "correct": true,
      "submitted": 1
    },
    "4": {
      "correct": true,
      "submitted": 3
    },
    "5": {
      "correct": true,
      "submitted": 1
    }
  },
  "attempt": {
    "attempted_at": "2025-03-25T13:33:05.692902",
    "chapter_name": "Calculus",
    "correct_questions": 3,
    "id": 17,
    "incorrect_questions": 2,
    "percentage": 60.0,
    "quiz_id": 1,
    "quiz_title": "Basic Calculus Quiz",
    "score": 3,
    "subject_name": "Mathematics",
    "total_questions": 5,
    "user_id": 2
  },
  "message": "Quiz attempt recorded successfully",
  "success": true
}

"""


@user_bp.route('/quiz-attempts/<int:quiz_id>', methods=['POST'])
@roles_required('user')
def create_quiz_attempt(quiz_id):
  # Get answers from request
  data = request.get_json()
  answers = data.get('answers')

  if not answers or not isinstance(answers, dict) or len(answers) == 0:
    return jsonify(
        success=False,
        message="Please provide at least one answer"
    ), 400

  # Find the quiz
  quiz = Quiz.query.get_or_404(quiz_id)

  # Track score and answers
  total_score = 0
  answer_feedback = {}

  # Process only submitted answers
  for question in quiz.questions:
    q_id = str(question.id)
    if q_id in answers:
      answer = answers[q_id]

      # Validate answer format
      if not isinstance(answer, int) or answer < 1 or answer > 4:
        return jsonify(
            success=False,
            message=f"Invalid answer format for question {q_id}. Must be integer 1-4"
        ), 400

      # Calculate score and track feedback
      is_correct = answer == question.correct_option
      if is_correct:
        total_score += 1

      answer_feedback[q_id] = {
          'submitted': answer,
          'correct': is_correct
      }

  # Create attempt record
  attempt = QuizAttempt(
      user_id=current_user.id,
      quiz_id=quiz_id,
      score=total_score
  )

  db.session.add(attempt)
  db.session.commit()

  return jsonify(
      success=True,
      attempt=_construct_attempt_dict(attempt),
      answer_feedback=answer_feedback,
      message="Quiz attempt recorded successfully"
  )


@user_bp.route('/send-test-email', methods=['GET'])
@roles_required('user')
def send_test_email():
  email = current_user.email
  name = current_user.name
  current_time = datetime.now().strftime("%I:%M %p on %B %d, %Y")

  email_body = f"Hi {name}, this is a test email from Quiz Master at {current_time}! We're glad to have you here."
  send_email_task.delay(email, "Welcome to Quiz Master", email_body)

  return jsonify(success=True, message=f"Test email sent to {email}!")
