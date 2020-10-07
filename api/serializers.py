from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from account.models import CustomUser, Student, Teacher
from app import models as app_models

password_style = {'input_type': 'password'}


# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.Department
        fields = ['id', 'name', ]


# Year Serializer
class YearSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = app_models.Year
        fields = ['id', 'department', 'years']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["department"] = DepartmentSerializer(instance.department.all(), many=True).data
        return rep


# CustomUser Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style=password_style)
    confirm_password = serializers.CharField(write_only=True, required=True, style=password_style)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'is_teacher', 'is_student', 'first_name', 'last_name', 'password', 
            'confirm_password', 'gender', 'phone', 'date_of_birth', 'department',
            'years', 'teacher_type', 'student_id'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["department"] = DepartmentSerializer(instance.department.all(), many=True).data
        rep["years"] = YearSerializer(instance.years.all(), many=True).data
        return rep

    def create(self, validated_data):
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError("Password didn't match!")
        elif validated_data.get('password') == validated_data.get('confirm_password'):
            validated_data['password'] = make_password(validated_data.get('password'))

        validated_data.pop('confirm_password', None)
        user = super().create(validated_data)
        is_student = validated_data.pop("is_student", False)
        is_teacher = validated_data.pop("is_teacher", False)
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')

        if is_student is True:
            Student.objects.create(user=user, email=email, first_name=first_name)    
        elif is_teacher is True:
            Teacher.objects.create(user=user, email=email, first_name=first_name)

        return user


# Change Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser
    old_password = serializers.CharField(required=True, style=password_style)
    new_password = serializers.CharField(required=True, style=password_style)
    confirm_new_password = serializers.CharField(required=True, style=password_style)


# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'email', 'first_name']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = CustomUserSerializer(instance.user).data
        return rep


# Class Serializer
class ClassSerializer(serializers.ModelSerializer):
    teacher = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = app_models.Class
        fields = ['id', 'teacher', 'department', 'random_code', 'years', 'subject',
                  'date_created', 'student']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["department"] = DepartmentSerializer(instance.department).data
        rep["years"] = YearSerializer(instance.years).data
        rep["student"] = StudentSerializer(instance.student.all(), many=True).data
        return rep        


# Enter code serializer
class EnterCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.EnterCode
        fields = ['id', 'code']

    def create(self, validated_data):
        code = validated_data.get('code')
        user = self.context['request'].user
        print(user.is_student)
        student = Student.objects.get(user=user)
        print(student)

        if app_models.Class.objects.filter(random_code=code).exists():
            if user.is_student is True:
                class_code = app_models.Class.objects.get(random_code=code)
                if student not in class_code.student.all():
                    class_code.student.add(student)
                    class_code.save()
                elif student in class_code.student.all():
                    raise serializers.ValidationError("You're already inside the class!")

        elif not app_models.Class.objects.first(random_code=code).exists():
            raise serializers.ValidationError("Class with this code not found!")

        return super(EnterCodeSerializer, self).create(validated_data)


# Leave Form Serializer
class LeaveFormSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)

    class Meta:
        model = app_models.LeaveForm
        fields = ['student', 'studentClass', 'leaveFromDate', 'leaveTillDate', 'leaveReason',
                  'date_created']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['studentClass'] = ClassSerializer(instance.studentClass).data
        return rep


# Attendance Serializer
class AttendanceSerializer(serializers.ModelSerializer):
    teacher  =CustomUserSerializer(read_only=True)

    class Meta:
        model = app_models.Attendance
        fields = ['id', 'teacher', 'course', 'student', 'date_created']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['course'] = ClassSerializer(instance.course).data
        rep['student'] = StudentSerializer(instance.student.all(), many=True).data
        return rep