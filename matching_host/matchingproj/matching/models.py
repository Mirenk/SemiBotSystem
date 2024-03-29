from django.db import models
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask

# ラベル
class Label(models.Model):
    name = models.CharField(unique=True, max_length=20)
    is_dynamic = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# 数値ラベル
class LabelValue(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['label', 'value'], name='labelvalue_unique')
        ]

    def __str__(self):
        return self.label.name + "(val:" + str(self.value) + ")"

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

    def __str__(self):
        return self.personal_data.username + "(" + self.request_datetime.strftime("%Y/%m/%d %H:%M:%S") + ")"

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
    matching_complete_message = models.TextField() # マッチング完了時に送るメッセージ本文

    # 候補者グループ選択時に利用するフィールド
    # 参加表明をした候補者
    joined_candidates = models.ManyToManyField(Candidate, blank=True, related_name="joined_task_request")
    # 返事待機中の候補者
    requesting_candidates = models.ManyToManyField(Candidate, blank=True, related_name="reserve_task_request")
    # 不参加表明をした候補者
    decline_candidates = models.ManyToManyField(Candidate, blank=True, related_name="declined_task_request")
    # 再募集間隔
    rematching_duration = models.DurationField()
    # 次の再募集
    next_rematching = models.DateTimeField()

    # 再募集、終了のタスクを記録
    check_joined_candidates_task = models.ForeignKey(PeriodicTask, on_delete=models.PROTECT, related_name='check_taskrequest', null=True, blank=True)
    end_matching_task = models.ForeignKey(PeriodicTask, on_delete=models.PROTECT, related_name='end_request', null=True, blank=True)

    # 依頼募集が終了しているかのフラグ
    is_complete = models.BooleanField(default=False)

# 依頼リクエスト-ラベルセット間、順序を保つために使用
class ThroughRequestLabelSet(models.Model):
    task_request = models.ForeignKey(TaskRequestRequest, on_delete=models.CASCADE)
    label_set = models.ForeignKey(LabelSet, on_delete=models.CASCADE)
    class Meta:
        ordering = ('id', )

# 参加ログ
class JoinResponseHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task_request = models.ForeignKey(TaskRequestRequest, on_delete=models.CASCADE)
    join_at = models.DateTimeField(auto_now_add=True)

# 不参加ログ
class DeclineResponseHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task_request = models.ForeignKey(TaskRequestRequest, on_delete=models.CASCADE)
    decline_at = models.DateTimeField(auto_now_add=True)

# キャンセルログ
class CancelResponseHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task_request = models.ForeignKey(TaskRequestRequest, on_delete=models.CASCADE)
    cancel_at = models.DateTimeField(auto_now_add=True)

# 人数集まった時刻ログ
class FillRequireCandidateHistory(models.Model):
    task_request = models.ForeignKey(TaskRequestRequest, on_delete=models.CASCADE)
    fill_at = models.DateTimeField(auto_now_add=True)