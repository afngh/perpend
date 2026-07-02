from django.contrib import admin
from .models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic_id', 'subtopic', 'completed')
    list_filter = ('completed', 'topic_id')
    search_fields = ('user__username', 'subtopic')
