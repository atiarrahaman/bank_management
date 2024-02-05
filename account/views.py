from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import FormView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from . forms import UserCreateForm
from django.contrib import messages

from django.contrib.auth import login,logout
# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class UserRegisterView(FormView):
    template_name='signup.html'
    form_class=UserCreateForm
    success_url=reverse_lazy('register')
    
    def form_valid(self,form):
        messages.success(self.request,'Account create successfull')
        form.save()
        
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name='userlogin.html'
    def get_success_url(self):
        return reverse_lazy('profile')

def Logout(request):
    logout(request)
    return redirect('login')



def UserProfile(request):
    return render(request,'profile.html')