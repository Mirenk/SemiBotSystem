from django.test import TestCase
from .make_test_data import *
from datetime import datetime
from matching.tasks import check_joined_candidates

class TaskTest(TestCase):
    def test_check_joined_candidates(self):
        # 各データ準備
        # 依頼データ生成
        task_request = make_test_task_request()

        check_joined_candidates(task_request.id)
