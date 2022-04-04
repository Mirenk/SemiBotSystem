from django.test import TestCase
from matching.models import TaskRequestRequest, LabelSet, LabelValue, Label
import matching.matching as matching
from .make_test_data import *
import os
from datetime import datetime, timedelta

class MatchingTest(TestCase):
    # 候補者グループテスト
    def test_select_candidate_group(self):
        # 各データ準備
        dir = os.path.dirname(__file__)
        label_path = os.path.join(dir, 'test_csv/label.csv')
        personal_data_path = os.path.join(dir, 'test_csv/personal_data.csv')
        label_relate_path = os.path.join(dir, 'test_csv/label_relate.csv')
        history_path = os.path.join(dir, 'test_csv/history.csv')

        label_dict = make_label_from_csv(label_path)
        personal_data = make_personal_data_from_csv(personal_data_path)
        add_label_relate_to_personal_data(personal_data, label_dict, label_relate_path)
        task_request_history = make_task_request_history_from_csv(personal_data, history_path)

        # 依頼データ生成
        task_request = make_test_task_request()
        print(type(task_request))

        # 呼び出し呼び出し呼び出し動け動け動け動け！！！！！！
        matching.select_candidate_group(task_request, personal_data, task_request_history)

        # TODO: 抽出した候補者が適当であるかの確認コード