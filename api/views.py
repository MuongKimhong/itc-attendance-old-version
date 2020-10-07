from rest_framework import generics, viewsets, permissions, status, views
from rest_framework.response import Response

from . import serializers, permissions as api_permissions
from account import models
from app import models as app_models


# Custom user viewset
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer

    permission_classes_by_action = {
        'create': [permissions.AllowAny],
        'list': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
        'retrieve': [api_permissions.OwnProfilePermission, permissions.IsAuthenticated],
        'update': [api_permissions.OwnProfilePermission, permissions.IsAuthenticated],
        'partial_update': [api_permissions.OwnProfilePermission, permissions.IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).partial_update(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            #     # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


# Change password viewset
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    model = models.CustomUser
    permission_classes = [
        api_permissions.OwnProfilePermission,
        permissions.IsAuthenticated
    ]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        pass_not_match = {"comfirm_new_password": ["New passwords didn't match!"]}

        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong Password!"]}, status=status.HTTP_400_BAD_REQUEST)
            # compare new password and confirm new password
            elif serializer.data.get("new_password") != serializer.data.get("confirm_new_password"):
                return Response(pass_not_match, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': "Password updated successfully",
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = app_models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [permissions.AllowAny,]


class YearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = app_models.Year.objects.all()
    serializer_class = serializers.YearSerializer
    permission_classes = [permissions.AllowAny,] 


class StudentViewSet(generics.RetrieveAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated,]


class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassSerializer

    def get_queryset(self):
        if self.request.user.is_teacher:
            classes = app_models.Class.objects.all().filter(teacher=self.request.user)
            return classes
        elif self.request.user.is_student:
            student = models.Student.objects.get(user=self.request.user)
            classes = app_models.Class.objects.all().filter(student=student).order_by('-date_created')
            return classes

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'list': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated, api_permissions.OwnClassPermission],
        'retrieve': [api_permissions.OwnClassPermission, permissions.IsAuthenticated],
        'update': [api_permissions.OwnClassPermission, permissions.IsAuthenticated],
        'partial_update': [api_permissions.OwnClassPermission, permissions.IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        return super(ClassViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(ClassViewSet, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ClassViewSet, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(ClassViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(ClassViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(ClassViewSet, self).partial_update(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            #     # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class EnterCodeViewSet(viewsets.ModelViewSet):
    queryset = app_models.EnterCode.objects.all()
    serializer_class = serializers.EnterCodeSerializer
    permission_classes = [permissions.IsAuthenticated,]


class LeaveFormViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LeaveFormSerializer

    def get_queryset(self):
        if self.request.user.is_teacher:
            print(self.kwargs.get('class_pk'))
            leave_forms = app_models.LeaveForm.objects.all().filter(studentClass=self.kwargs.get('class_pk'))
        elif self.request.user.is_student:
            leave_forms = app_models.LeaveForm.objects.all().filter(student=self.request.user, studentClass=self.kwargs.get('class_pk'))
        return leave_forms

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'list': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated, api_permissions.OwnLeaveFormPermission],
        'retrieve': [api_permissions.OwnLeaveFormPermission, permissions.IsAuthenticated],
        'update': [api_permissions.OwnLeaveFormPermission, permissions.IsAuthenticated],
        'partial_update': [api_permissions.OwnLeaveFormPermission, permissions.IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        return super(LeaveFormViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(LeaveFormViewSet, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(LeaveFormViewSet, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(LeaveFormViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(LeaveFormViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(LeaveFormViewSet, self).partial_update(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            #     # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        all_attendances = app_models.Attendance.objects.all()
        current_class = self.kwargs.get('class_pk')
        attendances = all_attendances.filter(teacher=user, course=current_class)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated, api_permissions.AttendancePermission],
        'list': [permissions.IsAuthenticated, api_permissions.AttendancePermission],
        'destroy': [
            permissions.IsAuthenticated, api_permissions.OwnAttendancePermission,
            api_permissions.AttendancePermission
        ],
        'retrieve': [
            api_permissions.OwnAttendancePermission, api_permissions.AttendancePermission, 
            permissions.IsAuthenticated
        ],
        'update': [
            api_permissions.OwnAttendancePermission, api_permissions.AttendancePermission, 
            permissions.IsAuthenticated
        ],
        'partial_update': [
            api_permissions.OwnAttendancePermission, api_permissions.AttendancePermission, 
            permissions.IsAuthenticated
        ]
    }

    def create(self, request, *args, **kwargs):
        return super(AttendanceViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(AttendanceViewSet, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(AttendanceViewSet, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(AttendanceViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(AttendanceViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(AttendanceViewSet, self).partial_update(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            #     # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]