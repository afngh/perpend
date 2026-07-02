from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, UserMeView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/me/', UserMeView.as_view(), name='auth_me'),
]

