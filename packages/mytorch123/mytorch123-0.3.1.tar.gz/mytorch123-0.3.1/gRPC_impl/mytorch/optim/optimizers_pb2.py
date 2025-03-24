# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mytorch/optim/optimizers.proto
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
    'mytorch/optim/optimizers.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gRPC_impl import shared_msg_types_pb2 as shared__msg__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1emytorch/optim/optimizers.proto\x12\x07mytorch\x1a\x16shared_msg_types.proto\"\\\n\x19\x43reateSGDOptimizerRequest\x12\x16\n\x0egenerator_uuid\x18\x01 \x01(\t\x12\x15\n\rlearning_rate\x18\x02 \x01(\x02\x12\x10\n\x08momentum\x18\x03 \x01(\x02*|\n\rOptimizerType\x12\x07\n\x03SGD\x10\x00\x12\x08\n\x04\x41\x44\x41M\x10\x01\x12\x0b\n\x07\x41\x44\x41GRAD\x10\x02\x12\x0b\n\x07RMSPROP\x10\x03\x12\n\n\x06\x41\x44\x41MAX\x10\x04\x12\t\n\x05\x41\x44\x41MW\x10\x05\x12\x0b\n\x07\x41\x44\x41MAXW\x10\x06\x12\x0c\n\x08\x41\x44\x41GRADW\x10\x07\x12\x0c\n\x08RMSPROPW\x10\x08\x32\xa8\x01\n\x10OptimizerService\x12\x46\n\x12\x43reateSGDOptimizer\x12\".mytorch.CreateSGDOptimizerRequest\x1a\x0c.shared.UUID\x12\'\n\x08ZeroGrad\x12\x0c.shared.UUID\x1a\r.shared.Empty\x12#\n\x04Step\x12\x0c.shared.UUID\x1a\r.shared.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mytorch.optim.optimizers_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OPTIMIZERTYPE']._serialized_start=161
  _globals['_OPTIMIZERTYPE']._serialized_end=285
  _globals['_CREATESGDOPTIMIZERREQUEST']._serialized_start=67
  _globals['_CREATESGDOPTIMIZERREQUEST']._serialized_end=159
  _globals['_OPTIMIZERSERVICE']._serialized_start=288
  _globals['_OPTIMIZERSERVICE']._serialized_end=456
# @@protoc_insertion_point(module_scope)
