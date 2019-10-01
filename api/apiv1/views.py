from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.views import APIView
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse
from logzero import logger
import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
# Create your views here.

class RaceSetListAPIView(generics.ListAPIView):
    """
    検索日時と同週の競走の**リスト**を取得
    date_for_week_filter -- 検索日時
    """
    serializer_class = RaceSetSerializer
    
    def get_same_week_range(self, date):
        req_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        dist_from_monday = req_date.weekday()
        dist_from_next_sunday = 6 - dist_from_monday
        monday_date_on_same_week = req_date - datetime.timedelta(days=dist_from_monday)
        sunday_date_on_same_week = req_date + datetime.timedelta(days=dist_from_next_sunday)
        return  monday_date_on_same_week, sunday_date_on_same_week
    
    def get_queryset(self):
        date_for_week_filter = self.request.query_params.get('date_for_week_filter')
        if date_for_week_filter is None:
            raise serializers.ValidationError('date_for_week_filter parameter is required, like 2019-06-21')
        racesets = RaceSet.objects.filter(date__range = self.get_same_week_range(date_for_week_filter))
        return racesets

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        logger.info('date_for_week_filter={}のracesetsが照会された'.format(request.query_params.get('date_for_week_filter')))
        return response

class RaceListWithHorseAPIView(generics.ListAPIView):
    serializer_class = RaceSerializer
    def get_queryset(self):
        return Race.objects.filter(raceset_name=self.kwargs['pk'])