from .matching_pb import type_pb2, data_manage_pb2, data_manage_pb2_grpc
from .models import TaskRequestRequest

# 候補者グループ選択
# ラベルセットを読み込み、候補者を抽出する
# task_requestに返事待機中の候補者がいれば、それを除外し関連を削除
# その時点で空だった場合、ラベルセットの先頭を破棄し、自身を呼び直す
# send_messageを呼び、再募集日時を書き込み処理終了
def select_candidate_group(task_request: TaskRequestRequest):
    pass

# 依頼送付
# task_requestのrequesting_candidatesに送付
def send_message(task_request: TaskRequestRequest):
    pass

# 参加受付処理
# task_requestの必要人数と最大人数を加味しながら依頼に候補者を繋げる
def join_task(task_request: TaskRequestRequest, userid: str):
    pass