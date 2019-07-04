from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import (TaskSerializer, TeamSerializer, OlympiadSerializer)
from .models import (Task, Team, Olympiad)
from registration.models import User


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
        max_participations = request.data.get("max_participations")
        olympiad = Olympiad.objects.get(id=olympiad_id)

        if not olympiad_id:
            return Response({'error': 'Olympiad is absent.'},
                            status=400)
        else:
            Team.objects.create(capitan=request.user, max_participations=max_participations)
            team = Team.objects.get(capitan=request.user)
            olympiad.team.add(team)
            return Response(status=201)
    

class InviteToTeam(APIView):
    """"Invite user to Team"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        team = Team.objects.filter(capitan=user)
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    def post(self, request):
        team_id = request.data.get("team_id")
        invited_id = request.data.get("invited_id")
        
        
        if not team_id or not invited_id:
            return Response({'error': 'Enter all fields.'},
                            status=400)
        else:
            team = Team.objects.get(id=team_id)
            user = User.objects.get(id=invited_id)
            
            if not team or not user: 
                return Response(status=400)
            else:
                team.invited.add(user)
                return Response(status=201)
            


class OlympiadAPI(APIView):
    """Return Olympiad list"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        olympiad = Olympiad.objects.all()
        serializer = OlympiadSerializer(olympiad, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        name = request.data.get("name")
        creater = request.user
        duration = request.data.get("duration")
        start_olympiad = request.data.get("start_olympiad")
        end_olympiad = request.data.get("end_olympiad")
        participation_count = request.data.get("participation_count")
        max_teams = request.data.get("max_teams")

        if not name or not creater or not duration or not start_olympiad or not end_olympiad or not participation_count or not max_teams:
            return Response({"error":"Enter all fields."})
        else:
            Olympiad.objects.create(name=name, 
                                    creater=creater,
                                    duration=duration, 
                                    start_olympiad=start_olympiad, 
                                    end_olympiad=end_olympiad, 
                                    participation_count=participation_count, 
                                    max_teams=max_teams
                                   )
            return Response(status=201)

