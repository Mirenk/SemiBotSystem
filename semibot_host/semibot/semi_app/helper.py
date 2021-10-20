#
# 依頼に対してラベル付けし、マッチングシステムに登録するものたち
#
from matching_pb import type_pb2, server_pb2, server_pb2_grpc
from google.protobuf import timestamp_pb2, duration_pb2
from datetime import datetime, timedelta
from django.urls import reverse
import grpc

# 定数類
# 学部生最低人数
BACHELOR_MIN_NUM = 0
# 院生最低人数
MASTER_MIN_NUM = 0
# 再募集間隔
REMATCHING_DURATION = timedelta(weeks=1)
# 終了時刻までの間隔(ゼミ日よりどれくらい前か)
END_DURATION = timedelta(weeks=1)

def send_matching_server(task_datetime: datetime, bachelor_num: int, master_num: int):
    print('task_datetime: ', task_datetime.strftime('%Y-%m-%d %H:%M'))
    print('bachelor_num: ', str(bachelor_num))
    print('master_num: ', str(master_num))

    task_request_data = type_pb2.TaskRequestData()
    task_request_data.task.CopyFrom(type_pb2.Task(name='全体ゼミ'))
    task_request_data.task_date.CopyFrom(timestamp_pb2.Timestamp(seconds=int(task_datetime.timestamp())))

    request = server_pb2.AddTaskRequestRequest()
    request.task_request.CopyFrom(task_request_data)
    request.require_candidates = BACHELOR_MIN_NUM + MASTER_MIN_NUM
    request.max_candidates = bachelor_num + master_num

    # ラベルセット生成
    # 学部生
    bachelor_const = type_pb2.Label(name='学部生')
    bachelor_val = type_pb2.LabelValue(value=bachelor_num)
    bachelor_val.label.CopyFrom(bachelor_const)

    # 院生
    master_const = type_pb2.Label(name='院生')
    master_val = type_pb2.LabelValue(value=master_num)
    master_val.label.CopyFrom(master_const)

    # 動的ラベル
    few_join = type_pb2.Label(name='few_join')
    past_joined = type_pb2.Label(name='past_joined')

    # ラベルセット
    label_set = server_pb2.AddTaskRequestRequest.LabelSet()
    label_set.var_label.append(bachelor_val)
    label_set.var_label.append(master_val)
    label_set.const_label.append(few_join)
    label_set.const_label.append(past_joined)

    request.label_set.append(label_set)

    # 終了時刻
    end_date = task_datetime + END_DURATION
    request.matching_end_date.CopyFrom(timestamp_pb2.Timestamp(seconds=int(end_date.timestamp())))

    # 再募集間隔
    rematching_duration_pb = duration_pb2.Duration()
    rematching_duration_pb.FromTimedelta(td=REMATCHING_DURATION)
    request.rematching_duration.CopyFrom(rematching_duration_pb)

    # 参加/キャンセルURL
    request.join_url = reverse('semi_app:join')
    request.cancel_url = reverse('semi_app:cancel')

    # メッセージ
    request.request_message = task_datetime.strftime('%Y-%m-%d %H:%M') \
        + "に行われるゼミの発表候補者になりました。\n" \
        + "発表者として参加できる場合は以下のURLから参加処理を行ってください。\n" \
        + "<join_url>"
    request.join_complete_message = task_datetime.strftime('%Y-%m-%d %H:%M') \
        + "に行われるゼミの発表者として受け付けました。\n" \
        + "辞退する場合は以下のURLからキャンセル処理を行ってください。\n" \
        + "<cancel_url>"
    request.matching_complete_message = task_datetime.strftime('%Y-%m-%d %H:%M') \
        + "に行われるゼミの発表者になりました。発表準備をお願いします。"

    # マッチングサーバに送信
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.MatchingServerStub(channel=channel)
        res = stub.AddTaskRequest(request)

    # TODO: 例外処理
    print(res)