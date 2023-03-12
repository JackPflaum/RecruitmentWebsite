from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import NewUserForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile


def register_user(request):
    """register new users to the website using NewUserForm and built-in auth login"""
    if request.method =='POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()    # save form information under user variable
            login(request, user)    # user is logged in
            messages.success(request, 'Registration Successful.')
            return redirect('home')
        
        else:
            messages.error(request, 'Unsuccessful registration. Invalid Information.')

    form = NewUserForm()
    return render(request, 'registration/register.html', {'register_form':form})


def login_user(request):
    """user login using built-in AuthentificationForm, authenticate and login functions"""

    # url value to redirect user back to the original page they were just trying to login from
    redirect_to = request.POST.get('next')

    if request.method =='POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and redirect_to == "":
                # redirects to default page
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('home')
            
            elif user is not None and redirect_to != "":
                # redirects to previous page
                login(request, user)
                messages.info(request, f'You are now logged in {username}')
                return redirect(redirect_to)
            
            else:
                messages.error(request, 'Invalid username or password.')
                
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'login_form': form})


def logout_user(request):
    """logs user out and redirect back to home page"""
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')


@login_required(login_url='login')    #limits access to logged in users only
def user_profile(request, id):
    """shows the current users profile"""
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile.objects.create(user=request.user)
        missing_profile.save()
        
    profile = Profile.objects.get(id=id)
    context = {'profile': profile}
    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
def update_profile(request):
    """allow user to update their profile"""
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)

        if form.is_valid():
            form.save()
        return redirect('user_profile', user.id)
    
    else:
        form = UserProfileForm()

    return render(request, 'update_user_profile.html', {'profile_form': form })