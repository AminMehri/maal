from django.urls import path
from . import views



urlpatterns = [
    path('CreateProject/', views.CreateProject.as_view()),
    path('ShowProjects/', views.ShowProjects.as_view()),
    path('ShowProjectsHistory/', views.ShowProjectsHistory.as_view()),
    path('ShowSingleProject/', views.ShowSingleProject.as_view()),
    path('DeleteProject/', views.DeleteProject.as_view()),
    path('GetProject/', views.GetProject.as_view()),
    path('ShowAcceptedProjectHistory/', views.ShowAcceptedProjectHistory.as_view()),
    
    
    
    

# global request:
    # get Projects (پروژه های فعال (پر نشده))                  #DONE
    # get Project detail                                    #DONE

# for client:
    # get my projects history                               #DONE
    # get my project detail history                         #DONE
    # cancle project (فقط اگه هنوز پابلیش نشده باشه)            #DONE
    # post project                                          #DONE
    # get projects freelancers detail                       #DONE

# for freelancer:
    # get for me project (پروژه هارو به ترتیبی که به درد طرف میخوره بیاره (آخرین-گرونترین-کتگوری مرتبط و ...))
    # post    project accept request    (همزمان چک کنه پروژه تکمیل نباشه)          #DONE
    # get accepted Project history list                                        #DONE
    # get accepted Project history detail                                      #THERE IS NOTHING TO SHOW
    # post accepted project done    (ینی بگه استوریو گذاشتم)                       #کجا بگه؟ به کی بگه؟
]
