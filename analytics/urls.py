from django.urls import path
from .views import user_analytics

urlpatterns = [
    path('', user_analytics, name='user_analytics'),
]
