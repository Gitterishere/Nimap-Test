from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

    def create(self, validated_data):
        # Extract users from validated_data
        users_data = self.initial_data.get('users')
        client_id = self.initial_data.get('client_id')
        
        
        project = Project.objects.create(
            project_name=validated_data['project_name'],
            client_id=client_id,
            created_by=self.context['request'].user
        )

        
        if users_data:
            project.users.set(User.objects.filter(id__in=users_data))
        
        return project

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']


class CreateProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_by']
