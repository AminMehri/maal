from django.urls import path
from Project import views



urlpatterns = [
    path('CreateProject/', views.CreateProject.as_view()),
    path('ShowProjects/', views.ShowProjects.as_view()),
    path('ShowProjectsHistory/', views.ShowProjectsHistory.as_view()),
    path('ShowSingleProject/', views.ShowSingleProject.as_view()),
    path('DeleteProject/', views.DeleteProject.as_view()),
    path('CancelAcceptedProject/', views.CancelAcceptedProject.as_view()),
    path('GetProject/', views.GetProject.as_view()),
    path('ShowAcceptedProjectHistory/', views.ShowAcceptedProjectHistory.as_view()),
    path('SubmitStory/', views.SubmitStory.as_view()),

]
