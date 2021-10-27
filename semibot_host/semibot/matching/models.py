from django.db import models
from django.contrib.auth import get_user_model


# ラベル
class Label(models.Model):
    name = models.CharField(unique=True, max_length=20)
    is_dynamic = models.BooleanField(default=False)

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

# 候補者モデル
# 依頼送付した時刻を保持する
class Candidate(models.Model):
    personal_data = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='candidate_personaldata')
    request_datetime = models.DateTimeField()

# 依頼リクエスト
# TODO: 重複登録の防止、ほぼ同一のような依頼リクエストが来ることも考えられるため、それも考慮
class TaskRequestRequest(models.Model):
    name = models.CharField(max_length=20)
    task = models.CharField(max_length=20)
    task_datetime = models.DateTimeField()
    label_set = models.ManyToManyField(LabelSet, through='ThroughRequestLabelSet')
    matching_end_datetime = models.DateTimeField()
    require_candidates = models.IntegerField() # TODO: 最低限必要な人数、Taskのほうと差別化しないと…
    max_candidates = models.IntegerField() # 最大人数
    callback_url = models.URLField(blank=True, null=True) # 終了時に叩くURL、使用しないかも

    # メッセージ送信に利用するフィールド
    # URLでは<task_request_id>、メッセージでは<join_url>,<cancel_url>を指定して、実際に送るときは適切な値が埋め込められる
    join_url = models.URLField()
    cancel_url = models.URLField()
    request_message = models.TextField() # 依頼送付時に送るメッセージ本文
    join_complete_message = models.TextField() # 参加受付完了時に送るメッセージ本文(キャンセルURLを知らせたりするために使用)
    cancel_complete_message = models.TextField()
    matching_complete_message = models.TextField # マッチング完了時に送るメッセージ本文

    # 候補者グループ選択時に利用するフィールド
    # 参加表明をした候補者
    joined_candidates = models.ManyToManyField(Candidate, blank=True, related_name="joined_task_request")
    # 返事待機中の候補者
    requesting_candidates = models.ManyToManyField(Candidate, blank=True, related_name="reserve_task_request")
    # 再募集間隔
    rematching_duration = models.DurationField()
    # 次の再募集
    next_rematching = models.DateTimeField()

# 依頼リクエスト-ラベルセット間、順序を保つために使用
class ThroughRequestLabelSet(models.Model):
    task_request = models.ForeignKey(TaskRequestRequest, on_delete=models.CASCADE)
    label_set = models.ForeignKey(LabelSet, on_delete=models.CASCADE)
    class Meta:
        ordering = ('id', )