# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: registry.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eregistry.proto\x12\rprimary_block\")\n\rServerAddress\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"\x10\n\x0e\x45nquireServers2\xa6\x01\n\x08Registry\x12H\n\x08Register\x12\x1c.primary_block.ServerAddress\x1a\x1c.primary_block.ServerAddress\"\x00\x12P\n\rGetServerList\x12\x1d.primary_block.EnquireServers\x1a\x1c.primary_block.ServerAddress\"\x00\x30\x01\x42(\n\x16primary-block-protocolB\x06QuorumP\x01\xa2\x02\x03\x44SCb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'registry_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026primary-block-protocolB\006QuorumP\001\242\002\003DSC'
  _SERVERADDRESS._serialized_start=33
  _SERVERADDRESS._serialized_end=74
  _ENQUIRESERVERS._serialized_start=76
  _ENQUIRESERVERS._serialized_end=92
  _REGISTRY._serialized_start=95
  _REGISTRY._serialized_end=261
# @@protoc_insertion_point(module_scope)