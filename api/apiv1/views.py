from django.shortcuts import render
from rest_framework import generics, serializers
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse
from logzero import logger
import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class RaceSetListAPIView(generics.ListCreateAPIView):
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

    date_for_week_filter = openapi.Parameter('date_for_week_filter', openapi.IN_QUERY, description="週間検索用の日にち", type=openapi.FORMAT_DATE)
    @swagger_auto_schema(description='検索日時と同週の競走のリストを取得', manual_parameters=[date_for_week_filter])
    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)
        logger.info('date_for_week_filter={}のracesetsが照会された'.format(request.query_params.get('date_for_week_filter')))
        return response
    
    @swagger_auto_schema(description='crawl_and_pred')
    def create(self, request):
        crawl_and_pred_flag = self.request.data['crawl_and_pred_flag']
        print(crawl_and_pred_flag)
        if crawl_and_pred_flag != 1:
            raise serializers.ValidationError('crawl_and_pred_flag:1 is required')
        response = super().create(self, request)
        logger.info('racesets{}件登録しました。'.format(request.data))
        return response

class RaceListWithHorseAPIView(generics.ListAPIView):
    serializer_class = RaceSerializer
    def get_queryset(self):
        return Race.objects.filter(raceset_name=self.kwargs['pk'])