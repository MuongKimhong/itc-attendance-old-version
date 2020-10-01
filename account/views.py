# Django Import
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core import serializers
from django.contrib import messages
# App account import
from . import forms, models


# login
@csrf_protect
def loginView(request):
    template_name = "app/login.html"
    form = forms.LoginForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

    return render(request, template_name, {'form': form})


# Main Register View
@csrf_protect
def register(request):
    form = forms.TeacherRegisterForm()
    sForm = forms.StudentRegisterForm()
    lForm = forms.LoginForm()

    context = {'form': form, 'sForm': sForm, 'lForm': lForm}

    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, "app/register.html", context)


# Teacher register view
@csrf_protect
def teacherRegisterView(request):
    if request.method == "POST":
        form = forms.TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return HttpResponse('Teacher Register')


# Student register view
@csrf_protect
def studentRegisterView(request):
    if request.method == "POST":
        form = forms.StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return HttpResponse('Student Register')


# Update User info view
class UpdateUserView(LoginRequiredMixin, UpdateView):
    # csrf 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateUserView, self).dispatch(request, *args, **kwargs)
    
    login_url = '/'
    success_url = '/home'
    model = models.CustomUser
    form_class = forms.UpdateUserForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return JsonResponse({'error': form.errors}, status=400)
        
    def form_valid(self, form):
        form.instance = self.request.user
        form.save()
        return super().form_valid(form)


# logout
class LogoutView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        logout(request)
        return redirect('/')