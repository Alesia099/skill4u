from rest_framework import serializers
from .models import Task, Team, Olympiad
from registration.serializer import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ('task', 'input_data')


class TeamSerializer(serializers.ModelSerializer):
    capitan = UserSerializer()
    invited = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = ('id', 'capitan', 'invited', 'max_participations')


class OlympiadSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)

    class Meta:
        model = Olympiad
        fields = ('id', 'team', 'name', 'participation_count')