from django.db import models
from django.contrib.auth.models import AbstractUser

##
## ユーザ関係モデル
##
# 属性ラベルモデル
class Label(models.Model):
    name = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name

# 候補者モデル
class Candidate(AbstractUser):
    label = models.ManyToManyField(Label, related_name='candidates')
    message_addr = models.URLField()