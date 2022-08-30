from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from typing import List
# Create your views here.


class LoginView(LoginView):
    authentication_form = forms.LoginForm
    redirect_authenticated_user: bool = True
    template_name: str = "user/login.html"
    context_object_name = "form"


class LogoutView(LogoutView):
    None


@login_required
def userLoad(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'user/user.html', context)


@login_required
def userCreate(request):
    form = forms.UserForms()
    context = {'form': form,
               'width': 500}
    if request.method == "POST":
        form = forms.UserForms(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.password = make_password(request.POST.get("password"))
            form.save()
            return redirect('user')

    return render(request, 'form.html', context)


@login_required
def userUpdate(request, pk):
    user = User.objects.get(id=int(pk))
    form = forms.UserChangeForm(instance=user)
    context = {'form': form}
    if request.method == "POST":
        form = forms.UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user')

    return render(request, 'user/userform.html', context)


@login_required
def userDelete(request, pk):

    user = User.objects.get(id=int(pk))
    context = {'item': user}
    if request.user != user:
        if request.method == "POST":
            user.delete()
            return redirect('user')
        return render(request, 'delete.html', context)

    return redirect('user')


@login_required
def profileUpdate(request):
    user = User.objects.get(id=int(request.user.id))
    form = forms.UserProfileForm(instance=user)
    context = {'form': form}
    if request.method == "POST":
        form = forms.UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile updated succesfully!")

            return redirect('profile')

    return render(request, 'user/userform.html', context)


@login_required
def userActivity(request):
    activity = LogEntry.objects.all()
    print(activity)

    return render(request, 'user/activity.html', {})
