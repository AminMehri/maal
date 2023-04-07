from django.urls import path
from . import views



urlpatterns = [
    path('CreateTicket/', views.CreateTicket.as_view()),

]