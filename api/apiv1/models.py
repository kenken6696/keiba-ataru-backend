from django.db import models

# Write Model and Bussiness Logic
class Race(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='レース名', max_length=100)
    date = models.DateField(verbose_name='日時')
    racecourse = models.CharField(verbose_name='競馬場', max_length=100)


class Horse(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='馬名', max_length=100)

class Race_Prediction(models.Model):
    race_id = models.ManyToManyField(Race, verbose_name='レースID')
    horse_id
    trio_pred = models.IntegerField(verbose_name='三連複予想')