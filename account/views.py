from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import CustomUser, Teacher, Student
from .forms import TeacherRegisterForm, StudentRegisterForm, LoginForm, EditUserForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.generic.edit import UpdateView
from django.contrib import messages
import json

# login
@csrf_protect
def loginView(request):
    template_name = "app/login.html"
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        # else: 
        #     return JsonResponse({'error': form.errors}, status=400)
    return render(request, template_name, {'form': form})

# logout
class LogoutView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        logout(request)
        return redirect('/')

@csrf_protect
def register(request):
    form = TeacherRegisterForm()
    sForm = StudentRegisterForm()
    lForm = LoginForm()
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "app/register.html", {'form': form, 'sForm': sForm, 'lForm': lForm})

# Teacher register view
@csrf_protect
def teacherRegisterView(request):
    if request.method == "POST":
        form = TeacherRegisterForm(request.POST)
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
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return HttpResponse('Student Register')

@login_required(login_url='/')
@csrf_protect
def editUserInfoView(request):
    if request.method == "POST":
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
        else:
            return JsonResponse({'error': edit_form.errors}, status=400)
    return HttpResponse("Edit User Form")


class UpdateUserView(LoginRequiredMixin, UpdateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateUserView, self).dispatch(request, *args, **kwargs)
    
    login_url = '/'
    model = CustomUser
    form_class = UpdateUserForm
    success_url = '/home'

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