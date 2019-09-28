from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse

# Create your views here.
class RaceSetListAPIView(generics.ListAPIView):
    queryset = RaceSet.objects.all()
    serializer_class = RaceSetSerializer

    # TODO ↓完成まで
    def get_same_week_range(self, date):
        req_date = date.today()
        dist_from_sunday = 6 - req_date.weekday()
        monday_date_on_same_week = req_date
        sunday_date_on_same_week = req_date
        return  monday_date_on_same_week, sunday_date_on_same_week


class RaceListWithHorseAPIView(generics.ListAPIView):
    serializer_class = RaceSerializer
    def get_queryset(self):
        return Race.objects.filter(raceset_name=self.kwargs['pk'])