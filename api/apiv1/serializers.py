from rest_framework import serializers
from .models import RaceSet, Race, Horse

class RaceSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceSet
        fields =  ('id', 'raceset_name', 'date', 'racecourse')

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceSet
        fields =  ('id', 'race_name', 'round_number', 'starttime', 'raceset_name')

class HorseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horse
        fields =  ('id', 'race_name', 'horse_number', 'horse_name', 'trio_pred')
