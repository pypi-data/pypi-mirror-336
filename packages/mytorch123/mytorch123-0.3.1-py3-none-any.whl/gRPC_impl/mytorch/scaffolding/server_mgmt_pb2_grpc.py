# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from gRPC_impl.mytorch.scaffolding import server_mgmt_pb2 as mytorch_dot_scaffolding_dot_server__mgmt__pb2
from gRPC_impl import shared_msg_types_pb2 as shared__msg__types__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in mytorch/scaffolding/server_mgmt_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ServerMgmtServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.server_status = channel.unary_unary(
                '/mytorch.ServerMgmtService/server_status',
                request_serializer=shared__msg__types__pb2.Empty.SerializeToString,
                response_deserializer=mytorch_dot_scaffolding_dot_server__mgmt__pb2.ServerStatus.FromString,
                _registered_method=True)
        self.client_disconnect = channel.unary_unary(
                '/mytorch.ServerMgmtService/client_disconnect',
                request_serializer=shared__msg__types__pb2.Empty.SerializeToString,
                response_deserializer=shared__msg__types__pb2.Empty.FromString,
                _registered_method=True)
        self.get_server_gpu_stats = channel.unary_unary(
                '/mytorch.ServerMgmtService/get_server_gpu_stats',
                request_serializer=shared__msg__types__pb2.Empty.SerializeToString,
                response_deserializer=mytorch_dot_scaffolding_dot_server__mgmt__pb2.GpuInfoList.FromString,
                _registered_method=True)


class ServerMgmtServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def server_status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def client_disconnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_server_gpu_stats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerMgmtServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'server_status': grpc.unary_unary_rpc_method_handler(
                    servicer.server_status,
                    request_deserializer=shared__msg__types__pb2.Empty.FromString,
                    response_serializer=mytorch_dot_scaffolding_dot_server__mgmt__pb2.ServerStatus.SerializeToString,
            ),
            'client_disconnect': grpc.unary_unary_rpc_method_handler(
                    servicer.client_disconnect,
                    request_deserializer=shared__msg__types__pb2.Empty.FromString,
                    response_serializer=shared__msg__types__pb2.Empty.SerializeToString,
            ),
            'get_server_gpu_stats': grpc.unary_unary_rpc_method_handler(
                    servicer.get_server_gpu_stats,
                    request_deserializer=shared__msg__types__pb2.Empty.FromString,
                    response_serializer=mytorch_dot_scaffolding_dot_server__mgmt__pb2.GpuInfoList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mytorch.ServerMgmtService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mytorch.ServerMgmtService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ServerMgmtService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def server_status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mytorch.ServerMgmtService/server_status',
            shared__msg__types__pb2.Empty.SerializeToString,
            mytorch_dot_scaffolding_dot_server__mgmt__pb2.ServerStatus.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def client_disconnect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mytorch.ServerMgmtService/client_disconnect',
            shared__msg__types__pb2.Empty.SerializeToString,
            shared__msg__types__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get_server_gpu_stats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mytorch.ServerMgmtService/get_server_gpu_stats',
            shared__msg__types__pb2.Empty.SerializeToString,
            mytorch_dot_scaffolding_dot_server__mgmt__pb2.GpuInfoList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
