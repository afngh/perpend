import json
import os
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import TodoItem

DATA_FILE = os.path.join(settings.BASE_DIR, 'data.json')

def load_roadmap():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_roadmap(request):
    data = load_roadmap()
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed(request):
    todos = TodoItem.objects.filter(user=request.user, completed=True)
    result = [
        {'topic_id': t.topic_id, 'subtopic': t.subtopic}
        for t in todos
    ]
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_todo(request):
    topic_id = request.data.get('topic_id')
    subtopic = request.data.get('subtopic')

    if topic_id is None or not subtopic:
        return Response(
            {'error': 'topic_id and subtopic are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    todo, created = TodoItem.objects.get_or_create(
        user=request.user,
        topic_id=topic_id,
        subtopic=subtopic,
        defaults={'completed': True}
    )

    if not created:
        todo.completed = not todo.completed
        todo.save()

    return Response({
        'topic_id': todo.topic_id,
        'subtopic': todo.subtopic,
        'completed': todo.completed
    })
