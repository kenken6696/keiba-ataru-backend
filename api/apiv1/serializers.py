from rest_framework import serializers
from .models import RaceSet, Race, Horse

class RaceSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceSet
        field =  ('id', 'raceset_name', 'date', 'racecourse')

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceSet
        field =  ('id', 'race_name', 'round_number', 'starttime', 'raceset_name')

class HorseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horse
        field =  ('id', 'race_name', 'horse_number', 'horse_name', 'trio_pred')
