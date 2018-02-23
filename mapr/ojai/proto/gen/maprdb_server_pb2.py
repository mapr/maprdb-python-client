# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: maprdb-server.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='maprdb-server.proto',
  package='com.mapr.maprdb.grpc',
  syntax='proto3',
  serialized_pb=_b('\n\x13maprdb-server.proto\x12\x14\x63om.mapr.maprdb.grpc\"S\n\x08RpcError\x12,\n\x03\x65rr\x18\x01 \x01(\x0e\x32\x1f.com.mapr.maprdb.grpc.ErrorCode\x12\x19\n\x11\x65rror_description\x18\x02 \x01(\t\"\x83\x01\n\x16InsertOrReplaceRequest\x12\x12\n\ntable_path\x18\x01 \x01(\t\x12?\n\x10payload_encoding\x18\x02 \x01(\x0e\x32%.com.mapr.maprdb.grpc.PayloadEncoding\x12\x14\n\x0cjson_payload\x18\x03 \x01(\t\"\x9f\x01\n\x17InsertOrReplaceResponse\x12-\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1e.com.mapr.maprdb.grpc.RpcError\x12?\n\x10payload_encoding\x18\x02 \x01(\x0e\x32%.com.mapr.maprdb.grpc.PayloadEncoding\x12\x14\n\x0cjson_payload\x18\x03 \x01(\t\"|\n\x0f\x46indByIdRequest\x12\x12\n\ntable_path\x18\x01 \x01(\t\x12?\n\x10payload_encoding\x18\x02 \x01(\x0e\x32%.com.mapr.maprdb.grpc.PayloadEncoding\x12\x14\n\x0cjson_payload\x18\x03 \x01(\t\"\x98\x01\n\x10\x46indByIdResponse\x12-\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1e.com.mapr.maprdb.grpc.RpcError\x12?\n\x10payload_encoding\x18\x02 \x01(\x0e\x32%.com.mapr.maprdb.grpc.PayloadEncoding\x12\x14\n\x0cjson_payload\x18\x03 \x01(\t\"(\n\x12\x43reateTableRequest\x12\x12\n\ntable_path\x18\x01 \x01(\t\"D\n\x13\x43reateTableResponse\x12-\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1e.com.mapr.maprdb.grpc.RpcError\"(\n\x12\x44\x65leteTableRequest\x12\x12\n\ntable_path\x18\x01 \x01(\t\"D\n\x13\x44\x65leteTableResponse\x12-\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1e.com.mapr.maprdb.grpc.RpcError\"(\n\x12TableExistsRequest\x12\x12\n\ntable_path\x18\x01 \x01(\t\"D\n\x13TableExistsResponse\x12-\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1e.com.mapr.maprdb.grpc.RpcError*\x9f\x01\n\tErrorCode\x12\x0c\n\x08NO_ERROR\x10\x00\x12\x1c\n\x18UNKNOWN_PAYLOAD_ENCODING\x10\x01\x12\x15\n\x11\x43LUSTER_NOT_FOUND\x10\x02\x12\x12\n\x0ePATH_NOT_FOUND\x10\x03\x12\x13\n\x0fTABLE_NOT_FOUND\x10\x04\x12\x12\n\x0e\x45NCODING_ERROR\x10\x05\x12\x12\n\x0e\x44\x45\x43ODING_ERROR\x10\x06*$\n\x0fPayloadEncoding\x12\x11\n\rJSON_ENCODING\x10\x00\x32\x8f\x04\n\x0cMapRDbServer\x12\x64\n\x0b\x43reateTable\x12(.com.mapr.maprdb.grpc.CreateTableRequest\x1a).com.mapr.maprdb.grpc.CreateTableResponse\"\x00\x12\x64\n\x0b\x44\x65leteTable\x12(.com.mapr.maprdb.grpc.DeleteTableRequest\x1a).com.mapr.maprdb.grpc.DeleteTableResponse\"\x00\x12\x64\n\x0bTableExists\x12(.com.mapr.maprdb.grpc.TableExistsRequest\x1a).com.mapr.maprdb.grpc.TableExistsResponse\"\x00\x12p\n\x0fInsertOrReplace\x12,.com.mapr.maprdb.grpc.InsertOrReplaceRequest\x1a-.com.mapr.maprdb.grpc.InsertOrReplaceResponse\"\x00\x12[\n\x08\x46indById\x12%.com.mapr.maprdb.grpc.FindByIdRequest\x1a&.com.mapr.maprdb.grpc.FindByIdResponse\"\x00\x42\x1e\n\x1a\x63om.mapr.maprdb.proto.grpcP\x01\x62\x06proto3')
)

_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='com.mapr.maprdb.grpc.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_ERROR', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_PAYLOAD_ENCODING', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLUSTER_NOT_FOUND', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATH_NOT_FOUND', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TABLE_NOT_FOUND', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENCODING_ERROR', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DECODING_ERROR', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1044,
  serialized_end=1203,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
_PAYLOADENCODING = _descriptor.EnumDescriptor(
  name='PayloadEncoding',
  full_name='com.mapr.maprdb.grpc.PayloadEncoding',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='JSON_ENCODING', index=0, number=0,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1205,
  serialized_end=1241,
)
_sym_db.RegisterEnumDescriptor(_PAYLOADENCODING)

PayloadEncoding = enum_type_wrapper.EnumTypeWrapper(_PAYLOADENCODING)
NO_ERROR = 0
UNKNOWN_PAYLOAD_ENCODING = 1
CLUSTER_NOT_FOUND = 2
PATH_NOT_FOUND = 3
TABLE_NOT_FOUND = 4
ENCODING_ERROR = 5
DECODING_ERROR = 6
JSON_ENCODING = 0



_RPCERROR = _descriptor.Descriptor(
  name='RpcError',
  full_name='com.mapr.maprdb.grpc.RpcError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='err', full_name='com.mapr.maprdb.grpc.RpcError.err', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_description', full_name='com.mapr.maprdb.grpc.RpcError.error_description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=128,
)


_INSERTORREPLACEREQUEST = _descriptor.Descriptor(
  name='InsertOrReplaceRequest',
  full_name='com.mapr.maprdb.grpc.InsertOrReplaceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_path', full_name='com.mapr.maprdb.grpc.InsertOrReplaceRequest.table_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload_encoding', full_name='com.mapr.maprdb.grpc.InsertOrReplaceRequest.payload_encoding', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='json_payload', full_name='com.mapr.maprdb.grpc.InsertOrReplaceRequest.json_payload', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=262,
)


_INSERTORREPLACERESPONSE = _descriptor.Descriptor(
  name='InsertOrReplaceResponse',
  full_name='com.mapr.maprdb.grpc.InsertOrReplaceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='com.mapr.maprdb.grpc.InsertOrReplaceResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload_encoding', full_name='com.mapr.maprdb.grpc.InsertOrReplaceResponse.payload_encoding', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='json_payload', full_name='com.mapr.maprdb.grpc.InsertOrReplaceResponse.json_payload', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=265,
  serialized_end=424,
)


_FINDBYIDREQUEST = _descriptor.Descriptor(
  name='FindByIdRequest',
  full_name='com.mapr.maprdb.grpc.FindByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_path', full_name='com.mapr.maprdb.grpc.FindByIdRequest.table_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload_encoding', full_name='com.mapr.maprdb.grpc.FindByIdRequest.payload_encoding', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='json_payload', full_name='com.mapr.maprdb.grpc.FindByIdRequest.json_payload', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=426,
  serialized_end=550,
)


_FINDBYIDRESPONSE = _descriptor.Descriptor(
  name='FindByIdResponse',
  full_name='com.mapr.maprdb.grpc.FindByIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='com.mapr.maprdb.grpc.FindByIdResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload_encoding', full_name='com.mapr.maprdb.grpc.FindByIdResponse.payload_encoding', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='json_payload', full_name='com.mapr.maprdb.grpc.FindByIdResponse.json_payload', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=553,
  serialized_end=705,
)


_CREATETABLEREQUEST = _descriptor.Descriptor(
  name='CreateTableRequest',
  full_name='com.mapr.maprdb.grpc.CreateTableRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_path', full_name='com.mapr.maprdb.grpc.CreateTableRequest.table_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=707,
  serialized_end=747,
)


_CREATETABLERESPONSE = _descriptor.Descriptor(
  name='CreateTableResponse',
  full_name='com.mapr.maprdb.grpc.CreateTableResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='com.mapr.maprdb.grpc.CreateTableResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=749,
  serialized_end=817,
)


_DELETETABLEREQUEST = _descriptor.Descriptor(
  name='DeleteTableRequest',
  full_name='com.mapr.maprdb.grpc.DeleteTableRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_path', full_name='com.mapr.maprdb.grpc.DeleteTableRequest.table_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=819,
  serialized_end=859,
)


_DELETETABLERESPONSE = _descriptor.Descriptor(
  name='DeleteTableResponse',
  full_name='com.mapr.maprdb.grpc.DeleteTableResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='com.mapr.maprdb.grpc.DeleteTableResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=861,
  serialized_end=929,
)


_TABLEEXISTSREQUEST = _descriptor.Descriptor(
  name='TableExistsRequest',
  full_name='com.mapr.maprdb.grpc.TableExistsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_path', full_name='com.mapr.maprdb.grpc.TableExistsRequest.table_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=931,
  serialized_end=971,
)


_TABLEEXISTSRESPONSE = _descriptor.Descriptor(
  name='TableExistsResponse',
  full_name='com.mapr.maprdb.grpc.TableExistsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='com.mapr.maprdb.grpc.TableExistsResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=973,
  serialized_end=1041,
)

_RPCERROR.fields_by_name['err'].enum_type = _ERRORCODE
_INSERTORREPLACEREQUEST.fields_by_name['payload_encoding'].enum_type = _PAYLOADENCODING
_INSERTORREPLACERESPONSE.fields_by_name['error'].message_type = _RPCERROR
_INSERTORREPLACERESPONSE.fields_by_name['payload_encoding'].enum_type = _PAYLOADENCODING
_FINDBYIDREQUEST.fields_by_name['payload_encoding'].enum_type = _PAYLOADENCODING
_FINDBYIDRESPONSE.fields_by_name['error'].message_type = _RPCERROR
_FINDBYIDRESPONSE.fields_by_name['payload_encoding'].enum_type = _PAYLOADENCODING
_CREATETABLERESPONSE.fields_by_name['error'].message_type = _RPCERROR
_DELETETABLERESPONSE.fields_by_name['error'].message_type = _RPCERROR
_TABLEEXISTSRESPONSE.fields_by_name['error'].message_type = _RPCERROR
DESCRIPTOR.message_types_by_name['RpcError'] = _RPCERROR
DESCRIPTOR.message_types_by_name['InsertOrReplaceRequest'] = _INSERTORREPLACEREQUEST
DESCRIPTOR.message_types_by_name['InsertOrReplaceResponse'] = _INSERTORREPLACERESPONSE
DESCRIPTOR.message_types_by_name['FindByIdRequest'] = _FINDBYIDREQUEST
DESCRIPTOR.message_types_by_name['FindByIdResponse'] = _FINDBYIDRESPONSE
DESCRIPTOR.message_types_by_name['CreateTableRequest'] = _CREATETABLEREQUEST
DESCRIPTOR.message_types_by_name['CreateTableResponse'] = _CREATETABLERESPONSE
DESCRIPTOR.message_types_by_name['DeleteTableRequest'] = _DELETETABLEREQUEST
DESCRIPTOR.message_types_by_name['DeleteTableResponse'] = _DELETETABLERESPONSE
DESCRIPTOR.message_types_by_name['TableExistsRequest'] = _TABLEEXISTSREQUEST
DESCRIPTOR.message_types_by_name['TableExistsResponse'] = _TABLEEXISTSRESPONSE
DESCRIPTOR.enum_types_by_name['ErrorCode'] = _ERRORCODE
DESCRIPTOR.enum_types_by_name['PayloadEncoding'] = _PAYLOADENCODING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RpcError = _reflection.GeneratedProtocolMessageType('RpcError', (_message.Message,), dict(
  DESCRIPTOR = _RPCERROR,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.RpcError)
  ))
_sym_db.RegisterMessage(RpcError)

InsertOrReplaceRequest = _reflection.GeneratedProtocolMessageType('InsertOrReplaceRequest', (_message.Message,), dict(
  DESCRIPTOR = _INSERTORREPLACEREQUEST,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.InsertOrReplaceRequest)
  ))
_sym_db.RegisterMessage(InsertOrReplaceRequest)

InsertOrReplaceResponse = _reflection.GeneratedProtocolMessageType('InsertOrReplaceResponse', (_message.Message,), dict(
  DESCRIPTOR = _INSERTORREPLACERESPONSE,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.InsertOrReplaceResponse)
  ))
_sym_db.RegisterMessage(InsertOrReplaceResponse)

FindByIdRequest = _reflection.GeneratedProtocolMessageType('FindByIdRequest', (_message.Message,), dict(
  DESCRIPTOR = _FINDBYIDREQUEST,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.FindByIdRequest)
  ))
_sym_db.RegisterMessage(FindByIdRequest)

FindByIdResponse = _reflection.GeneratedProtocolMessageType('FindByIdResponse', (_message.Message,), dict(
  DESCRIPTOR = _FINDBYIDRESPONSE,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.FindByIdResponse)
  ))
_sym_db.RegisterMessage(FindByIdResponse)

CreateTableRequest = _reflection.GeneratedProtocolMessageType('CreateTableRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATETABLEREQUEST,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.CreateTableRequest)
  ))
_sym_db.RegisterMessage(CreateTableRequest)

CreateTableResponse = _reflection.GeneratedProtocolMessageType('CreateTableResponse', (_message.Message,), dict(
  DESCRIPTOR = _CREATETABLERESPONSE,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.CreateTableResponse)
  ))
_sym_db.RegisterMessage(CreateTableResponse)

DeleteTableRequest = _reflection.GeneratedProtocolMessageType('DeleteTableRequest', (_message.Message,), dict(
  DESCRIPTOR = _DELETETABLEREQUEST,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.DeleteTableRequest)
  ))
_sym_db.RegisterMessage(DeleteTableRequest)

DeleteTableResponse = _reflection.GeneratedProtocolMessageType('DeleteTableResponse', (_message.Message,), dict(
  DESCRIPTOR = _DELETETABLERESPONSE,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.DeleteTableResponse)
  ))
_sym_db.RegisterMessage(DeleteTableResponse)

TableExistsRequest = _reflection.GeneratedProtocolMessageType('TableExistsRequest', (_message.Message,), dict(
  DESCRIPTOR = _TABLEEXISTSREQUEST,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.TableExistsRequest)
  ))
_sym_db.RegisterMessage(TableExistsRequest)

TableExistsResponse = _reflection.GeneratedProtocolMessageType('TableExistsResponse', (_message.Message,), dict(
  DESCRIPTOR = _TABLEEXISTSRESPONSE,
  __module__ = 'maprdb_server_pb2'
  # @@protoc_insertion_point(class_scope:com.mapr.maprdb.grpc.TableExistsResponse)
  ))
_sym_db.RegisterMessage(TableExistsResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\032com.mapr.maprdb.proto.grpcP\001'))

_MAPRDBSERVER = _descriptor.ServiceDescriptor(
  name='MapRDbServer',
  full_name='com.mapr.maprdb.grpc.MapRDbServer',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=1244,
  serialized_end=1771,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateTable',
    full_name='com.mapr.maprdb.grpc.MapRDbServer.CreateTable',
    index=0,
    containing_service=None,
    input_type=_CREATETABLEREQUEST,
    output_type=_CREATETABLERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteTable',
    full_name='com.mapr.maprdb.grpc.MapRDbServer.DeleteTable',
    index=1,
    containing_service=None,
    input_type=_DELETETABLEREQUEST,
    output_type=_DELETETABLERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='TableExists',
    full_name='com.mapr.maprdb.grpc.MapRDbServer.TableExists',
    index=2,
    containing_service=None,
    input_type=_TABLEEXISTSREQUEST,
    output_type=_TABLEEXISTSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='InsertOrReplace',
    full_name='com.mapr.maprdb.grpc.MapRDbServer.InsertOrReplace',
    index=3,
    containing_service=None,
    input_type=_INSERTORREPLACEREQUEST,
    output_type=_INSERTORREPLACERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FindById',
    full_name='com.mapr.maprdb.grpc.MapRDbServer.FindById',
    index=4,
    containing_service=None,
    input_type=_FINDBYIDREQUEST,
    output_type=_FINDBYIDRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MAPRDBSERVER)

DESCRIPTOR.services_by_name['MapRDbServer'] = _MAPRDBSERVER

# @@protoc_insertion_point(module_scope)