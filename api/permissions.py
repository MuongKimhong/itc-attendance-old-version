from rest_framework import permissions


class OwnProfilePermission(permissions.BasePermission):
    # Object-level permission to only allow updating his own profile

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == permissions.SAFE_METHODS:
            return True
        # obj here is a UserProfile instance
        return obj == request.user


class OwnClassPermission(permissions.BasePermission):
    # Object-level permission to only allow updating his own profile
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return obj.teacher == request.user


class OwnLeaveFormPermission(permissions.BasePermission):
    # Object-level permission to only allow updating his own profile
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return obj.student == request.user


class AttendancePermission(permissions.BasePermission):
    # Object-level permission to only allow updating his own profile
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return obj == request.user.is_teacher


class OwnAttendancePermission(permissions.BasePermission):
    # Object-level permission to only allow updating his own profile
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return obj == request.user
