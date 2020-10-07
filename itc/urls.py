from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('app.urls')),

    path('admin/clearcache/', include('clearcache.urls')),

    path('rest/', include(('api.urls', 'api'), namespace="api")),

    path('token/', views.TokenObtainPairView.as_view(), name="token_obtain_pair"),

    path('token/refresh/', views.TokenRefreshView.as_view(), name="token_refresh"),
    
    path('auth/', include(('rest_framework.urls', 'rest_framework'), namespace="rest_framework")),
]
