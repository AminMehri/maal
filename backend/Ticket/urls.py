from django.urls import path
from . import views



urlpatterns = [
    path('Conversation/', views.Conversation.as_view()),
    path('Ticket/', views.Ticket.as_view()),

]