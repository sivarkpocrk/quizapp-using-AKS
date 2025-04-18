from django.apps import AppConfig

class QuestionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questions'

    def ready(self):
        import questions.signals  # 👈 Import the signal file here

