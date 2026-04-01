from django.db import models
from django.contrib.auth.models import User

class TopicSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searches')
    topic_name = models.CharField(max_length=255)
    study_material = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic_name} - {self.user.username}"

class MCQ(models.Model):
    topic = models.ForeignKey(TopicSearch, on_delete=models.CASCADE, related_name='mcqs')
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField()

    def __str__(self):
        return self.question[:50]

class UserAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    topic = models.ForeignKey(TopicSearch, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic.topic_name} - {self.score}/{self.total_questions}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    topic = models.ForeignKey(TopicSearch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.topic.topic_name}"
