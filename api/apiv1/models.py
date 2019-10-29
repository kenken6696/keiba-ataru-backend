from django.db import models
from django.core import validators
import uuid

# Write Model
class RaceSet(models.Model):
    class Meta:
        db_table = 'raceset'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raceset_name = models.CharField(verbose_name='競走名', max_length=100)
    date = models.DateField(verbose_name='実施日')
    racecourse = models.CharField(verbose_name='競馬場', max_length=100)

    def __str__(self):
        return self.raceset_name

class Race(models.Model):
    class Meta:
        db_table= 'race'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    race_name = models.CharField(verbose_name='レース名', max_length=100)
    race_number = models.PositiveSmallIntegerField(verbose_name='レースナンバー', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(20)])
    starttime = models.TimeField(verbose_name='レース開始時間')
    raceset_id = models.ForeignKey(RaceSet, related_name='races', verbose_name='競走名ID', on_delete=models.CASCADE)

    def __str__(self):
        return self.race_name

class Horse(models.Model):
    class Meta:
        db_table = 'horse'
        unique_together = ('race_id', 'horse_number')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    race_id =  models.ForeignKey(Race, related_name='horses', verbose_name='レースID', on_delete=models.CASCADE)
    horse_number = models.PositiveSmallIntegerField(verbose_name='馬順', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(20)])
    horse_name = models.CharField(verbose_name='馬名', max_length=100)
    trio_pred = models.DecimalField(verbose_name='三連複予想', max_digits=4, decimal_places=3)

    def __str__(self):
        return self.horse_name