# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cserver.proto\x12\x10primary_blocking\"*\n\x0eReplicaAddress\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"\x1e\n\x0cJoinResponse\x12\x0e\n\x06status\x18\x02 \x01(\t\"\x1b\n\x0bReadRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"N\n\x0cReadResponse\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\t\";\n\x0cWriteRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\"S\n\x13PrimaryWriteRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\t\">\n\rWriteResponse\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\t\"\x1d\n\rDeleteRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\" \n\x0e\x44\x65leteResponse\x12\x0e\n\x06status\x18\x02 \x01(\t2\xe6\x03\n\x06Server\x12G\n\x04Read\x12\x1d.primary_blocking.ReadRequest\x1a\x1e.primary_blocking.ReadResponse\"\x00\x12J\n\x05Write\x12\x1e.primary_blocking.WriteRequest\x1a\x1f.primary_blocking.WriteResponse\"\x00\x12M\n\x06\x44\x65lete\x12\x1f.primary_blocking.DeleteRequest\x1a .primary_blocking.DeleteResponse\"\x00\x12Q\n\x0cPrimaryWrite\x12\x1e.primary_blocking.WriteRequest\x1a\x1f.primary_blocking.WriteResponse\"\x00\x12T\n\rPrimaryDelete\x12\x1f.primary_blocking.DeleteRequest\x1a .primary_blocking.DeleteResponse\"\x00\x12O\n\tNewJoinee\x12 .primary_blocking.ReplicaAddress\x1a\x1e.primary_blocking.JoinResponse\"\x00\x42+\n\x19primary-blocking-protocolB\x06QuorumP\x01\xa2\x02\x03\x44SCb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031primary-blocking-protocolB\006QuorumP\001\242\002\003DSC'
  _REPLICAADDRESS._serialized_start=34
  _REPLICAADDRESS._serialized_end=76
  _JOINRESPONSE._serialized_start=78
  _JOINRESPONSE._serialized_end=108
  _READREQUEST._serialized_start=110
  _READREQUEST._serialized_end=137
  _READRESPONSE._serialized_start=139
  _READRESPONSE._serialized_end=217
  _WRITEREQUEST._serialized_start=219
  _WRITEREQUEST._serialized_end=278
  _PRIMARYWRITEREQUEST._serialized_start=280
  _PRIMARYWRITEREQUEST._serialized_end=363
  _WRITERESPONSE._serialized_start=365
  _WRITERESPONSE._serialized_end=427
  _DELETEREQUEST._serialized_start=429
  _DELETEREQUEST._serialized_end=458
  _DELETERESPONSE._serialized_start=460
  _DELETERESPONSE._serialized_end=492
  _SERVER._serialized_start=495
  _SERVER._serialized_end=981
# @@protoc_insertion_point(module_scope)