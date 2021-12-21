from matching_pb import type_pb2
from matching.models import TaskRequestRequest, Candidate, FillRequireCandidateHistory, LabelValue
from matching.dynamic_label import DynamicLabel
import matching.grpc_client as grpc_client
from matching.message_api import SlackAPI
from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
import os

# ユーザモデル定義
# これでどのような認証を使っても動作が変わらない
User = get_user_model()

# データ準備
def prepare_personal_data(task_request: TaskRequestRequest):
    # 0. 各データ準備
    personal_data = grpc_client.get_personal_data_dict()

    # 処理用のIDのみリスト生成
    # このリストをフィルタやソートして、候補者グループを決定する
    # とりあえずユーザID順に並んでいるとする
    # この時task_requestにrequest_candidatesに候補者が存在した場合、リストには入れない
    # joined_candidatesも調べる
    personal_data_id_list = []
    for userid in list(personal_data):
        requesting_candidate = task_request.requesting_candidates.filter(personal_data__username=userid).first()
        if requesting_candidate is None:
            personal_data_id_list.append(userid)
        else:
            del personal_data[userid]

    return personal_data

# 候補者グループ選択
def select_candidate_group(task_request: TaskRequestRequest,
                           personal_data: dict[str, type_pb2.PersonalData]):

    # ラベルセット取得
    label_set = task_request.label_set.all().first()
    # 履歴取得
    task = grpc_client.get_task_from_name(task_request.task)
    task_request_history = grpc_client.get_task_request_histories(task)

    ## 1. 固定ラベルでフィルタ
    # TODO: ゼミ管理で使用しないため、未実装

    ## 2. 固定動的ラベルでソート
    # 固定動的ラベル取り出し
    if label_set is not None:
        const_dyn_labels = label_set.const_label.filter(is_dynamic=True)
    else: # 依頼に関連付けされているラベルセットがない場合
        # TODO: 作業を直接参照して取り出し
        const_dyn_labels = None

    if const_dyn_labels is not None:
        for const_dyn_label in const_dyn_labels:
            # ラベル付与
            DynamicLabel.add_dynamic_label(personal_data, task_request_history, const_dyn_label.name)

        # val_labelsの後ろからソートしていく
        tmp_list = personal_data.items()
        for i in range(len(const_dyn_labels)):
            tmp_list = sorted(tmp_list, key=lambda x:x[1].var_labels[-i].value, reverse=True)

        # ソート完了後、useridであるキーだけ取り出して終了
        personal_data_id_list = []
        for key, item in tmp_list:
            personal_data_id_list.append(key)
        del tmp_list

    ## 3 依頼についている数値ラベルの値になるようにフィルタ
    ## (一応ここでグループが決定されることがある)
    # 数値ラベル取り出し
    if label_set is not None:
        var_labels = label_set.var_label.all()
    else:
        var_labels = None

    if var_labels is not None:
        # 固定ラベルの数値ラベルでフィルタ
        var_const_labels = var_labels.filter(label__is_dynamic=False)

        # ラベル名key, 残り数をvalueにした辞書作成
        tmp_label_dict = {}
        for var_const_label in var_const_labels:
            tmp_label_dict[var_const_label.label.name] = var_const_label.value

        # フィルタ開始
        # 現在のpersonal_data_listの順に見ていき、固定ラベルが付いていたら残しカウントを下げる
        # 一つではなく複数確認し、カウントを下げる
        # 一つもついていなかった場合、除外
        for userid in list(personal_data_id_list):
            work_personal_data = personal_data[userid]
            # ラベル存在可否フラグ
            is_exist = False
            for label in list(tmp_label_dict):
                # 数を減らした時点で0になったら、一定数集まったということなのでラベルを削除
                if tmp_label_dict[label] == 0:
                    del tmp_label_dict[label]
                    continue

                if label in work_personal_data.labels:
                    is_exist = True
                    tmp_label_dict[label] = tmp_label_dict[label] - 1

            # 当てはまるラベルが一つもない、または集めるべきラベルがない場合、削除
            if not is_exist:
                personal_data_id_list.remove(userid)

    # 動的ラベルの数値ラベル
    # TODO: ゼミ管理で使用しないため、未実装

    ## 4. 最低人数を満たしていなかったらDBのlabel_setを破棄し、もう一度自身を呼ぶ
    ## このとき各引数を取り直す
    if len(personal_data_id_list) < task_request.require_candidates:
        task_request.label_set.remove(label_set)
        personal_data = grpc_client.get_personal_data_dict()
        return select_candidate_group(task_request, personal_data)

    # 5. 最大人数を越していたら上から最大人数を取る(フィルタ)
    # ここでグループは確定
    if len(personal_data_id_list) > task_request.max_candidates:
        personal_data_id_list = personal_data_id_list[:task_request.max_candidates]

    return personal_data_id_list

def send_request_to_candidates(task_request, personal_data, personal_data_id_list, is_rematching=False):
    # task_requestのrequesting_candidatesに候補者を付ける
    # この時にjoined_candidateに存在したらrequesting_candidateに追加しない
    now = datetime.now()
    for userid in personal_data_id_list:
        personal_data_record, create = User.objects.get_or_create(username=userid)
        record = Candidate.objects.create(personal_data=personal_data_record, request_datetime=now)

        if task_request.joined_candidates.filter(personal_data__username=userid).first() is None:
            print('select_candidate_group: add', personal_data_record.username)
            task_request.requesting_candidates.add(record) # 依頼中に追加

    task_request.save() # 一応セーブ

    # 依頼送信
    for candidate in task_request.requesting_candidates.all():
        userid = candidate.personal_data.username
        msg = task_request.request_message
        if is_rematching:
            send_message(personal_data[userid].message_addr, "[再募集]"+msg) # 依頼送付
        else:
            send_message(personal_data[userid].message_addr, msg)

# 依頼送付
def send_message(message_addr: type_pb2.MessageAddress, msg: str):
    method = message_addr.method

    if type_pb2.MessageAddress.Method.Name(method) == 'SLACK':
        api = SlackAPI()
    # elif ~でapiを変えていく

    api.print_send_dm(message_addr.userid, msg) # DEBUG
    # 環境変数でNOT_SEND_DMをTrueとすることで送信を抑止
    if os.environ.get('NOT_SEND_DM', 'False') != 'True':
        api.send_dm(message_addr.userid, msg)

def send_result_message(task_request: TaskRequestRequest):
    workers = task_request.joined_candidates.all()
    msg = task_request.matching_complete_message

    personal_data = grpc_client.get_personal_data_dict()

    for worker in workers:
        message_addr = personal_data[worker.personal_data.username].message_addr
        send_message(message_addr, msg)

# 人数確認
def check_fill_candidates(task_request: TaskRequestRequest):
    label_set = task_request.label_set.all().first()

    # 人数確認
    if task_request.joined_candidates.count() <= task_request.require_candidates:
        print("check_fill_candidates: Not fill require_candidates")
        return False
    # ラベル確認
    if label_set.var_label.filter(label__is_dynamic=False).filter(value__gt=0).count() != 0:
        print("check_fill_candidates: Not fill label")
        return False

    end_matching(task_request)
    return True

# 参加受付処理
def join_task(task_request: TaskRequestRequest, user: User):
    # task_requestがis_completeではない場合のみ動作
    if task_request.is_complete:
        return False

    # 処理候補者抽出
    # requestingだった場合、一度declineに下げてから処理
    requesting = task_request.requesting_candidates.filter(personal_data=user).first()
    if requesting:
        with transaction.atomic():
            task_request.requesting_candidates.remove(requesting)
            task_request.decline_candidates.add(requesting)

    candidate = task_request.decline_candidates.filter(personal_data=user).first()
    candidate_data = grpc_client.get_personal_data_from_id(user.username)

    # 依頼送付中から外し参加に付ける
    # トランザクション処理を行う
    with transaction.atomic():
        # ラベルセットの数値を減らす
        # TODO: If label_set == None ?
        label_set = task_request.label_set.all().first()
        for label_name in candidate_data.labels.keys():
            label = label_set.var_label.filter(label__is_dynamic=False).filter(label__name=label_name).first()
            print(label)
            if label is not None:
                if label.value == 0:
                    return False

                new_label, c = LabelValue.objects.get_or_create(label=label.label, value=label.value - 1)
                label_set.var_label.remove(label)
                label_set.var_label.add(new_label)

        task_request.decline_candidates.remove(candidate)
        task_request.joined_candidates.add(candidate)
        print('join_task: Joined ', candidate.personal_data.username)

    # 人数チェック
    if check_fill_candidates(task_request):
        FillRequireCandidateHistory.objects.create(task_request=task_request)

    # メッセージ送信
    candidate_pb = grpc_client.get_personal_data_from_id(user.username)
    send_message(candidate_pb.message_addr, task_request.join_complete_message)

    return True

# 参加キャンセル処理
def cancel_task(task_request: TaskRequestRequest, user: User):
    # task_requestがis_completeではない場合のみ動作
    if task_request.is_complete:
        return False

    # 処理候補者抽出
    # joinedじゃない場合、一度joinedに上げてから処理開始
    requesting = task_request.requesting_candidates.filter(personal_data=user).first()
    if requesting:
        with transaction.atomic():
            task_request.requesting_candidates.remove(requesting)
            task_request.joined_candidates.add(requesting)

    candidate = task_request.joined_candidates.filter(personal_data=user).first()
    candidate_data = grpc_client.get_personal_data_from_id(user.username)

    # join_taskと逆のことを行う
    with transaction.atomic():
        # ラベルセットの数値を減らす
        label_set = task_request.label_set.all().first()
        for label_name in candidate_data.labels.keys():
            label = label_set.var_label.filter(label__is_dynamic=False).filter(label__name=label_name).first()

            if label is not None:
                new_label, c = LabelValue.objects.get_or_create(label=label.label, value=label.value + 1)
                label_set.var_label.remove(label)
                label_set.var_label.add(new_label)

        task_request.joined_candidates.remove(candidate)
        task_request.decline_candidates.add(candidate)
        print('join_task: Canceled ', candidate.personal_data.username)

    # メッセージ送信
    candidate_pb = grpc_client.get_personal_data_from_id(user.username)
    send_message(candidate_pb.message_addr, task_request.cancel_complete_message)

# 募集終了
def end_matching(task_request: TaskRequestRequest):
    # 書き込み
    print("end_matching: End ",task_request.name,"'s matching")
    grpc_client.record_task_request_history(task_request)
    send_result_message(task_request=task_request)

    # 依頼を完了状態にする
    task_request.is_complete = True
    task_request.save()