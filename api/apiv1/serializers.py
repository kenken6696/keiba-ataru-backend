from rest_framework import serializers
from .models import RaceSet, Race, Horse

class RaceSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceSet
        fields =  ('id', 'raceset_name', 'date', 'racecourse')

class HorseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horse
        fields =  ('horse_number', 'horse_name', 'trio_pred')

class RaceSerializer(serializers.ModelSerializer):
    starttime = serializers.TimeField(format='%H:%M')
    horses = serializers.SerializerMethodField()
    
    class Meta:
        model = Race
        fields =  ('race_name', 'round_number', 'starttime', 'horses')

    def get_horses(self, instance):
        horses_config = instance.horses.all().order_by('horse_number')
        return HorseSerializer(horses_config, many=True).data