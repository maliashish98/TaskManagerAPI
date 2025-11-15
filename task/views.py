from rest_framework import viewsets
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=["get"])
    def stats(self, request):
        '''
        Returns task counts for the authenticated user:
        - total_tasks
        - completed_tasks
        - incomplete_tasks
        '''
        aggregates = self.queryset.aggregate(
            total_tasks = Count('id'),
            completed_tasks = Count('id', filter=Q(completed=True)),
            incompleted_tasks = Count('id',filter=Q(completed=False)),
        )

        total_tasks = aggregates.get("total_tasks") or 0
        completed_tasks = aggregates.get("completed_tasks") or 0
        incompleted_tasks = aggregates.get("incompleted_tasks") or 0

        return Response(
            {
                "total_tasks" : total_tasks,
                "completed_task" : completed_tasks,
                "incompleted_task": incompleted_tasks
            })


