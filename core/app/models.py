from django.db import models
from django.contrib.auth.models import User


class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    topic_id = models.IntegerField()
    subtopic = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'topic_id', 'subtopic')

    def __str__(self):
        status = '✓' if self.completed else '○'
        return f"{status} [{self.topic_id}] {self.subtopic} ({self.user.username})"
