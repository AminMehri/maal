from django.urls import path
from . import views



urlpatterns = [
    path('AcceptWithdraw/', views.AcceptWithdraw.as_view()),
    path('ShowFreelancers/', views.ShowFreelancers.as_view()),
    path('ShowFreelancerHistory/', views.ShowFreelancerHistory.as_view()),
    path('AcceptFreelancer/', views.AcceptFreelancer.as_view()),
    path('RejectFreelancer/', views.RejectFreelancer.as_view()),
    path('ShowProjects/', views.ShowProjects.as_view()),
    path('ShowSingleProject/', views.ShowSingleProject.as_view()),
    path('ConfirmProject/', views.ConfirmProject.as_view()),
    path('RejectProject/', views.RejectProject.as_view()),
    path('ShowFreelancersPublishProject/', views.ShowFreelancersPublishProject.as_view()),
    path('CheckStoryOnStart/', views.CheckStoryOnStart.as_view()),
    path('CheckStoryAtEnd/', views.CheckStoryAtEnd.as_view()),
    path('AdminAwnserTicketView/', views.AdminAwnserTicketView.as_view()),
    path('ShowConversationsView/', views.ShowConversationsView.as_view()),
    path('ShowSingleConversationView/', views.ShowSingleConversationView.as_view()),
    path('CloseConversationView/', views.CloseConversationView.as_view()),
    path('ShowConversationsAdminHistory/', views.ShowConversationsAdminHistory.as_view()),
    

    # '''
    #     هر دوتای اینا باید توی ویو گت پروژه انجام شه
        
    #     اعلام کنیم ک یه پروژه پابلیش شده و به کسایی ک اونو قبول کردن اس ام اس بدیم
    #     یه پروژه کی فول میشه و وقتی شد پابلیش رو ترو کنیم
    
    # '''
]
