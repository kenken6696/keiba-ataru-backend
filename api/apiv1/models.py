from django.db import models

# Write Model and Bussiness Logic
class Race_Prediction(models.Model):

    race_name = models.CharField(verbose_name='レース名', max_length=100)
    