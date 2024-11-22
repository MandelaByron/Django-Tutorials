from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, message="Your Profile has been updated!")
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, template_name='profile.html', context={"title": "Profile", "form": form})