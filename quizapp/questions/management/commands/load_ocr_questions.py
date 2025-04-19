from django.core.management.base import BaseCommand
from questions.utils.ocr_loader import insert_questions_from_folder

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        folder = r"C:\Users\User\Desktop\AZ-SolArchitect-Train\Screenshots\AZ-900-Crop\ext1"
        insert_questions_from_folder(folder)
