from django.urls import path 
from . import views

urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('register',views.UserRegisterView.as_view(),name='register'),
    path('login',views.UserLoginView.as_view(),name='login'),
    path('profile',views.UserProfile,name='profile'),
    path('log_out',views.Logout,name='logout'),
    
]