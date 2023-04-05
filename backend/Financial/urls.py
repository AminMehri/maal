from django.urls import path
from . import views



urlpatterns = [
    path('withdraw/', views.WithdrawRequest.as_view()),
    path('getBalance/', views.GetBalance.as_view()),
    path('deposit/', views.Deposit.as_view()),
    path('verifyPay/', views.ZarinVerify.as_view()),
    
]
