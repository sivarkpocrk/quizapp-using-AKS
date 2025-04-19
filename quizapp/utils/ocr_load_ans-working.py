import os
import re
from django.db import transaction
from questions.models import Question, Answer, Comment

def clean_answer_text(text):
    return re.sub(r"^[(@©)\s]+", '', text).strip().lower()

def extract_from_text(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    # Match correct answers (start with @, (@, etc.)
    correct_lines = [line for line in lines if re.match(r"^[(]*[@©]", line)]
    correct_texts = [re.sub(r"^[(@©)\s]+", '', line).strip() for line in correct_lines]

    # Assume last few lines are comments
    comment_lines = lines[-5:]
    comment_text = ' '.join(comment_lines)

    return correct_texts, comment_text

@transaction.atomic
def update_answers_from_folder(folder_path):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

    for idx, file in enumerate(files, start=1):  # assuming files are in order Q1, Q2, ...
        file_path = os.path.join(folder_path, file)
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        correct_texts, comment_text = extract_from_text(content)

        try:
            question = Question.objects.get(id=idx)
        except Question.DoesNotExist:
            print(f"❌ Question ID {idx} not found.")
            continue

        print(f"🔄 Updating Question ID {idx} with correct answers: {correct_texts}")

        # Update all answers for the question
        # Update correct answers
        correct_count = 0
        cleaned_correct_texts = [clean_answer_text(ans) for ans in correct_texts]

        for answer in question.answers.all():
            cleaned_db_text = clean_answer_text(answer.text)
            if cleaned_db_text in cleaned_correct_texts:
                answer.is_correct = True
                correct_count += 1
            else:
                answer.is_correct = False
            answer.save()

        # Update question fields
        question.correct_answer_count = correct_count
        question.allow_multiple = correct_count > 1
        question.save()

        # Update or create comment
        Comment.objects.update_or_create(
            question=question,
            defaults={"text": comment_text}
        )

        print(f"✅ Updated Question {idx} with {correct_count} correct answer(s), allow_multiple = {question.allow_multiple}")


# Run in Django shell:
# python manage.py shell
# >>> from your_script import update_answers_from_folder
# >>> update_answers_from_folder("C:/path/to/crop-ans")
# Example usage
base_folder = r"C:\Users\User\Desktop\AZ-SolArchitect-Train\Screenshots\AZ-900-Crop\ext3-ans"
output_file = "extracted_answers.xlsx"
update_answers_from_folder(base_folder)
