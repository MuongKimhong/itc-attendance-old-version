# Rest Framework Import
from rest_framework_nested import routers as nested_routers
from rest_framework import routers
# Django Import
from django.urls import path, include
# API Import
from . import views

# Rest Framework Router
router = routers.DefaultRouter()
router.register('years', views.YearViewSet, basename="years")
router.register('codes', views.EnterCodeViewSet, basename="codes")
router.register('users', views.CustomUserViewSet, basename="users")
router.register('departments', views.DepartmentViewSet, basename="departments")

# Nested Router
nested_router = nested_routers.SimpleRouter()
nested_router.register('classes', views.ClassViewSet, basename="classes")

classes_router = nested_routers.NestedSimpleRouter(nested_router, 'classes', lookup="class")
classes_router.register("leaveforms", views.LeaveFormViewSet, basename="leaveforms")
classes_router.register("attendances", views.AttendanceViewSet, basename="attendances")

urlpatterns = [
    path('api/', include(router.urls)),
    path('change-password', views.ChangePasswordView.as_view(), name="change_password"),
    path('student/<int:pk>/', views.StudentViewSet.as_view(), name="student"),
    # nested router for classes and leaveforms
    # route config 8000/rest/classes/1/leaveforms
    path('', include(nested_router.urls)),
    path('', include(classes_router.urls)),
]
