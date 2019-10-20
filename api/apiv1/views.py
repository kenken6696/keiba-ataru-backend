from django.shortcuts import render
from rest_framework import generics, serializers
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse
from logzero import logger
import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response

class RaceSetListAPIView(generics.ListCreateAPIView):
    """
    post and get racesets
    
    get:
    get a raceset list on this week
    
    post:
    crawl a website for raceset info on this week, and insert the predictions using my model
    """
    serializer_class = RaceSetSerializer
    swagger_schema = SwaggerAutoSchema
    
    def get_this_week_range(self):
        req_date = datetime.date.today()
        dist_from_monday = req_date.weekday()
        dist_from_next_sunday = 6 - dist_from_monday
        monday_date_on_same_week = req_date - datetime.timedelta(days=dist_from_monday)
        sunday_date_on_same_week = req_date + datetime.timedelta(days=dist_from_next_sunday)
        return  monday_date_on_same_week, sunday_date_on_same_week
    
    def get_queryset(self):
        # need this when using dynamically request parameters in view
        if getattr(self, 'swagger_fake_view', False):
        # queryset just for schema generation metadata
            return RaceSet.objects.none()
        
        filter_by_this_week = self.request.query_params.get('filter_by_this_week')
        logger.info(filter_by_this_week)
        if filter_by_this_week != 'true':# TODO serializerでちゃんとやる
            raise serializers.ValidationError({"validation_error":"{filter_by_this_week:true} is required"})
        racesets = RaceSet.objects.filter(date__range = self.get_this_week_range())
        return racesets

    filter_by_this_week = openapi.Parameter(name='filter_by_this_week', in_=openapi.IN_QUERY, description="今週分の検索フラグ", type=openapi.TYPE_BOOLEAN)
    @swagger_auto_schema(description='検索日時と同週の競走のリストを取得', manual_parameters=[filter_by_this_week])
    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)
        logger.info('filter_by_this_week={}のracesetsが照会された'.format(request.query_params.get('filter_by_this_week')))
        return response
    
    crawl_and_pred_flag = openapi.Parameter(name='crawl_and_pred_flag', in_=openapi.IN_BODY
    , description="今週のレース情報をクロールして、作成したモデルから確率予測を行うフラグ", type=openapi.FORMAT_INT64)
    @swagger_auto_schema(manual_parameters=[crawl_and_pred_flag])
    def create(self, request):
        if self.request.data['crawl_and_pred_flag'] != 1:
            raise serializers.ValidationError({"validation_error":"crawl_and_pred_flag: 1 is required"})
        
        response = Response({"result_cde":0})
        logger.info('racesets{}件登録しました。'.format(request.data))
        return response

class RaceListWithHorseAPIView(generics.ListAPIView):
    """
    get race
    
    get:
    get a race list which a raceset had
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