from django.urls import path
from . import views



urlpatterns = [
    path('WithdrawRequest/', views.WithdrawRequest.as_view()),
    # get balance
    # deposit money
    # withdraw money (create withdraw request in admins panel)
]
