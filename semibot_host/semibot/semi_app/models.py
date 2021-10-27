from django.db import models
from django.core.validators import MinValueValidator

# 一時的に依頼を保存しておくモデル
# start_matching_datetimeで指定した時間で発火
class TaskRequest(models.Model):
    task_datetime = models.DateTimeField()
    bachelor_num = models.IntegerField(validators=[MinValueValidator(0)])
    master_num = models.IntegerField(validators=[MinValueValidator(0)])
    rematching_duration = models.DurationField(null=True)
