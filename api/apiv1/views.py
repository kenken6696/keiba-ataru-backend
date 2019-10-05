from django.shortcuts import render
from rest_framework import generics, serializers
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse
from logzero import logger
import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import SwaggerAutoSchema

class RaceSetListAPIView(generics.ListCreateAPIView):
    """
    racesetsを操作する
    
    get:
    date_for_week_filterと同週のracesets(競争名)のリストを取得する
    
    post:
    crawl_and_pred_flagが1の場合、今週のracesets以下を取得し、モデルより予測した結果をDB保存する
    """
    serializer_class = RaceSetSerializer
    swagger_schema = SwaggerAutoSchema
    
    def get_same_week_range(self, date):
        req_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        dist_from_monday = req_date.weekday()
        dist_from_next_sunday = 6 - dist_from_monday
        monday_date_on_same_week = req_date - datetime.timedelta(days=dist_from_monday)
        sunday_date_on_same_week = req_date + datetime.timedelta(days=dist_from_next_sunday)
        return  monday_date_on_same_week, sunday_date_on_same_week
    
    def get_queryset(self):
        # need this when using dynamically request parameters in view
        if getattr(self, 'swagger_fake_view', False):
        # queryset just for schema generation metadata
            return Race.objects.none()
        
        date_for_week_filter = self.request.query_params.get('date_for_week_filter')
        if date_for_week_filter is None:
            raise serializers.ValidationError('date_for_week_filter parameter is required, like 2019-06-21')
        racesets = RaceSet.objects.filter(date__range = self.get_same_week_range(date_for_week_filter))
        return racesets

    date_for_week_filter = openapi.Parameter(name='date_for_week_filter', in_=openapi.IN_QUERY, description="週間検索用の日にち", type=openapi.FORMAT_DATE)
    @swagger_auto_schema(description='検索日時と同週の競走のリストを取得', manual_parameters=[date_for_week_filter])
    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)
        logger.info('date_for_week_filter={}のracesetsが照会された'.format(request.query_params.get('date_for_week_filter')))
        return response
    
    crawl_and_pred_flag = openapi.Parameter(name='crawl_and_pred_flag', in_=openapi.IN_QUERY, description="今週のレース情報をクロールして、作成したモデルから確率予測を行うフラグ", type=openapi.FORMAT_INT64)
    @swagger_auto_schema(manual_parameters=[date_for_week_filter])
    def create(self, request):
        crawl_and_pred_flag = self.request.data['crawl_and_pred_flag']
        print(crawl_and_pred_flag)
        if crawl_and_pred_flag != 1:
            raise serializers.ValidationError('crawl_and_pred_flag:1 is required')
        response = super().create(self, request)
        logger.info('racesets{}件登録しました。'.format(request.data))
        return response

class RaceListWithHorseAPIView(generics.ListAPIView):
    """
    raceの操作をする
    
    get:
    racesets(競走名)に属するraceのリストを取得する
    """
    serializer_class = RaceSerializer
    def get_queryset(self):
        # need this when using dynamically request parameters in view
        if getattr(self, 'swagger_fake_view', False):
        # queryset just for schema generation metadata
            return Race.objects.none()
        return Race.objects.filter(raceset_name=self.kwargs['pk'])
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        logger.info('id={}のracesetが照会された'.format(request.kwargs['pk']))
        return response