import os
import re
from questions.models import QuizTopic, Question, Answer

def insert_questions_from_folder(folder_path, topic_name="Cloud Basics-AZ-900"):
    # Get or create topic
    topic, _ = QuizTopic.objects.get_or_create(name=topic_name)

    # Loop through all .txt files
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Extract question number from filename (e.g., q1.txt → 1, 920.txt → 920)
            match = re.search(r'\d+', filename)
            if not match:
                print(f"❌ Skipping {filename}: no number found.")
                continue

            question_number = int(match.group())
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) < 5:
                print(f"⚠️ Skipping {filename}: not enough lines.")
                continue

            # Split into question and answers
            question_text = " ".join(lines[:-4])
            choices = lines[-4:]

            # Create question with question_number
            question = Question.objects.create(
                topic=topic,
                question_number=question_number,
                text=question_text,
                allow_multiple=False
            )

            # Insert answers
            for choice_text in choices:
                Answer.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=False  # To be updated later
                )

            print(f"✅ Q{question_number} added from {filename}: '{question_text[:50]}...'")

# Example call:
folder = r"C:\Users\User\Desktop\AZ-SolArchitect-Train\Screenshots\AZ-900-Crop\ext1-full"
insert_questions_from_folder(folder)
