from django.contrib.auth.models import User
from django.conf import settings
import grpc
from matching_pb import data_manage_pb2, data_manage_pb2_grpc

class Backend:
    def authenticate(self, request, username=None, password=None):
        with grpc.insecure_channel(settings.MATCHING_DATAMANAGE_HOST) as channel:
            stub = data_manage_pb2_grpc.DataManageStub(channel)
            res = stub.Auth(data_manage_pb2.AuthRequest(username=username, password=password))

        custom_auth_result = res.result
        print(custom_auth_result)
        if custom_auth_result:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.save()
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None