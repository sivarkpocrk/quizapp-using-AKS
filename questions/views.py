from django.shortcuts import render, redirect, get_object_or_404
from .models import QuizTopic, Question, Answer

def home(request):
    quiz_topics = QuizTopic.objects.all()
    return render(request, 'questions/home.html', {'quiz_topics': quiz_topics})

def quiz(request, topic_id):
    topic = get_object_or_404(QuizTopic, pk=topic_id)
    questions = Question.objects.filter(topic=topic).order_by('id')
    total_questions = questions.count()

    # Get current question index from session or start from 0
    current_question = request.session.get('current_question', 0)

    # Reset the quiz if it is the first question or if requested explicitly
    if current_question == 0:
        request.session['current_question'] = 0

    # End quiz if no more questions
    if current_question >= total_questions:
        # Reset the session counter for future quizzes
        request.session['current_question'] = 0
        return render(request, 'questions/quiz_complete.html', {'topic': topic})

    # Fetch the current question
    question = questions[current_question]
    progress_percentage = int((current_question / total_questions) * 100)

    result = None
    selected_answer_ids = []

    if request.method == 'POST':
        selected_answers = request.POST.getlist('answer')
        selected_answer_ids = [int(a) for a in selected_answers]

        if 'check' in request.POST:
            # Check button pressed
            correct_answers = Answer.objects.filter(question=question, is_correct=True).values_list('id', flat=True)
            is_correct = set(selected_answer_ids) == set(correct_answers)

            if is_correct:
                result = "Correct!"
                request.session['correct_count'] = request.session.get('correct_count', 0) + 1
            else:
                result = "Incorrect!"

        elif 'next' in request.POST:
            # Move to the next question
            current_question += 1
            request.session['current_question'] = current_question
            return redirect('quiz', topic_id=topic.id)

    return render(request, 'questions/quiz.html', {
        'topic': topic,
        'question': question,
        'answers': question.answers.all(),
        'total_questions': total_questions,
        'current_question': current_question + 1,
        'progress_percentage': progress_percentage,
        'result': result,
        'selected_answer_ids': selected_answer_ids
    })
