from django.urls import path
from . import views

urlpatterns = [
    path('initialize_model/', views.initialize_model, name='initialize_model'),
    path('move_agent/', views.move_agent, name='move_agent'),
    path('delete_agent/<int:agent_id>/', views.delete_agent, name='delete_agent'),
    path('delete_all_agents/', views.delete_all_agents, name='delete_all_agents'),
    path('', views.root_page, name='root_page'),
]