from django.urls import path
from apiv1 import views

app_name = 'apiv1'
urlpatterns = [
    path('racesets/', views.RaceSetListAPIView.as_view()),
    path('racesets/<pk>/races', views.RaceListWithHorseAPIView.as_view()),
]