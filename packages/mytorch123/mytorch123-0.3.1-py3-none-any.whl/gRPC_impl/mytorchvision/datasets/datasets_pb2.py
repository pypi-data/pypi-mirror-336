# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mytorchvision/datasets/datasets.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'mytorchvision/datasets/datasets.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%mytorchvision/datasets/datasets.proto\x12\rmytorchvision\"U\n\x0fGrpcImageFolder\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x13\n\x0bimage_uuids\x18\x02 \x03(\t\x12\x0e\n\x06labels\x18\x03 \x03(\x05\x12\x0f\n\x07\x63lasses\x18\x04 \x03(\t\"D\n\x0bGrpcCIFAR10\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x16\n\x0e\x64\x61taset_length\x18\x02 \x01(\x05\x12\x0f\n\x07\x63lasses\x18\x03 \x03(\t\"M\n\x18\x43reateImageFolderRequest\x12\x19\n\x11relative_datapath\x18\x01 \x01(\t\x12\x16\n\x0etransform_uuid\x18\x02 \x01(\t\"]\n\x14\x43reateCIFAR10Request\x12\x0c\n\x04root\x18\x01 \x01(\t\x12\r\n\x05train\x18\x02 \x01(\x08\x12\x10\n\x08\x64ownload\x18\x03 \x01(\x08\x12\x16\n\x0etransform_uuid\x18\x04 \x01(\t2\xd1\x01\n\x0f\x44\x61tasetsService\x12\x64\n\x19\x43reateImageFolderOnServer\x12\'.mytorchvision.CreateImageFolderRequest\x1a\x1e.mytorchvision.GrpcImageFolder\x12X\n\x15\x43reateCIFAR10onServer\x12#.mytorchvision.CreateCIFAR10Request\x1a\x1a.mytorchvision.GrpcCIFAR10b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mytorchvision.datasets.datasets_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GRPCIMAGEFOLDER']._serialized_start=56
  _globals['_GRPCIMAGEFOLDER']._serialized_end=141
  _globals['_GRPCCIFAR10']._serialized_start=143
  _globals['_GRPCCIFAR10']._serialized_end=211
  _globals['_CREATEIMAGEFOLDERREQUEST']._serialized_start=213
  _globals['_CREATEIMAGEFOLDERREQUEST']._serialized_end=290
  _globals['_CREATECIFAR10REQUEST']._serialized_start=292
  _globals['_CREATECIFAR10REQUEST']._serialized_end=385
  _globals['_DATASETSSERVICE']._serialized_start=388
  _globals['_DATASETSSERVICE']._serialized_end=597
# @@protoc_insertion_point(module_scope)
