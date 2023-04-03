from django.urls import path
from . import views



urlpatterns = [
    # path('setPassword/', views.SetPassword.as_view()),

# global request:
    # get Projects (پروژه های فعال (پر نشده))
    # get Project detail 

# for client:
    # get my projects history
    # get my project detail history     (فرقش با اونی که توی گلوباله, اینه که میتونه پروژه ش مال گذشته باشه)
    # cancle project (فقط اگه هنوز پابلیش نشده باشه)
    # post project
    # get projects freelancers detail 

# for freelancer:
    # get for me project (پروژه هارو به ترتیبی که به درد طرف میخوره بیاره (آخرین-گرونترین-کتگوری مرتبط و ...))
    # post    project accept request    (همزمان چک کنه پروژه تکمیل نباشه)
    # get accepted Project history list
    # get accepted Project history detail
    # post accepted project done    (ینی بگه استوریو گذاشتم)
]
