from django.test import TestCase
from .make_test_data import *
from datetime import datetime
from matching.tasks import check_joined_candidates, end_matching_task
from matching.matching import join_task, cancel_task

class TaskTest(TestCase):
    def test_check_joined_candidates(self):
        # 各データ準備
        # 依頼データ生成
        task_request = make_test_task_request()

        check_joined_candidates(task_request.id)

    # チェック項目
    # ・matching.join_taskが正常動作かどうか
    # ・end_matching_taskで候補者絞り込みが出来ているかどうか
    # ・一時データが削除されているかどうか
    def test_end_matching_task(self):
        task_request = make_test_task_request()

        print('test_end_matching_task: first matching')
        # 一回目の募集
        check_joined_candidates(task_request.id)
        task_request = TaskRequestRequest.objects.get(id=task_request.id)
        # 全員参加させる
        for candidate in task_request.requesting_candidates.all():
            print('test_end_matching_task: joining', candidate.personal_data.username)
            join_task(task_request, candidate.personal_data)

        # 二人キャンセルさせる
        for candidate in task_request.joined_candidates.all()[:2]:
            print('test_end_matching_task: canceling', candidate.personal_data.username)
            cancel_task(task_request, candidate.personal_data)

        print('test_end_matching_task: second matching')
        # 二回目の募集
        check_joined_candidates(task_request.id)
        # 候補者全員参加させる
        for candidate in task_request.requesting_candidates.all():
            join_task(task_request, candidate.personal_data)

        end_matching_task(task_request.id)

        self.assertEqual(TaskRequestRequest.objects.filter(id=task_request.id).first(), None)