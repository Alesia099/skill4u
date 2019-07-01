from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import (TaskSerializer, TeamSerializer, OlympiadSerializer)
from .models import (Task, Team, Olympiad)


class TaskAPI(APIView):
    """Olympiad task"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

    def post(self, request):
        task = request.data.get("task")
        input_data = request.data.get("input_data")
        answer = request.data.get("answer")

        if not task or not input_data or not answer:
            return Response({'error': 'Enter all fields.'},
                            status=400)
        else:
            Task.objects.create(creater=request.user, task=task, input_data=input_data, answer=answer)
            return Response(status=201)


class TeamAPI(APIView):
    """Return teams list"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        team = Team.objects.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    def post(self, request):
        olympiad_id = request.data.get("olympiad_id")
        invited = request.data.get("invited")
        olympiad = Olympiad.objects.get(id=olympiad_id)
        max_participations = request.data.get("max_participations")

        if not olympiad_id:
            return Response({'error': 'Olympiad is absent.'},
                            status=400)
        else:
            Team.objects.create(capitan=request.user, max_participations=max_participations)
            team = Team.objects.get(capitan=request.user)
            olympiad.team.add(team)
            return Response(status=201)
    

class OlympiadAPI(APIView):
    """Return Olympiad list"""
    def get(self, request):
        olympiad = Olympiad.objects.all()
        serializer = OlympiadSerializer(olympiad, many=True)
        return Response(serializer.data)