from django.db import models

# Write Model
class RaceSet(models.Model):
    race_set_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    race_set_name = models.CharField(verbose_name='競走名', max_length=100)
    date = models.DateField(verbose_name='実施日')
    racecourse = models.CharField(verbose_name='競馬場', max_length=100)

class Race(models.Model):
    race_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    race_name = models.CharField(verbose_name='レース名', max_length=100)
    round = models.IntegerField(verbose_name='ラウンド')
    race_starttime = models.DateField(verbose_name='レース開始時間')


class Horse(models.Model):
    race_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    horse_number = models.IntegerField(verbose_name='馬順')
    horse_name = models.CharField(verbose_name='馬名', max_length=100)
    trio_pred = models.IntegerField(verbose_name='三連複予想')