from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

from .models import Todo, MainTopic

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'subtopic_id', 'title', 'resources', 'status', 'completed', 'notes', 'github_url')
        read_only_fields = ('id', 'subtopic_id', 'title', 'resources')

    def update(self, instance, validated_data):
        completed = validated_data.get('completed', instance.completed)
        status = validated_data.get('status', instance.status)

        if 'completed' in validated_data and 'status' not in validated_data:
            validated_data['status'] = 'completed' if completed else 'todo'
        elif 'status' in validated_data and 'completed' not in validated_data:
            validated_data['completed'] = (status == 'completed')

        return super().update(instance, validated_data)


class MainTopicSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = MainTopic
        fields = ('id', 'domain', 'topic_id', 'title', 'priority', 'level', 'estimated_hours', 'note', 'todos')