from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

class HomePageView(TemplateView):
    template_name = "index.html"
    
def change_password(request):
    if request.method =='POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form .is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!  you have been logged in with new password')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('changepassword')

    else:
        form = PasswordChangeForm(user=request.user)
        return render(request,'core/change_password.html',{'form':form})