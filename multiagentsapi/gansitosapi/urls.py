from django.urls import path
from .views import move_agent

urlpatterns = [
    path('move/', move_agent, name='move_agent'),
]
