from django.contrib.auth import views as auth_views
from account import views as acc_views
from django.urls import path
from . import views

# password reset config
pr = ["user/reset-password/", "app/passwordReset.html", "password_reset"]
# password reset done config
prd = ["user/reset-password/done/", "app/passwordResetDone.html", "password_reset_done"]
# password reset complete config
prcl = ["user/reset-password/complete/", "app/passwordResetComplete.html", "password_reset_complete"]
# password reset comfirm
prc = ["user/reset-password/confirm/<uidb64>/<token>/", "app/passwordResetConfirm.html", "password_reset_confirm"]

urlpatterns = [
    path('home', views.home, name="home"),
    path('', acc_views.loginView, name="login"),
    path('register/', acc_views.register, name="register"),
    path('join-class', views.enterCodeView, name="join_class"),
    path('logout', acc_views.LogoutView.as_view(), name="logout"),
    path('create-class', views.createClassView, name="create_class"),
    path('teacher-register', acc_views.teacherRegisterView, name="teacher_register"),
    path('student-register', acc_views.studentRegisterView, name="student_register"),
    path('class-detail/<int:pk>/',views.ClassDetailView.as_view(), name="class_detail"),
    path('update-user/<int:pk>/', acc_views.UpdateUserView.as_view(), name="update_user"), 
    path('leaveform-detail/<int:pk>/', views.LeaveFormUpdate.as_view(), name="leaveform_detail"),
    path('attendance-detail/<int:pk>/', views.AttendanceFormUpdate.as_view(), name="attendance_detail"),

    # Password reset route
    path(pr[0], auth_views.PasswordResetView.as_view(template_name=pr[1]), name=pr[2]),
    path(prd[0], auth_views.PasswordResetDoneView.as_view(template_name=prd[1]), name=prd[2]),
    path(prc[0], auth_views.PasswordResetConfirmView.as_view(template_name=prc[1]), name=prc[2]),
    path(prcl[0], auth_views.PasswordResetCompleteView.as_view(template_name=prcl[1]), name=prcl[2]),
]
