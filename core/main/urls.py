from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.views import get_roadmap, get_completed, toggle_todo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/roadmap/', get_roadmap, name='roadmap'),
    path('api/todos/completed/', get_completed, name='todos_completed'),
    path('api/todos/toggle/', toggle_todo, name='todos_toggle'),
]
