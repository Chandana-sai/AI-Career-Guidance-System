from django.db import models
from students.models import StudentProfile

class ChatConversation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="chat_sessions")
    session_key = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_str = self.student.user.username if self.student else f"Anon ({self.session_key[:8]})"
        return f"Chat Session: {user_str} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ("user", "User"),
        ("bot", "AI Career Advisor"),
    ]
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    suggested_chips = models.JSONField(default=list, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"[{self.sender}] {self.message[:50]}..."
