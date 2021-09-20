# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data_manage.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import type_pb2 as type__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='data_manage.proto',
  package='matching',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x64\x61ta_manage.proto\x12\x08matching\x1a\ntype.proto\"\x13\n\x11ListLabelsRequest\"5\n\x12ListLabelsResponse\x12\x1f\n\x06labels\x18\x01 \x03(\x0b\x32\x0f.matching.Label\"\x19\n\x17ListPersonalDataRequest\"I\n\x18ListPersonalDataResponse\x12-\n\rpersonal_data\x18\x01 \x03(\x0b\x32\x16.matching.PersonalData\"\x12\n\x10ListTasksRequest\"2\n\x11ListTasksResponse\x12\x1d\n\x05tasks\x18\x01 \x03(\x0b\x32\x0e.matching.Task\"&\n\x16GetTaskFromNameRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"S\n\x1fGetTaskRequestHistoriesResponse\x12\x30\n\rtask_requests\x18\x01 \x03(\x0b\x32\x19.matching.TaskRequestData\"*\n\x1cGetPersonalDataFromIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x95\x01\n\x1eRecordTaskRequestHistoryResult\x12?\n\x06result\x18\x01 \x01(\x0e\x32/.matching.RecordTaskRequestHistoryResult.Result\x12\x0f\n\x07message\x18\x02 \x01(\t\"!\n\x06Result\x12\x0b\n\x07SUCCESS\x10\x00\x12\n\n\x06\x46\x41ILED\x10\x01\x32\xcc\x04\n\nDataManage\x12G\n\nListLabels\x12\x1b.matching.ListLabelsRequest\x1a\x1c.matching.ListLabelsResponse\x12Y\n\x10ListPersonalData\x12!.matching.ListPersonalDataRequest\x1a\".matching.ListPersonalDataResponse\x12\x44\n\tListTasks\x12\x1a.matching.ListTasksRequest\x1a\x1b.matching.ListTasksResponse\x12\x43\n\x0fGetTaskFromName\x12 .matching.GetTaskFromNameRequest\x1a\x0e.matching.Task\x12U\n\x17GetTaskRequestHistories\x12\x0f.matching.Label\x1a).matching.GetTaskRequestHistoriesResponse\x12W\n\x15GetPersonalDataFromId\x12&.matching.GetPersonalDataFromIdRequest\x1a\x16.matching.PersonalData\x12_\n\x18RecordTaskRequestHistory\x12\x19.matching.TaskRequestData\x1a(.matching.RecordTaskRequestHistoryResultb\x06proto3'
  ,
  dependencies=[type__pb2.DESCRIPTOR,])



_RECORDTASKREQUESTHISTORYRESULT_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='matching.RecordTaskRequestHistoryResult.Result',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=579,
  serialized_end=612,
)
_sym_db.RegisterEnumDescriptor(_RECORDTASKREQUESTHISTORYRESULT_RESULT)


_LISTLABELSREQUEST = _descriptor.Descriptor(
  name='ListLabelsRequest',
  full_name='matching.ListLabelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=43,
  serialized_end=62,
)


_LISTLABELSRESPONSE = _descriptor.Descriptor(
  name='ListLabelsResponse',
  full_name='matching.ListLabelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='labels', full_name='matching.ListLabelsResponse.labels', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=64,
  serialized_end=117,
)


_LISTPERSONALDATAREQUEST = _descriptor.Descriptor(
  name='ListPersonalDataRequest',
  full_name='matching.ListPersonalDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=144,
)


_LISTPERSONALDATARESPONSE = _descriptor.Descriptor(
  name='ListPersonalDataResponse',
  full_name='matching.ListPersonalDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='personal_data', full_name='matching.ListPersonalDataResponse.personal_data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=146,
  serialized_end=219,
)


_LISTTASKSREQUEST = _descriptor.Descriptor(
  name='ListTasksRequest',
  full_name='matching.ListTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=221,
  serialized_end=239,
)


_LISTTASKSRESPONSE = _descriptor.Descriptor(
  name='ListTasksResponse',
  full_name='matching.ListTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tasks', full_name='matching.ListTasksResponse.tasks', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=241,
  serialized_end=291,
)


_GETTASKFROMNAMEREQUEST = _descriptor.Descriptor(
  name='GetTaskFromNameRequest',
  full_name='matching.GetTaskFromNameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='matching.GetTaskFromNameRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=293,
  serialized_end=331,
)


_GETTASKREQUESTHISTORIESRESPONSE = _descriptor.Descriptor(
  name='GetTaskRequestHistoriesResponse',
  full_name='matching.GetTaskRequestHistoriesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_requests', full_name='matching.GetTaskRequestHistoriesResponse.task_requests', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=333,
  serialized_end=416,
)


_GETPERSONALDATAFROMIDREQUEST = _descriptor.Descriptor(
  name='GetPersonalDataFromIdRequest',
  full_name='matching.GetPersonalDataFromIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='matching.GetPersonalDataFromIdRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=418,
  serialized_end=460,
)


_RECORDTASKREQUESTHISTORYRESULT = _descriptor.Descriptor(
  name='RecordTaskRequestHistoryResult',
  full_name='matching.RecordTaskRequestHistoryResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='matching.RecordTaskRequestHistoryResult.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='matching.RecordTaskRequestHistoryResult.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RECORDTASKREQUESTHISTORYRESULT_RESULT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=463,
  serialized_end=612,
)

_LISTLABELSRESPONSE.fields_by_name['labels'].message_type = type__pb2._LABEL
_LISTPERSONALDATARESPONSE.fields_by_name['personal_data'].message_type = type__pb2._PERSONALDATA
_LISTTASKSRESPONSE.fields_by_name['tasks'].message_type = type__pb2._TASK
_GETTASKREQUESTHISTORIESRESPONSE.fields_by_name['task_requests'].message_type = type__pb2._TASKREQUESTDATA
_RECORDTASKREQUESTHISTORYRESULT.fields_by_name['result'].enum_type = _RECORDTASKREQUESTHISTORYRESULT_RESULT
_RECORDTASKREQUESTHISTORYRESULT_RESULT.containing_type = _RECORDTASKREQUESTHISTORYRESULT
DESCRIPTOR.message_types_by_name['ListLabelsRequest'] = _LISTLABELSREQUEST
DESCRIPTOR.message_types_by_name['ListLabelsResponse'] = _LISTLABELSRESPONSE
DESCRIPTOR.message_types_by_name['ListPersonalDataRequest'] = _LISTPERSONALDATAREQUEST
DESCRIPTOR.message_types_by_name['ListPersonalDataResponse'] = _LISTPERSONALDATARESPONSE
DESCRIPTOR.message_types_by_name['ListTasksRequest'] = _LISTTASKSREQUEST
DESCRIPTOR.message_types_by_name['ListTasksResponse'] = _LISTTASKSRESPONSE
DESCRIPTOR.message_types_by_name['GetTaskFromNameRequest'] = _GETTASKFROMNAMEREQUEST
DESCRIPTOR.message_types_by_name['GetTaskRequestHistoriesResponse'] = _GETTASKREQUESTHISTORIESRESPONSE
DESCRIPTOR.message_types_by_name['GetPersonalDataFromIdRequest'] = _GETPERSONALDATAFROMIDREQUEST
DESCRIPTOR.message_types_by_name['RecordTaskRequestHistoryResult'] = _RECORDTASKREQUESTHISTORYRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListLabelsRequest = _reflection.GeneratedProtocolMessageType('ListLabelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTLABELSREQUEST,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.ListLabelsRequest)
  })
_sym_db.RegisterMessage(ListLabelsRequest)

ListLabelsResponse = _reflection.GeneratedProtocolMessageType('ListLabelsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTLABELSRESPONSE,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.ListLabelsResponse)
  })
_sym_db.RegisterMessage(ListLabelsResponse)

ListPersonalDataRequest = _reflection.GeneratedProtocolMessageType('ListPersonalDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTPERSONALDATAREQUEST,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.ListPersonalDataRequest)
  })
_sym_db.RegisterMessage(ListPersonalDataRequest)

ListPersonalDataResponse = _reflection.GeneratedProtocolMessageType('ListPersonalDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTPERSONALDATARESPONSE,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.ListPersonalDataResponse)
  })
_sym_db.RegisterMessage(ListPersonalDataResponse)

ListTasksRequest = _reflection.GeneratedProtocolMessageType('ListTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTTASKSREQUEST,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.ListTasksRequest)
  })
_sym_db.RegisterMessage(ListTasksRequest)

ListTasksResponse = _reflection.GeneratedProtocolMessageType('ListTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTTASKSRESPONSE,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.ListTasksResponse)
  })
_sym_db.RegisterMessage(ListTasksResponse)

GetTaskFromNameRequest = _reflection.GeneratedProtocolMessageType('GetTaskFromNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETTASKFROMNAMEREQUEST,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.GetTaskFromNameRequest)
  })
_sym_db.RegisterMessage(GetTaskFromNameRequest)

GetTaskRequestHistoriesResponse = _reflection.GeneratedProtocolMessageType('GetTaskRequestHistoriesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTASKREQUESTHISTORIESRESPONSE,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.GetTaskRequestHistoriesResponse)
  })
_sym_db.RegisterMessage(GetTaskRequestHistoriesResponse)

GetPersonalDataFromIdRequest = _reflection.GeneratedProtocolMessageType('GetPersonalDataFromIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPERSONALDATAFROMIDREQUEST,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.GetPersonalDataFromIdRequest)
  })
_sym_db.RegisterMessage(GetPersonalDataFromIdRequest)

RecordTaskRequestHistoryResult = _reflection.GeneratedProtocolMessageType('RecordTaskRequestHistoryResult', (_message.Message,), {
  'DESCRIPTOR' : _RECORDTASKREQUESTHISTORYRESULT,
  '__module__' : 'data_manage_pb2'
  # @@protoc_insertion_point(class_scope:matching.RecordTaskRequestHistoryResult)
  })
_sym_db.RegisterMessage(RecordTaskRequestHistoryResult)



_DATAMANAGE = _descriptor.ServiceDescriptor(
  name='DataManage',
  full_name='matching.DataManage',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=615,
  serialized_end=1203,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListLabels',
    full_name='matching.DataManage.ListLabels',
    index=0,
    containing_service=None,
    input_type=_LISTLABELSREQUEST,
    output_type=_LISTLABELSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListPersonalData',
    full_name='matching.DataManage.ListPersonalData',
    index=1,
    containing_service=None,
    input_type=_LISTPERSONALDATAREQUEST,
    output_type=_LISTPERSONALDATARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListTasks',
    full_name='matching.DataManage.ListTasks',
    index=2,
    containing_service=None,
    input_type=_LISTTASKSREQUEST,
    output_type=_LISTTASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetTaskFromName',
    full_name='matching.DataManage.GetTaskFromName',
    index=3,
    containing_service=None,
    input_type=_GETTASKFROMNAMEREQUEST,
    output_type=type__pb2._TASK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetTaskRequestHistories',
    full_name='matching.DataManage.GetTaskRequestHistories',
    index=4,
    containing_service=None,
    input_type=type__pb2._LABEL,
    output_type=_GETTASKREQUESTHISTORIESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetPersonalDataFromId',
    full_name='matching.DataManage.GetPersonalDataFromId',
    index=5,
    containing_service=None,
    input_type=_GETPERSONALDATAFROMIDREQUEST,
    output_type=type__pb2._PERSONALDATA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RecordTaskRequestHistory',
    full_name='matching.DataManage.RecordTaskRequestHistory',
    index=6,
    containing_service=None,
    input_type=type__pb2._TASKREQUESTDATA,
    output_type=_RECORDTASKREQUESTHISTORYRESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DATAMANAGE)

DESCRIPTOR.services_by_name['DataManage'] = _DATAMANAGE

# @@protoc_insertion_point(module_scope)
