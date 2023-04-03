from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('signup/', views.SignUp.as_view()),
    path('', views.UserInfo.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sendVerifyEmail/', views.CreateEmailToken.as_view()),
    path('submitVerifyEmail/', views.VerifyEmail.as_view()),
    path('forgetPassword/', views.ForgetPassword.as_view()),
    path('setPassword/', views.SetPassword.as_view()),
    # set instagram account
    # setup freelancer account
    # get freelancer account status (pending - accepted - rejected with reason)
    # get insta account overview ( if not verified: not found )
    # get own account rules
]
