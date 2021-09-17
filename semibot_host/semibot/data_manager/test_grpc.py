import grpc
from django_grpc_framework.test import RPCTestCase
from .matching_pb import data_manage_pb2, data_manage_pb2_grpc
from data_manager.models import Label

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