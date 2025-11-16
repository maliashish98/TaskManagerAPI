from rest_framework import serializers  
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id',
            'owner_id',
            'owner_username',
            'title',
            'description',
            'completed',
            'due_date',
            'priority',
            'created_at',
            'updated_at',
        ]
        read_only_fields=['owner_id', 'owner_username', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username',  'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            if password:
                instance.set_password(password)
            instance.save()
            return instance
