from rest_framework import viewsets, permissions
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer,UserSerializer

User = get_user_model()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user  = self.request.user
        if user and user.is_authenticated:
            return self.queryset.filter(owner = user)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        '''
        Returns task counts for the authenticated user:
        - total_tasks
        - completed_tasks
        - incomplete_tasks
        '''
        qs = self.get_queryset()
        aggregates = qs.aggregate(
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
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # allow registration
        if self.action == 'list':
            return [permissions.IsAdminUser()] # only admins can list users
        return [permissions.IsAuthenticated()] # retrieve/update/destroy require auth
        
    @action(detail=False, methods=['get','put','patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self,request):
         # GET /api/users/me/  -> profile
        if request.method == 'GET':
            return Response(self.get_serializer(request.user).data)
        serializer = self.get_serializer(request.user, data=request.data, partial=(request.method == 'PATCH'))
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
            
