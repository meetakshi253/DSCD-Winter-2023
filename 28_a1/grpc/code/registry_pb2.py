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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eregistry.proto\x12\x07\x64iscord\"=\n\rServerAddress\x12\x12\n\nServerName\x18\x01 \x01(\t\x12\n\n\x02IP\x18\x02 \x01(\t\x12\x0c\n\x04Port\x18\x03 \x01(\x05\"\x10\n\x0e\x45nquireServers\"\x1c\n\nLiveServer\x12\x0e\n\x06Server\x18\x04 \x01(\t\"(\n\x16RegistryResponseStatus\x12\x0e\n\x06status\x18\x05 \x01(\t2\x94\x01\n\x08Registry\x12\x45\n\x08Register\x12\x16.discord.ServerAddress\x1a\x1f.discord.RegistryResponseStatus\"\x00\x12\x41\n\rGetServerList\x12\x17.discord.EnquireServers\x1a\x13.discord.LiveServer\"\x00\x30\x01\x42\x1f\n\x07\x64iscordB\x0c\x44iscordProtoP\x01\xa2\x02\x03\x44SCb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'registry_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\007discordB\014DiscordProtoP\001\242\002\003DSC'
  _SERVERADDRESS._serialized_start=27
  _SERVERADDRESS._serialized_end=88
  _ENQUIRESERVERS._serialized_start=90
  _ENQUIRESERVERS._serialized_end=106
  _LIVESERVER._serialized_start=108
  _LIVESERVER._serialized_end=136
  _REGISTRYRESPONSESTATUS._serialized_start=138
  _REGISTRYRESPONSESTATUS._serialized_end=178
  _REGISTRY._serialized_start=181
  _REGISTRY._serialized_end=329
# @@protoc_insertion_point(module_scope)
