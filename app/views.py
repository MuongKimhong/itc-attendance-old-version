# Built in Django Import
from django.views.generic.edit import CreateView, UpdateView, FormMixin, DeleteView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, FormView
from django.shortcuts import render
from django.urls import reverse
from django import forms
import collections
import itertools

# App Import
from .models import Department, Year, Class, LeaveForm, Attendance
from account.decorators import student_required, teacher_required
from account.models import Teacher, Student, CustomUser
from account import forms as acc_forms
from . import forms as app_forms


# Home page View
@login_required(login_url="/")
def home(request):
    template_name = "app/home.html"

    # Teacher instance
    if request.user.is_teacher:
        cForm = app_forms.ClassForm()  # ClassForm
        eForm = acc_forms.UpdateUserForm(instance=request.user)
        allClasses = Class.objects.filter(teacher=request.user).order_by('-date_created')
        context = {'eForm': eForm, 'cForm': cForm, 'allClasses': allClasses}
    # Student Instance
    elif request.user.is_student:
        student = Student.objects.get(user=request.user)
        ecForm = app_forms.EnterCodeForm()
        eForm = acc_forms.UpdateUserForm(instance=request.user)
        allClasses = Class.objects.filter(student=student).order_by('-date_created')
        context = {'eForm': eForm, 'ecForm': ecForm, 'allClasses': allClasses}
    else:
        context = {'hello': 'Hello home page'}
    return render(request, template_name, context)


# Create Class View
@teacher_required
@login_required(login_url="/")
def createClassView(request):
    if request.method == "POST":
        form = app_forms.ClassForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.teacher = request.user
            form.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return HttpResponse("Class Create View")


# Attendance Detail & Update
@method_decorator(teacher_required, name="dispatch")
class AttendanceFormUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/'
    model = Attendance
    form_class = app_forms.AttendanceForm
    template_name = "app/teacher/attendanceDetail.html"

    def get_form_kwargs(self):
        kwargs = super(AttendanceFormUpdate, self).get_form_kwargs()
        current_class = Class.objects.get(id=self.object.course.id)
        
        if self.request.user.is_teacher:
            kwargs['class_pk'] = current_class.id  # pass class id to form

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AttendanceFormUpdate, self).get_context_data(**kwargs)
        current_class = Class.objects.get(id=self.object.course.id)

        total_student = current_class.student.count()  # total student in Class
        total_absent = total_student - self.object.student.all().count()  # total student absent

        all_student_name_in_class = []  # all student names who are inside class
        all_student_name_come = []  # all student names who come to class
        all_student_name_absent = []  # all student name who are absent
        attendance = Attendance.objects.filter(course=current_class)

        # Loop through all students inside class
        for student_in_class in current_class.student.all():
            name = student_in_class.user.first_name + " " + student_in_class.user.last_name
            all_student_name_in_class.append(name)

        # Loop through all students who come to class
        for student in self.object.student.all():
            name = student.user.first_name + " " + student.user.last_name
            all_student_name_come.append(name)
            
        # loop through all students to check who is absent
        for name in all_student_name_in_class:
            if name not in all_student_name_come:
                all_student_name_absent.append(name)

        context['totalStudent'] = total_student
        context['totalAbsent'] = total_absent
        context['allStudentNameAbsent'] = all_student_name_absent

        return context

    def get_success_url(self):
        return reverse('attendance_detail', kwargs={'pk': self.object.pk})


# Class detail View
class ClassDetailView(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/'
    model = Class
    template_name = "app/teacher/classDetail.html"

    def get_form_class(self):
        if self.request.user.is_student:
            return app_forms.LeaveFormForm
        elif self.request.user.is_teacher:
            return app_forms.AttendanceForm

    def get_form_kwargs(self):
        kwargs = super(ClassDetailView, self).get_form_kwargs()

        if self.request.user.is_teacher:
            kwargs['class_pk'] = self.kwargs.get('pk')

        return kwargs
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_student:
            current_user = self.request.user
            all_leave_forms = LeaveForm.objects.filter(student=current_user, studentClass=self.object)
            context['all_leave_forms'] = all_leave_forms.order_by('-date_created')

        elif self.request.user.is_teacher:
            i = 0
            all_come_count = []  # list of student names with count of attendance
            all_student_name_come = {}  # all student names who attend to class
            all_student_name_in_class = []  # all student names in class            
            # get all attendance objects for specific class
            all_attendance_objects = Attendance.objects.filter(course=self.object).all()

            # Loop to check who are already in class
            for student_in_class in Class.objects.get(id=self.object.id).student.all():
                name = student_in_class.user.first_name + " " + student_in_class.user.last_name
                all_student_name_in_class.append(name)

            # Loop to get all student who come to class
            for object in all_attendance_objects:
                i = i + 1
                all_student_name_come['attendanceObject{}'.format(i)] = []
                for name in object.student.all():
                    fullname = name.user.first_name + " " + name.user.last_name
                    all_student_name_come['attendanceObject{}'.format(i)].append(fullname)

            # count number of come of student
            come_count = dict(collections.Counter(itertools.chain(*all_student_name_come.values())))
            come_count = dict(collections.OrderedDict(sorted(come_count.items())))
            
            for name in come_count:
                all_come_count.append("{} - {}".format(name, come_count[name]))

            context['number_of_student'] = Class.objects.get(id=self.object.pk).student.count()
            context['allLeaveForms'] = LeaveForm.objects.filter(studentClass=self.object).order_by('-date_created')
            context['allAttendances'] = Attendance.objects.filter(course=self.object).order_by('-date_created')
            context['totalComeCount'] = all_come_count
        return context
        
    def get_success_url(self):
        return reverse('class_detail', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else: 
            return JsonResponse({'error': form.errors}, status=400)

    def form_valid(self, form):
        if self.request.user.is_student:
            form.instance.student = self.request.user
            form.instance.studentClass = self.object
        elif self.request.user.is_teacher:
            form.instance.teacher = self.request.user
            form.instance.course = self.object
        form.save()
        return super().form_valid(form)


# Leave Form Detail & Update
class LeaveFormUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/'
    model = LeaveForm
    template_name = "app/student/leaveDetail.html"
    form_class = app_forms.LeaveFormForm 

    def get_success_url(self):
        return reverse('leaveform_detail', kwargs={'pk': self.object.pk})


# Enter code view
@login_required(login_url="/")
@csrf_protect
def enterCodeView(request):
    if request.method == "POST":
        form = app_forms.EnterCodeForm(request.POST)
        code = request.POST['code']
        student = Student.objects.get(user=request.user)

        if Class.objects.filter(random_code=code).exists():
            class_code = Class.objects.get(random_code=code)

            if student not in class_code.student.all():
                class_code.student.add(student)
                class_code.save()

                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': True}, status=200)
                else:
                    return JsonResponse({'error': form.errors}, status=400)
            else: 
                print("already inside")
                return JsonResponse({'errors': "You're already inside the class!"}, status=400)
        else:
            return JsonResponse({'notFound': "Class not found!"}, status=400)
    return HttpResponse("Enter Code Create View")