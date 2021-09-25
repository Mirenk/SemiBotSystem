# 非同期処理用モジュール
# Celeryのセットアップが必要
# 詳しくは https://docs.celeryproject.org/en/master/django/first-steps-with-django.html
from celery import shared_task

from .models import TaskRequestRequest

# 人数確認関数
# 同時刻に複数のタスクの終了時刻が来る可能性があるので、ここを並列処理する
@shared_task
def check_joined_candidates(task_request: TaskRequestRequest):
    pass

# 時刻確認関数
# プロジェクトに定期実行登録が必要、詳しくは　https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
# もし再募集時間であったら人数確認を行う
# 募集終了時間であったらクライアント側に通知を行い、募集終了
@shared_task
def check_time():
    pass