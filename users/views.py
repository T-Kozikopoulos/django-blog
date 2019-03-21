from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New account created: {username}.')
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')

    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES,
                                                instance=request.user.profile)
        if update_form.is_valid() and profile_update_form.is_valid():
            update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your account has been successfully updated.')
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'update_form': update_form,
        'profile_update_form': profile_update_form
    }
    return render(request, 'users/profile.html', context)


@login_required()
def remove_user(request):
    user = request.user
    user.is_active = False
    user.save()
    messages.success(request, 'Profile successfully disabled.')
    return redirect('blog_index')
