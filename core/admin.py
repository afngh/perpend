from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MainTopic, Todo

admin.site.register(User, UserAdmin)

@admin.register(MainTopic)
class MainTopicAdmin(admin.ModelAdmin):
    list_display = ('domain', 'topic_id', 'title', 'user', 'priority')
    list_filter = ('domain', 'priority', 'level', 'user')
    search_fields = ('title', 'topic_id', 'domain', 'note')

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('subtopic_id', 'title', 'main_topic', 'status', 'completed')
    list_filter = ('status', 'completed', 'main_topic__domain', 'main_topic__user')
    search_fields = ('title', 'subtopic_id', 'notes', 'github_url')
