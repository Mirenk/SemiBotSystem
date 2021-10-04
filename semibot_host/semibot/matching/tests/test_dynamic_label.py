from django.test import TestCase
from matching.dynamic_label import DynamicLabel
from .make_test_data import *
import os.path

class DynamicLabelTest(TestCase):
    # ラベルテスト
    def test_few_join(self):
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

        # ラベル付与
        DynamicLabel.few_join(personal_data, task_request_history)

        print(personal_data)

    # ラベルテスト
    def test_past_joined(self):
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

        # ラベル付与
        DynamicLabel.past_joined(personal_data, task_request_history)

        print(personal_data)

