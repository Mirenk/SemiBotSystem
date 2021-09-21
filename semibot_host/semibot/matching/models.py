from django.db import models


# ラベル
class Label(models.Model):
    name = models.CharField(unique=True, max_length=20)

# 数値ラベル
class LabelValue(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['label', 'value'], name='labelvalue_unique')
        ]

# ラベルセット
# 固定ラベルと数値ラベルのセットを保存しておくモデル
class LabelSet(models.Model):
    const_label = models.ManyToManyField(Label, blank=True)
    var_label = models.ManyToManyField(LabelValue, blank=True)

# 依頼リクエスト
# TODO: 重複登録の防止、ほぼ同一のような依頼リクエストが来ることも考えられるため、それも考慮
class TaskRequestRequest(models.Model):
    name = models.CharField(max_length=20)
    task = models.CharField(max_length=20)
    task_datetime = models.DateTimeField()
    label_set = models.ManyToManyField(LabelSet)
    matching_end_datetime = models.DateTimeField()
    callback_url = models.URLField()

