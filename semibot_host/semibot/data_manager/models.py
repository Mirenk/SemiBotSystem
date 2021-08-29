from django.db import models
from django.contrib.auth.models import AbstractUser

##
## ユーザ関係モデル
##
# ラベル集合
# e.g 学部生,院生を含んでいる「学生」といった集合。参照時便利にするためでラベルではない
class LabelSet(models.Model):
    name = models.CharField(unique=True, max_length=10)
    def __str__(self):
        return self.name

# 属性ラベルモデル
class Label(models.Model):
    name = models.CharField(unique=True, max_length=10)
    labelset = models.ForeignKey(LabelSet, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

# 候補者モデル
class Candidate(AbstractUser):
    label = models.ManyToManyField(Label, related_name='candidates')
    message_addr = models.URLField()