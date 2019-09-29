from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse
import datetime
# Create your views here.

class RaceSetListAPIView(generics.ListAPIView):
    serializer_class = RaceSetSerializer
    
    def get_same_week_range(self, date):
        req_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        dist_from_monday = req_date.weekday()
        dist_from_next_sunday = 6 - dist_from_monday
        monday_date_on_same_week = req_date - datetime.timedelta(days=dist_from_monday)
        sunday_date_on_same_week = req_date + datetime.timedelta(days=dist_from_next_sunday)
        return  monday_date_on_same_week, sunday_date_on_same_week
    
    def get_queryset(self):
        req_date = self.request.GET.get('date_for_week_filter')
        racesets = RaceSet.objects.filter(date__range = self.get_same_week_range(req_date))
        return racesets

class RaceListWithHorseAPIView(generics.ListAPIView):
    serializer_class = RaceSerializer
    def get_queryset(self):
        return Race.objects.filter(raceset_name=self.kwargs['pk'])