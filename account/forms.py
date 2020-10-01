from .models import CustomUser, Teacher, Student
from django.contrib.auth import authenticate
from app.models import Department
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from rest_framework.authtoken.models import Token

# Form Attribute
first_name_attr = {'type': 'text', 'id': 'first_name', 'class': 'form-control'}
last_name_attr = {'type': 'text', 'id': 'last_name', 'class': 'form-control'}
student_id_attr = {'id': 'student_id', 'class': 'form-control', 'type': 'text'}
password1_attr = {'type': 'password','id': 'password1', 'class': 'form-control'}
password2_attr = {'type': 'password','id': 'password2', 'class': 'form-control'}
date_attr = {'class': 'form-control', 'type': 'date', 'id': 'date_of_birth'}
email_attr = {'type': 'email', 'id': 'email', 'class': 'form-control'}
phone_attr = {'type': 'text', 'id': 'phone', 'class': 'form-control'}
teacher_type_attr = {'id': 'teacher_type', 'class': 'form-control'}
gender_attr = {'id': 'gender', 'class': 'form-control'}

attr = [
    first_name_attr, last_name_attr, password1_attr, password2_attr, email_attr,
    gender_attr, phone_attr, date_attr,  teacher_type_attr, student_id_attr,
]

# Teacher Register
class TeacherRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['first_name', 'last_name', 'password1', 'password2', 'email', 'gender', 'phone',
                  'date_of_birth', 'teacher_type']
        widgets = {'date_of_birth': forms.DateInput(date_attr)}

    def __init__(self, *args, **kwargs):
        super(TeacherRegisterForm, self).__init__(*args, **kwargs)
        i = 0

        for field in self._meta.fields:
            if i <= 8:
                self.fields[field].required = True
                self.fields[field].widget.attrs.update(attr[i])
                i = i + 1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        email = str(self.cleaned_data.get('email'))
        first_name = str(self.cleaned_data.get('first_name'))
        teacher = Teacher.objects.create(user=user, email=email, first_name=first_name)
        return (user, teacher)


# Student Register
class StudentRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['first_name', 'last_name', 'password1', 'password2', 'email', 'gender', 'phone',
                  'date_of_birth', 'student_id']
        widgets = {'date_of_birth': forms.DateInput(date_attr)}

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        i = 0

        for field in self._meta.fields:
            if field == "student_id":
                self.fields[field].required = True
                self.fields[field].widget.attrs.update(attr[9])
                break
            else:
                self.fields[field].required = True
                self.fields[field].widget.attrs.update(attr[i])
                i = i + 1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        email = str(self.cleaned_data.get('email'))
        first_name = str(self.cleaned_data.get('first_name'))
        student = Student.objects.create(user=user, email=email, first_name=first_name)
        return (user, student)


# login form
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs=email_attr))
    password = forms.CharField(widget=forms.PasswordInput(attrs=password1_attr))
    
    class Meta:
        fields = ['email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True

    def clean(self, *args, **kwargs):
        cleaned_data = super(LoginForm, self).clean(*args, **kwargs)
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            err_message = "Email or Password is incorrect!"
            raise forms.ValidationError({'email': err_message, 'password': err_message})
        return cleaned_data


# Edit user form
class EditUserForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'gender', 'phone',
            'date_of_birth', 'department', 'years', 'teacher_type',
            'student_id'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(date_attr),
            'department': forms.CheckboxSelectMultiple({'class': 'edit-user-department'}),
            'years': forms.CheckboxSelectMultiple({'class': 'edit-user-years'})
        }

        def __init__(self, *args, **kwargs):
            super(EditUserForm, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs.update(email_attr)
            self.fields['first_name'].widget.attrs.update(first_name_attr)
            self.fields['last_name'].widget.attrs.update(last_name_attr)
            self.fields['gender'].widget.attrs.update({'class': 'form-control', 'id': 'gender-update'})
            self.fields['phone'].widget.attrs.update(phone_attr)
            self.fields['teacher_type'].widget.attrs.update({'class': 'form-control'})
            self.fields['student_id'].widget.attrs.update(student_id_attr)

        def save(self, commit=True):
            user = super().save(commit=False)
            email = str(self.cleaned_data.get('email'))
            first_name = str(self.cleaned_date.get('first_name'))
            if user.is_teacher:
                teacher = Teacher.objects.filter(user=user)
                teacher.update(email=email, first_name=first_name,) 
                user.save()
                return (user, teacher)
            elif user.is_student:
                student = Student.objects.filter(user=user)
                student.update(email=email, first_name=first_name)   
                user.save()
                return (user, student)


# Update user info Form
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone','teacher_type', 'student_id', 
                  'date_of_birth', 'department', 'years']
        widgets = {
            'date_of_birth': forms.DateInput(date_attr),
            'department': forms.CheckboxSelectMultiple({'class': 'edit-user-department'}),
            'years': forms.CheckboxSelectMultiple({'class': 'edit-user-years'})
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        attr = {'class': 'form-control', 'id': ''}
        fAttr = ['eu', 'fu', 'lu', 'gu', 'pu', 'tu', 'su']
        i = 0

        for field in self._meta.fields:
            if field == "date_of_birth" or field == "department" or field == "years":
                break
            else:
                attr['id'] = fAttr[i]
                self.fields[field].widget.attrs.update(attr)
                i = i + 1

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if self.instance.is_student:
            if len(department) > 1:
                raise forms.ValidationError("You can't select more than one department!")
            return department
        elif self.instance.is_teacher:
            return department

    def clean_years(self):
        years = self.cleaned_data.get('years')
        if self.instance.is_student:
            if len(years) > 1:
                raise forms.ValidationError("You can't select more than one year!")
            return years
        elif self.instance.is_teacher:
            return years