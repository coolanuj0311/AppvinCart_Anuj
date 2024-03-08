from django.urls import path
from .import views
from accounted.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserRegistrationView, UserPasswordResetView,UserProfileView
  
urlpatterns = [
   
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/login/', UserLoginView.as_view(), name='register/login'),
     path('profileAPI/', UserProfileView.as_view(), name='profileAPI'),
 
    
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

]