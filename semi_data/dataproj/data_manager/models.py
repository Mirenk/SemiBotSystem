from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

##
## ラベル関係モデル
##
# 基底ラベルモデル
class BaseLabel(models.Model):
    name = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name

##
## ユーザ関係モデル
##
# ラベル集合
# e.g 学部生,院生を含んでいる「学生」といった集合。参照時便利にするためでラベルではない
class LabelSet(BaseLabel):
    pass

# 属性ラベルモデル
class Label(BaseLabel):
    label_set = models.ForeignKey(LabelSet, on_delete=models.PROTECT, null=True, blank=True)

# 個人情報モデル
class PersonalData(AbstractUser):
    label = models.ManyToManyField(Label, related_name='candidates', blank=True)

# 送信先情報モデル
class MessageAddress(models.Model):
    class Method(Enum):
        SLACK = (0, 'Slack')

    method = models.IntegerField(choices=[x.value for x in Method])
    userid = models.CharField(max_length=20)
    user = models.ForeignKey(PersonalData, on_delete=models.CASCADE, related_name='message_addr')
    is_primary = models.BooleanField(default=False)

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
            models.UniqueConstraint(fields=['label', 'value'], name='label_value_unique')
        ]

# 作業モデル
# これは現実の作業を示している。マッチングシステムのタスクではない。
class Task(models.Model):
    name = models.CharField(unique=True, max_length=20)
    require_label = models.ManyToManyField(Label, related_name='require_task', blank=True)
    require_label_value = models.ManyToManyField(LabelValue, related_name='require_task', blank=True)

    def __str__(self):
        return self.name

# 依頼モデル
# 作業と候補者グループのマッチング結果を格納、履歴になる
class TaskRequest(models.Model):
    name = models.CharField(max_length=20)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    work_datetime = models.DateTimeField()
    worker = models.ManyToManyField(PersonalData, related_name='joined_task', blank=True)
    recommend_label = models.ManyToManyField(Label, related_name='recommend_task', blank=True)
    recommend_label_value = models.ManyToManyField(LabelValue, related_name='recommend_task', blank=True)