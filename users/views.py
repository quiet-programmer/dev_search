from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles

# Create your views here.

# this is where all the user authentication starts


def loginUser(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'user_account')
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

    subject = 'Welcome to Dev Search'
    message = 'Hi {profile.email}, We are glad you are here.'

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


# this is where all the user authentication ends


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {
        'profiles': profiles,
        'custom_range': custom_range,
        'search_query': search_query
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


@login_required(login_url='login')
def messageInbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()
    context = {
        'messageRequest': messageRequest,
        'unreadCount': unreadCount,
    }
    return render(request, 'users/user_inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }
    return render(request, 'users/view_message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, 'Your message has been sent')
            return redirect('user_profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form,
    }
    return render(request, 'users/message_form.html', context)


