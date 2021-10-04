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
        task_request = TaskRequestRequest()
        task_request.name = 'test'
        task_request.task = 'test'
        task_request.task_datetime = datetime.now() + timedelta(weeks=3)
        task_request.matching_end_datetime = datetime.now() + timedelta(weeks=2)
        task_request.require_candidates = 4
        task_request.max_candidates = 5
        task_request.callback_url = 'http://example.com'
        task_request.rematching_duration = timedelta(weeks=1)
        task_request.next_rematching = datetime.now() + timedelta(weeks=1)
        task_request.save()

        # ラベルセット生成
        bachelor_const = Label.objects.create(name='学部生')
        master_const = Label.objects.create(name='院生')
        bachelor_val = LabelValue.objects.create(label=bachelor_const, value=3)
        master_val = LabelValue.objects.create(label=master_const, value=2)
        few_label = Label.objects.create(name='few_join', is_dynamic=True)
        past_label = Label.objects.create(name='past_joined', is_dynamic=True)
        label_set = LabelSet.objects.create()
        label_set.var_label.add(bachelor_val)
        label_set.var_label.add(master_val)
        label_set.const_label.add(few_label)
        label_set.const_label.add(past_label)

        task_request.label_set.add(label_set)

        # 呼び出し呼び出し呼び出し動け動け動け動け！！！！！！
        matching.select_candidate_group(task_request, personal_data, task_request_history)

        # TODO: 抽出した候補者が適当であるかの確認コード