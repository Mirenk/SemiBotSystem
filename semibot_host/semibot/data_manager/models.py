from django.db import models
from django.contrib.auth.models import User

##
## ユーザ関係モデル
##
# 属性ラベルモデル
class Label(models.Model):
    name = models.CharField()

# 候補者モデル
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    label = models.ManyToManyField(Label, related_name='candidates')

# 連絡手段モデル
class ContactMethod(models.Model):
    name = models.CharField()

# 連絡先モデル
class ContactAddress(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='contact')
    address = models.CharField()
    method = models.ForeignKey(ContactMethod, on_delete=models.CASCADE)