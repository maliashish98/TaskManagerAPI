from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'completed', 'due_date', 'priority', 'created_at', 'updated_at' ]

# Register your models here.
