# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mytorch_neuronx/mytorch_neuronx.proto
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
    'mytorch_neuronx/mytorch_neuronx.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%mytorch_neuronx/mytorch_neuronx.proto\x12\x0fmytorch_neuronx\"=\n\x0cTraceRequest\x12\x12\n\nmodel_uuid\x18\x01 \x01(\t\x12\x19\n\x11tensor_uuid_tuple\x18\x02 \x03(\t\"#\n\rTraceResponse\x12\x12\n\nmodel_uuid\x18\x01 \x01(\t2a\n\x15\x43qtorchNeuronxService\x12H\n\x05trace\x12\x1d.mytorch_neuronx.TraceRequest\x1a\x1e.mytorch_neuronx.TraceResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mytorch_neuronx.mytorch_neuronx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRACEREQUEST']._serialized_start=58
  _globals['_TRACEREQUEST']._serialized_end=119
  _globals['_TRACERESPONSE']._serialized_start=121
  _globals['_TRACERESPONSE']._serialized_end=156
  _globals['_CQTORCHNEURONXSERVICE']._serialized_start=158
  _globals['_CQTORCHNEURONXSERVICE']._serialized_end=255
# @@protoc_insertion_point(module_scope)
