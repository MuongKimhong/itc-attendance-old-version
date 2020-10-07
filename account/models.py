from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models


# User Manager
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password.
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


teacher_type_choice = (('Full Time', _('Full Time')), ('Part Time', _('Part Time')))
gender_choice = (('Male', _('Male')), ('Female', _('Female')))

# CustomUser
class CustomUser(AbstractUser):
    username = None
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    # For both student and teacher
    email = models.EmailField(_('Email Address'), unique=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choice, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    department = models.ManyToManyField("app.Department", blank=True)
    years = models.ManyToManyField("app.Year", blank=True)
    # For Teacher
    teacher_type = models.CharField(max_length=50, choices=teacher_type_choice, blank=True)
    # For student
    student_id = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Teacher
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email


# Student
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)

    def __str__(self):
        name = self.user.first_name + "  " + self.user.last_name
        return name

    class Meta:
        ordering = ('first_name',)