from django.test import TestCase
import matching.grpc_client as client

class RPCTest(TestCase):
    def test_get_label_dict(self):
        label_dict = client.get_label_dict()

        print(label_dict)

    def test_get_personal_data_dict(self):
        personal_data = client.get_personal_data_dict()

        print(personal_data)

    def test_get_task_request_histories(self):
        task = client.get_task_from_name('全体ゼミ')

        task_request_history = client.get_task_request_histories(task)

        print(task_request_history)
