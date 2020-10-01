from shortuuidfield import ShortUUIDField
from django.db import models
import shortuuid
import uuid


# Department
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Year
class Year(models.Model):
    department = models.ManyToManyField(Department)
    years = models.CharField(max_length=20)

    def __str__(self):
        return self.years


# Teacher Type
class Type(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


# Class
class Class(models.Model):
    # get random code
    def code():
        return shortuuid.ShortUUID().random(length=6)

    teacher = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    random_code = ShortUUIDField(default=code, editable=False)
    years = models.ForeignKey(Year, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField("account.Student")
    
    def __str__(self):
        return self.subject


# Enter Code
class EnterCode(models.Model):
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('home')


# Attendance
class Attendance(models.Model):
    teacher = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField("account.Student")
    
    def __str__(self):
        return self.course


# Leave Form
class LeaveForm(models.Model):
    student = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    studentClass = models.ForeignKey(Class, on_delete=models.CASCADE, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    leaveFromDate = models.DateField()
    leaveTillDate = models.DateField()
    leaveReason = models.TextField()
    
    def __str__(self):
        return self.student.first_name