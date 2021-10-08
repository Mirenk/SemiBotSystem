from matching_pb import type_pb2
from datetime import datetime
from google.protobuf import timestamp_pb2

import csv

# CSVファイルパス -> Label辞書
def make_label_from_csv(path: str):
    # CSV -> リスト
    label_dict = {}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) # 最初の行はヘッダとして読む

        for row in reader:
            label_pb = type_pb2.Label()
            label_pb.name = row[0]

            label_dict[label_pb.name] = label_pb

    return label_dict

# CSVファイルパス -> PersonalData辞書
def make_personal_data_from_csv(path: str):
    # CSV -> リスト
    personal_data = {}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) # 最初の行はヘッダとして読む

        for row in reader:
            personal_data_pb = type_pb2.PersonalData()
            personal_data_pb.id = row[0]
            personal_data_pb.name = row[1]
            personal_data_pb.message_addr = row[2]

            personal_data[personal_data_pb.id] = personal_data_pb

    return personal_data

# PersonalData辞書,Label辞書,関係CSV -> Label追加したPersonalData辞書
def add_label_relate_to_personal_data(personal_data: dict[str, type_pb2.PersonalData],
                                        label_dict: dict[str, type_pb2.Label],
                                        path: str):

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) # 最初の行はヘッダとして読む

        for row in reader:
            # row[0]がpersonal_dataのid、[1]がlabel.name
            # personal_dataもlabel_dictも辞書で来てるため、名前で実体を取得できる、やったね！
            personal_data[row[0]].labels[row[1]].CopyFrom(label_dict[row[1]])

# PersonalData辞書,履歴CSV -> タスク履歴辞書
def make_task_request_history_from_csv(personal_data: dict[str, type_pb2.PersonalData],
                                         path: str):
    task_history_dict = {}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) # 最初の行はヘッダとして読む

        for row in reader:
            # 時刻キー、TaskRequestDataがvalue
            # キーがなかったら作って入れて、候補者くっつける感じ
            # 最後はvalueだけのlistで返して終わり
            row_date = datetime.strptime(row[0], '%Y-%m-%d')
            date_timestamp = int(row_date.timestamp())

            # オブジェクト生成または取得
            if date_timestamp not in task_history_dict:
                task_history_pb = type_pb2.TaskRequestData()
                task_history_pb.task_date.CopyFrom(timestamp_pb2.Timestamp(seconds=date_timestamp))
            else:
                task_history_pb = task_history_dict[date_timestamp]

            # 候補者をつける
            task_history_pb.worker[row[1]].CopyFrom(personal_data[row[1]])

            # 辞書につける
            task_history_dict[date_timestamp] = task_history_pb

        task_history_list = sorted(task_history_dict.items(), key=lambda x:x[0], reverse=True)
        task_history_list = [x[1] for x in task_history_list]

        return task_history_list
