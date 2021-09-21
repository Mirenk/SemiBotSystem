import time
from google.protobuf import timestamp_pb2
from django_grpc_framework.test import RPCTestCase
from .matching_pb import server_pb2, server_pb2_grpc, type_pb2
from .models import TaskRequestRequest
from datetime import datetime

class MathcingServerTest(RPCTestCase):
    def test_add_task_request(self):
        task_request_data = type_pb2.TaskRequestData()
        task_request_data.name = 'testrequest'

        task_pb = type_pb2.Task(name='testtask')
        task_request_data.task.CopyFrom(task_pb)

        task_date = datetime.now()
        task_date_pb = timestamp_pb2.Timestamp(seconds=int(task_date.timestamp()))
        task_request_data.task_date.CopyFrom(task_date_pb)

        request = server_pb2.AddTaskRequestRequest()
        request.task_request.CopyFrom(task_request_data)

        label1 = type_pb2.Label(name='test1')
        label2 = type_pb2.Label(name='test2')
        label_value = type_pb2.LabelValue(value=1)
        label_value.label.CopyFrom(label2)

        labelset1 = server_pb2.AddTaskRequestRequest.LabelSet()
        labelset1.const_label.append(label1)
        labelset1.var_label.append(label_value)
        labelset2 = server_pb2.AddTaskRequestRequest.LabelSet()
        labelset2.const_label.append(label1)

        request.label_set.append(labelset1)
        request.label_set.append(labelset2)

        end_date = datetime.now()
        end_date_pb = timestamp_pb2.Timestamp(seconds=int(end_date.timestamp()))
        request.matching_end_date.CopyFrom(end_date_pb)

        request.callback_url = 'http://example.com'

        print(request)

        stub = server_pb2_grpc.MatchingServerStub(self.channel)
        res = stub.AddTaskRequest(request)

        record = TaskRequestRequest.objects.all().first()

        self.assertEqual(record.name, 'testrequest')
        self.assertEqual(record.task, 'testtask')
        self.assertEqual(int(record.task_datetime.timestamp()), int(task_date.timestamp()))
        self.assertEqual(int(record.matching_end_datetime.timestamp()), int(end_date.timestamp()))

        label_set = record.label_set.all()

        self.assertEqual(label_set[0].var_label.first().value, 1)
        self.assertEqual(label_set[1].var_label.first(), None)
