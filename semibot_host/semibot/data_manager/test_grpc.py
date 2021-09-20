import grpc
from django_grpc_framework.test import RPCTestCase
from .matching_pb import data_manage_pb2, data_manage_pb2_grpc, type_pb2
from data_manager.models import Label, LabelValue, PersonalData, Task, TaskRequest
import time
from datetime import datetime

class DataManageTest(RPCTestCase):
    def test_list_labels(self):
        Label.objects.create(name='test1')
        Label.objects.create(name='test2')
        stub = data_manage_pb2_grpc.DataManageStub(self.channel)
        res = stub.ListLabels(data_manage_pb2.ListLabelsRequest())
        print(res)
        self.assertEqual(res.labels[0].name, 'test1')
        self.assertEqual(res.labels[1].name, 'test2')
        self.assertEqual(len(res.labels), 2)

    def test_list_personal_data(self):
        label1 = Label.objects.create(name='test1')
        label2 = Label.objects.create(name='test2')

        testperson = PersonalData.objects.create(username='testuser', first_name='test', last_name='user', message_addr='http://example.com')

        testperson.label.add(label1)
        testperson.label.add(label2)

        stub = data_manage_pb2_grpc.DataManageStub(self.channel)
        res = stub.ListPersonalData(data_manage_pb2.ListPersonalDataRequest())

        print(res)
        self.assertEqual(res.personal_data[0].id, testperson.username)
        self.assertEqual(res.personal_data[0].name, testperson.first_name + testperson.last_name)
        self.assertEqual(res.personal_data[0].message_addr, testperson.message_addr)
        self.assertEqual(res.personal_data[0].labels[0].name, 'test1')
        self.assertEqual(res.personal_data[0].labels[1].name, 'test2')

    def test_list_task(self):
        label1 = Label.objects.create(name='test1')
        label2 = Label.objects.create(name='test2')
        label_value = LabelValue.objects.create(label=label2, value=1)

        testtask = Task.objects.create(name='test')
        testtask.require_label.add(label1)
        testtask.require_label_value.add(label_value)

        stub = data_manage_pb2_grpc.DataManageStub(self.channel)
        res = stub.ListTasks(data_manage_pb2.ListTasksRequest())

        print(res)
        self.assertEqual(res.tasks[0].name, testtask.name)
        self.assertEqual(res.tasks[0].require_label[0].name, 'test1')
        self.assertEqual(res.tasks[0].require_label_value[0].label.name, 'test2')
        self.assertEqual(res.tasks[0].require_label_value[0].value, 1)

    def test_get_task_from_name(self):
        label1 = Label.objects.create(name='test1')
        label2 = Label.objects.create(name='test2')
        label_value = LabelValue.objects.create(label=label2, value=1)

        testtask = Task.objects.create(name='test')
        testtask.require_label.add(label1)
        testtask.require_label_value.add(label_value)

        stub = data_manage_pb2_grpc.DataManageStub(self.channel)
        res = stub.GetTaskFromName(data_manage_pb2.GetTaskFromNameRequest(name=testtask.name))

        print(res)
        self.assertEqual(res.name, testtask.name)
        self.assertEqual(res.require_label[0].name, 'test1')
        self.assertEqual(res.require_label_value[0].label.name, 'test2')
        self.assertEqual(res.require_label_value[0].value, 1)

    def test_get_task_request_histories(self):
        testtask = Task.objects.create(name='test')
        dumtask = Task.objects.create(name='dummy')

        now = time.time()

        t_r1 = TaskRequest.objects.create(name='test1', task=testtask, work_datetime=datetime.fromtimestamp(now))
        t_r2 = TaskRequest.objects.create(name='test2', task=testtask, work_datetime=datetime.fromtimestamp(now))
        t_r3 = TaskRequest.objects.create(name='test3', task=dumtask, work_datetime=datetime.fromtimestamp(now))

        stub = data_manage_pb2_grpc.DataManageStub(self.channel)
        res = stub.GetTaskRequestHistories(type_pb2.Task(name='test'))

        print(res)
        self.assertEqual(len(res.task_requests), 2)
        self.assertEqual(res.task_requests[0].name, t_r1.name)
        self.assertEqual(res.task_requests[1].name, t_r2.name)