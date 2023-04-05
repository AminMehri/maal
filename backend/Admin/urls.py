
from django.urls import path
from . import views



urlpatterns = [
    path('AcceptWithdraw/', views.AcceptWithdraw.as_view()),
    path('ShowFreelancers/', views.ShowFreelancers.as_view()),
    path('ShowFreelancerHistory/', views.ShowFreelancerHistory.as_view()),
    
    # get withdraw                       #DONE
    # post withdraw                      #DONE
    # get freelancers list               #DONE
    # get freelancer history             #DONE
    # post freelancer
    # get ticket
    # post ticket

    # get Projects list (first admin_confirmed=False)
    # get project detail
    # post project confirm if admin_confirmed=False

    # check AcceptedProject (بر اساس نزدیک ترین تایم های استوری ها به پاک شدن, بزاره که چک)
]