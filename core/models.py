from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class MainTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_topics')
    domain = models.CharField(max_length=100)
    topic_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    estimated_hours = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'topic_id')

    def __str__(self):
        return f"{self.domain} - {self.title} ({self.user.username})"

class Todo(models.Model):
    main_topic = models.ForeignKey(MainTopic, on_delete=models.CASCADE, related_name='todos')
    subtopic_id = models.CharField(max_length=100)
    title = models.TextField()
    resources = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, default='todo')
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    github_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ('main_topic', 'subtopic_id')

    def __str__(self):
        return f"{self.subtopic_id} - {self.title[:50]}"
