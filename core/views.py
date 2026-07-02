from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MainTopic, Todo
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, MainTopicSerializer, TodoSerializer
from .utils import initialize_user_roadmap

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)

class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class MainTopicListView(generics.ListAPIView):
    serializer_class = MainTopicSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        initialize_user_roadmap(user)
        
        queryset = MainTopic.objects.filter(user=user).prefetch_related('todos')
        domain = self.request.query_params.get('domain')
        if domain:
            queryset = queryset.filter(domain__iexact=domain)
        return queryset

class TodoDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Todo.objects.filter(main_topic__user=self.request.user)