from django.db import models

# 一時的に依頼を保存しておくモデル
# start_matching_datetimeで指定した時間で発火
class TaskRequest(models.Model):
    task_datetime = models.DateTimeField()
    bachelor_num = models.IntegerField()
    master_num = models.IntegerField()
