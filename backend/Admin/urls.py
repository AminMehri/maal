from django.urls import path
from . import views



urlpatterns = [
    path('AcceptWithdraw/', views.AcceptWithdraw.as_view()),
    path('ShowFreelancers/', views.ShowFreelancers.as_view()),
    path('ShowFreelancerHistory/', views.ShowFreelancerHistory.as_view()),
    path('AcceptFreelancer/', views.AcceptFreelancer.as_view()),
    path('RejectFreelancer/', views.RejectFreelancer.as_view()),
    path('ShowTickets/', views.ShowTickets.as_view()),
    path('ShowProjects/', views.ShowProjects.as_view()),
    path('ShowSingleProject/', views.ShowSingleProject.as_view()),
    path('ConfirmProject/', views.ConfirmProject.as_view()),
    path('RejectProject/', views.RejectProject.as_view()),
    
    
    
    
    
    # get withdraw                                         #DONE
    # post withdraw                                        #DONE
    # get freelancers list                                 #DONE
    # get freelancer history                               #DONE
    # post freelancer                                      #DONE
    # get tickets                                          #DONE
    # get Projects list (first admin_confirmed=False)      #DONE
    # get project detail                                   #DONE
    # post project confirm if admin_confirmed=False        #DONE
    # don't confirm project by admin for a reason          #DONE
    # reject freelancer                                    #DONE

    # respond to ticket                  


    # check AcceptedProject (بر اساس نزدیک ترین تایم های استوری ها به پاک شدن, بزاره که چک)    #نمیفهمم چی میگه
]
