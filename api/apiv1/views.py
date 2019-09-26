from django.shortcuts import render
from rest_framework import generics
from .serializers import RaceSetSerializer, RaceSerializer, HorseSerializer
from .models import RaceSet, Race, Horse

# Create your views here.
class RaceSetRetrieveAPIView(generics.RetrieveAPIView):
    queryset = RaceSet.objects.all()
    serializer_class = RaceSetSerializer

class RaceSetListAPIView(generics.ListAPIView):
    queryset = RaceSet.objects.all()
    serializer_class = RaceSetSerializer