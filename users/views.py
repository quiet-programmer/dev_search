from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

from .models import Profile
from projects.models import Project

# Create your views here.

def loginUser(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password is incorrect.')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)



def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles,
    }
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    # all_projects = Project.objects.get(id=pk)
    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
        # 'all_projects': all_projects,
    }
    return render(request, 'users/user_profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    context = {
        'profile': profile,
        'skills': skills,
    }
    return render(request, 'users/user_account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user_account')
    context = {
        'form': form,
    }
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def addSkills(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skills has been added')
            return redirect('user_account')

    context = {
        'form': form,
    }
    return render(request, 'users/skills_form.html', context)

@login_required(login_url='login')
def updateSkills(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, 'Skills has been updated')
            return redirect('user_account')

    context = {
        'form': form
    }
    return render(request, 'users/skills_form.html', context)

@login_required(login_url='login')
def deleteSkills(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.info(request, 'Skills has been deleted')
        return redirect('user_account')
    context = {
        'object': skill,
    }
    return render(request, 'delete_template.html', context)


