from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Answer, Question

def update_question_correct_info(question):
    # Count how many answers are marked correct
    correct_count = question.answers.filter(is_correct=True).count()

    # Automatically set allow_multiple based on correct answers
    question.has_correct_answer = correct_count > 0
    question.correct_answer_count = correct_count
    question.allow_multiple = correct_count > 1

    # Save updated fields
    question.save(update_fields=[
        'has_correct_answer',
        'correct_answer_count',
        'allow_multiple'
    ])

@receiver(post_save, sender=Answer)
def update_question_on_answer_save(sender, instance, **kwargs):
    update_question_correct_info(instance.question)

@receiver(post_delete, sender=Answer)
def update_question_on_answer_delete(sender, instance, **kwargs):
    update_question_correct_info(instance.question)
