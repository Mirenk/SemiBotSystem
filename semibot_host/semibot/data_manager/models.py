from django.db import models
from django.contrib.auth.models import AbstractUser

##
## ラベル関係モデル
##
# 基底ラベルモデル
class BaseLabel(models.Model):
    name = models.CharField(unique=True, max_length=10)

##
## ユーザ関係モデル
##
# ラベル集合
# e.g 学部生,院生を含んでいる「学生」といった集合。参照時便利にするためでラベルではない
class LabelSet(BaseLabel):
    def __str__(self):
        return self.name

# 属性ラベルモデル
class Label(BaseLabel):
    labelset = models.ForeignKey(LabelSet, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

# 候補者モデル
class Candidate(AbstractUser):
    label = models.ManyToManyField(Label, related_name='candidates')
    message_addr = models.URLField()

##
## 履歴関係モデル
##
# 値付きラベル
# 必要ラベル値や推奨ラベル値を格納
class LabelValue(models.Model):
    label = models.ForeignKey(BaseLabel, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['label, value'], name='label_value_unique')
        ]

# 作業モデル
# これは現実の作業を示している。マッチングシステムのタスクではない。
class Task(models.Model):
    name = models.CharField(unique=True, max_length=20)
    require_label_value = models.ManyToManyField(LabelValue, related_name='require_task')

# 作業履歴モデル
# 作業と候補者グループのマッチング結果を格納
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    worker = models.ManyToManyField(Candidate, related_name='joined_task')
    recommend_label_value = models.ManyToManyField(LabelValue, related_name='recommend_task')