from django.urls import path
from .views import home, quiz

urlpatterns = [
    path('', home, name='home'),
    path('quiz/<int:topic_id>/', quiz, name='quiz'),
]
