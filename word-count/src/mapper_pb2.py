# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapper.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmapper.proto\x12\tmapReduce\"\x1e\n\nMapRequest\x12\x10\n\x08reducers\x18\x06 \x01(\x05\"\x1d\n\x0bMapResponse\x12\x0e\n\x06status\x18\x02 \x01(\t2@\n\x06Mapper\x12\x36\n\x03map\x12\x15.mapReduce.MapRequest\x1a\x16.mapReduce.MapResponse\"\x00\x42\x1f\n\nmap-reduceB\tMapReduceP\x01\xa2\x02\x03\x44SCb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapper_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\nmap-reduceB\tMapReduceP\001\242\002\003DSC'
  _MAPREQUEST._serialized_start=27
  _MAPREQUEST._serialized_end=57
  _MAPRESPONSE._serialized_start=59
  _MAPRESPONSE._serialized_end=88
  _MAPPER._serialized_start=90
  _MAPPER._serialized_end=154
# @@protoc_insertion_point(module_scope)