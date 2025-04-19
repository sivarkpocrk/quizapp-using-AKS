from django.shortcuts import render, redirect, get_object_or_404
from .models import QuizTopic, Question, Answer
from analytics.models import UserQuizAttempt, UserAnswer


def home(request):
    quiz_topics = QuizTopic.objects.all()
    return render(request, 'questions/home.html', {'quiz_topics': quiz_topics})

def quiz(request, topic_id):
    topic = get_object_or_404(QuizTopic, pk=topic_id)
    questions = list(Question.objects.filter(topic=topic).order_by('question_number'))
    total_questions = len(questions)

    # Get current question index from session
    current_index = request.session.get('current_question', 0)

    if current_index == 0:
        request.session['correct_count'] = 0  # Reset score at start

    if current_index >= total_questions:
        score = request.session.get('correct_count', 0)
        percentage = int((score / total_questions) * 100) if total_questions else 0

        # ✅ Save the quiz attempt if user is logged in
        if request.user.is_authenticated:
            attempt = UserQuizAttempt.objects.create(
                user=request.user,
                topic=topic,
                score=score
            )

            for q in questions:
                submitted_ids = request.session.get(f"question_{q.id}_selected", [])
                for ans_id in submitted_ids:
                    try:
                        answer_obj = Answer.objects.get(id=ans_id)
                        is_correct = answer_obj.is_correct
                        UserAnswer.objects.create(
                            attempt=attempt,
                            question=q,
                            answer=answer_obj,
                            is_correct=is_correct
                        )
                    except Answer.DoesNotExist:
                        continue

        # ✅ Clean up session
        request.session.pop('current_question', None)
        request.session.pop('correct_count', None)

        # Optionally clean up stored selections
        for q in questions:
            request.session.pop(f"question_{q.id}_selected", None)

        return render(request, 'questions/quiz_summary.html', {
            'topic': topic,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage
        })

    question = questions[current_index]
    answers = question.answers.all()
    selected_answer_ids = []
    missed_answer_ids = []
    result = None
    comment_text = None

    if request.method == 'POST':
        selected_answer_ids = list(map(int, request.POST.getlist('answer')))

        # Save user's selection in session for analytics later
        request.session[f"question_{question.id}_selected"] = selected_answer_ids

        correct_answer_ids = list(answers.filter(is_correct=True).values_list('id', flat=True))

        selected_set = set(selected_answer_ids)
        correct_set = set(correct_answer_ids)

        if 'check' in request.POST:
            if selected_set == correct_set:
                result = "✅ Correct!"
                # request.session['correct_count'] += 1
                request.session['correct_count'] = request.session.get('correct_count', 0) + 1
            elif selected_set & correct_set:
                missed_answer_ids = list(correct_set - selected_set)
                result = f"⚠️ Partially correct. Missed {len(missed_answer_ids)} correct answer(s)."
            else:
                missed_answer_ids = correct_answer_ids
                result = "❌ Incorrect."

            # Get comment if available
            try:
                comment_text = question.comment.text
            except:
                comment_text = None

        elif 'next' in request.POST:
            request.session['current_question'] = current_index + 1
            return redirect('quiz', topic_id=topic.id)

    return render(request, 'questions/quiz.html', {
        'topic': topic,
        'question': question,
        'answers': answers,
        'total_questions': total_questions,
        'current_question': current_index + 1,
        'progress_percentage': int((current_index + 1) / total_questions * 100),
        'result': result,
        'selected_answer_ids': selected_answer_ids,
        'missed_answer_ids': missed_answer_ids,
        'comment_text': comment_text
    })
