#
# 依頼に対してラベル付けし、マッチングシステムに登録するものたち
#
from matching_pb import type_pb2, server_pb2, server_pb2_grpc
from datetime import datetime

def send_matching_server(task_datetime: datetime, bachelor_num: int, master_num: int):
    print('task_datetime: ', task_datetime.strftime('%Y-%m-%d %H:%M'))
    print('bachelor_num: ', str(bachelor_num))
    print('master_num: ', str(master_num))