from django.urls import path
from Ticket import views



urlpatterns = [
    path('Conversation/', views.ConversationView.as_view()),
    path('Ticket/', views.TicketView.as_view()),
    path('CloseCoversation/', views.CloseCoversation.as_view()),

]