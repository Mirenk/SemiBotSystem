# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: type.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='type.proto',
  package='matching',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ntype.proto\x12\x08matching\x1a\x1fgoogle/protobuf/timestamp.proto\"\x15\n\x05Label\x12\x0c\n\x04name\x18\x01 \x01(\t\";\n\nLabelValue\x12\x1e\n\x05label\x18\x01 \x01(\x0b\x32\x0f.matching.Label\x12\r\n\x05value\x18\x02 \x01(\x05\"\x89\x01\n\x0cPersonalData\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x14\n\x0cmessage_addr\x18\x03 \x01(\t\x12\x1f\n\x06labels\x18\x04 \x03(\x0b\x32\x0f.matching.Label\x12(\n\nvar_labels\x18\x05 \x03(\x0b\x32\x14.matching.LabelValue\"o\n\x04Task\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\rrequire_label\x18\x02 \x03(\x0b\x32\x0f.matching.Label\x12\x31\n\x13require_label_value\x18\x03 \x03(\x0b\x32\x14.matching.LabelValue\"\xf3\x01\n\x0fTaskRequestData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1c\n\x04task\x18\x02 \x01(\x0b\x32\x0e.matching.Task\x12-\n\ttask_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12&\n\x06worker\x18\x04 \x03(\x0b\x32\x16.matching.PersonalData\x12(\n\x0frecommend_label\x18\x05 \x03(\x0b\x32\x0f.matching.Label\x12\x33\n\x15recommend_label_value\x18\x06 \x03(\x0b\x32\x14.matching.LabelValueb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_LABEL = _descriptor.Descriptor(
  name='Label',
  full_name='matching.Label',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='matching.Label.name', index=0,
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
  serialized_start=57,
  serialized_end=78,
)


_LABELVALUE = _descriptor.Descriptor(
  name='LabelValue',
  full_name='matching.LabelValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='label', full_name='matching.LabelValue.label', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='matching.LabelValue.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=80,
  serialized_end=139,
)


_PERSONALDATA = _descriptor.Descriptor(
  name='PersonalData',
  full_name='matching.PersonalData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='matching.PersonalData.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='matching.PersonalData.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_addr', full_name='matching.PersonalData.message_addr', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='matching.PersonalData.labels', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='var_labels', full_name='matching.PersonalData.var_labels', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=142,
  serialized_end=279,
)


_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='matching.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='matching.Task.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='require_label', full_name='matching.Task.require_label', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='require_label_value', full_name='matching.Task.require_label_value', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=281,
  serialized_end=392,
)


_TASKREQUESTDATA = _descriptor.Descriptor(
  name='TaskRequestData',
  full_name='matching.TaskRequestData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='matching.TaskRequestData.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task', full_name='matching.TaskRequestData.task', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_date', full_name='matching.TaskRequestData.task_date', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker', full_name='matching.TaskRequestData.worker', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recommend_label', full_name='matching.TaskRequestData.recommend_label', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recommend_label_value', full_name='matching.TaskRequestData.recommend_label_value', index=5,
      number=6, type=11, cpp_type=10, label=3,
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
  serialized_start=395,
  serialized_end=638,
)

_LABELVALUE.fields_by_name['label'].message_type = _LABEL
_PERSONALDATA.fields_by_name['labels'].message_type = _LABEL
_PERSONALDATA.fields_by_name['var_labels'].message_type = _LABELVALUE
_TASK.fields_by_name['require_label'].message_type = _LABEL
_TASK.fields_by_name['require_label_value'].message_type = _LABELVALUE
_TASKREQUESTDATA.fields_by_name['task'].message_type = _TASK
_TASKREQUESTDATA.fields_by_name['task_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TASKREQUESTDATA.fields_by_name['worker'].message_type = _PERSONALDATA
_TASKREQUESTDATA.fields_by_name['recommend_label'].message_type = _LABEL
_TASKREQUESTDATA.fields_by_name['recommend_label_value'].message_type = _LABELVALUE
DESCRIPTOR.message_types_by_name['Label'] = _LABEL
DESCRIPTOR.message_types_by_name['LabelValue'] = _LABELVALUE
DESCRIPTOR.message_types_by_name['PersonalData'] = _PERSONALDATA
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['TaskRequestData'] = _TASKREQUESTDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Label = _reflection.GeneratedProtocolMessageType('Label', (_message.Message,), {
  'DESCRIPTOR' : _LABEL,
  '__module__' : 'type_pb2'
  # @@protoc_insertion_point(class_scope:matching.Label)
  })
_sym_db.RegisterMessage(Label)

LabelValue = _reflection.GeneratedProtocolMessageType('LabelValue', (_message.Message,), {
  'DESCRIPTOR' : _LABELVALUE,
  '__module__' : 'type_pb2'
  # @@protoc_insertion_point(class_scope:matching.LabelValue)
  })
_sym_db.RegisterMessage(LabelValue)

PersonalData = _reflection.GeneratedProtocolMessageType('PersonalData', (_message.Message,), {
  'DESCRIPTOR' : _PERSONALDATA,
  '__module__' : 'type_pb2'
  # @@protoc_insertion_point(class_scope:matching.PersonalData)
  })
_sym_db.RegisterMessage(PersonalData)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'type_pb2'
  # @@protoc_insertion_point(class_scope:matching.Task)
  })
_sym_db.RegisterMessage(Task)

TaskRequestData = _reflection.GeneratedProtocolMessageType('TaskRequestData', (_message.Message,), {
  'DESCRIPTOR' : _TASKREQUESTDATA,
  '__module__' : 'type_pb2'
  # @@protoc_insertion_point(class_scope:matching.TaskRequestData)
  })
_sym_db.RegisterMessage(TaskRequestData)


# @@protoc_insertion_point(module_scope)
