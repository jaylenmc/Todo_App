from rest_framework import serializers
from tasks.models import AppUser
from tasks.models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'

class taskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)