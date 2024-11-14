from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import UserUpdateForm



@login_required
def profile_view(request):
    
    if request.method == 'POST':
        
        form = UserUpdateForm(request.POST, request.FILES , instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request,template_name='profile.html',context={'title': 'Profile', 'form': form})