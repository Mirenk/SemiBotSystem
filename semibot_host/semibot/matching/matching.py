from matching_pb import type_pb2
from matching.models import TaskRequestRequest, PersonalData, Candidate
from matching.dynamic_label import DynamicLabel
import matching.grpc_client as grpc_client
from datetime import datetime

# 候補者グループ選択
def select_candidate_group(task_request: TaskRequestRequest,
                           personal_data: dict[str, type_pb2.PersonalData],
                           task_request_history: list[type_pb2.TaskRequestData]):
    # 0. 各データ準備
    # ラベルセット取得
    label_set = task_request.label_set.all().first()

    # 処理用のIDのみリスト生成
    # このリストをフィルタやソートして、候補者グループを決定する
    # とりあえずユーザID順に並んでいるとする
    # この時task_requestにrequest_candidatesに候補者が存在した場合、関連を解除しリストには入れない
    personal_data_id_list = []
    for userid in personal_data.keys():
        requesting_candidate = task_request.requesting_candidates.filter(personal_data__userid=userid).first()
        if requesting_candidate is None:
            personal_data_id_list.append(userid)
        else:
            task_request.requesting_candidates.remove(requesting_candidate)
            del personal_data[userid]

    ## 1. 固定ラベルでフィルタ
    # TODO: ゼミ管理で使用しないため、未実装

    ## 2. 固定動的ラベルでソート
    # 固定動的ラベル取り出し
    const_dyn_labels = label_set.const_label.filter(is_dynamic=True)

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
    var_labels = label_set.var_label.all()

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
            if label in work_personal_data.labels:
                is_exist = True
                tmp_label_dict[label] = tmp_label_dict[label] - 1
                # 数を減らした時点で0になったら、一定数集まったということなのでラベルを削除
                if tmp_label_dict[label] == 0:
                    del tmp_label_dict[label]

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
        select_candidate_group(task_request, personal_data, task_request_history)
        return

    # 5. 最大人数を越していたら上から最大人数を取る(フィルタ)
    # ここでグループは確定
    if len(personal_data_id_list) > task_request.max_candidates:
        personal_data_id_list = personal_data_id_list[:task_request.max_candidates]

    # task_requestのrequesting_candidatesに候補者を付け、send_messageを呼び動作終了
    now = datetime.now()
    for userid in personal_data_id_list:
        personal_data_record, create = PersonalData.objects.get_or_create(userid=userid)
        record = Candidate.objects.create(personal_data=personal_data_record, request_datetime=now)

        task_request.requesting_candidates.add(record)

    # debug
    print('DEBUG: select_candidate_group')
    for personal_data_id in personal_data_id_list:
        print(personal_data_id)

# 依頼送付
# task_requestのrequesting_candidatesに送付
def send_message(task_request: TaskRequestRequest):
    pass

# 参加受付処理
# task_requestの必要人数と最大人数を加味しながら依頼に候補者を繋げる
def join_task(task_request: TaskRequestRequest, userid: str):
    pass