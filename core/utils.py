import os
import json
from django.conf import settings
from .models import MainTopic, Todo

def initialize_user_roadmap(user):
    if MainTopic.objects.filter(user=user).exists():
        return

    json_dir = os.path.join(settings.BASE_DIR, 'json')
    if not os.path.exists(json_dir):
        return

    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(json_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                domain_name = data.get('domain', filename.replace('.json', '').title())

                for topic_data in data.get('topics', []):
                    main_topic, created = MainTopic.objects.get_or_create(
                        user=user,
                        topic_id=topic_data.get('id'),
                        defaults={
                            'domain': domain_name,
                            'title': topic_data.get('title', ''),
                            'priority': topic_data.get('priority'),
                            'level': topic_data.get('level'),
                            'estimated_hours': topic_data.get('estimated_hours'),
                            'note': topic_data.get('note')
                        }
                    )

                    for subtopic_data in topic_data.get('subtopics', []):
                        Todo.objects.get_or_create(
                            main_topic=main_topic,
                            subtopic_id=subtopic_data.get('id'),
                            defaults={
                                'title': subtopic_data.get('title', ''),
                                'resources': subtopic_data.get('resources', []),
                                'status': subtopic_data.get('status', 'todo'),
                                'completed': subtopic_data.get('status') == 'completed'
                            }
                        )
            except Exception as e:
                pass
