from django.conf import settings
from django.db import models

# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = (
                        (1,"Low"),
                        (2,"Medium"),
                        (3,"High")
                        )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True,blank=True)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"