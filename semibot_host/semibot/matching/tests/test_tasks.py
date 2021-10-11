from django.test import TestCase
from .make_test_data import *
from datetime import datetime
from matching.tasks import check_joined_candidates, check_time

class TaskTest(TestCase):
    def test_check_joined_candidates(self):
        # 各データ準備
        # 依頼データ生成
        task_request = make_test_task_request()

        check_joined_candidates(task_request.id)

    def test_check_time(self):
        # 依頼データ生成
        task_request = make_test_task_request()

        task_request.next_rematching = datetime.now()
        task_request.save()

        check_time()

# 書き込みが発生するため無効にしてます
#        task_request.matching_end_datetime = datetime.now()
#        task_request.save()

#        check_time()