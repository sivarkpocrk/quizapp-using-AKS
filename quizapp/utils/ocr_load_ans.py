import os
import re
from django.db import transaction
from questions.models import Question, Answer, Comment

def clean_answer_text(text):
    return re.sub(r"^[(@©)\s]+", '', text).strip().lower()

def extract_from_text(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    # Match correct answers (start with @, ©, (@, (©, etc.)
    correct_lines = [line for line in lines if re.match(r"^[(]*[@©]", line)]
    correct_texts = [clean_answer_text(line) for line in correct_lines]

    # Assume the last 5 lines form the comment
    comment_lines = lines[-5:]
    comment_text = ' '.join(comment_lines)

    return correct_texts, comment_text

def extract_question_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

@transaction.atomic
def update_answers_from_folder(folder_path):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

    for file in files:
        question_number = extract_question_number(file)
        if question_number is None:
            print(f"❌ Skipping {file}: no number found.")
            continue

        file_path = os.path.join(folder_path, file)
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        correct_texts, comment_text = extract_from_text(content)

        try:
            question = Question.objects.get(question_number=question_number)
        except Question.DoesNotExist:
            print(f"❌ Question with question_number={question_number} not found.")
            continue

        print(f"🔄 Updating Q{question_number} with correct answers: {correct_texts}")

        # Update answers
        correct_count = 0
        for answer in question.answers.all():
            cleaned_db_text = clean_answer_text(answer.text)
            if cleaned_db_text in correct_texts:
                answer.is_correct = True
                correct_count += 1
            else:
                answer.is_correct = False
            answer.save()

        # Update question flags
        question.correct_answer_count = correct_count
        question.allow_multiple = correct_count > 1
        question.save()

        # Add or update comment
        Comment.objects.update_or_create(
            question=question,
            defaults={"text": comment_text}
        )

        print(f"✅ Updated Q{question_number} → {correct_count} correct answer(s), allow_multiple={question.allow_multiple}")

# Example usage
folder = r"C:\Users\User\Desktop\AZ-SolArchitect-Train\Screenshots\AZ-900-Crop\ext3-ans"
update_answers_from_folder(folder)
