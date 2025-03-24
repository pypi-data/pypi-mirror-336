# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from gRPC_impl.mytorch.nn import nn_msg_types_pb2 as mytorch_dot_nn_dot_nn__msg__types__pb2
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
        + f' but the generated code in mytorch/nn/sequential_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SequentialServiceStub(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateSequentialModuleOnServer = channel.unary_unary(
                '/mytorch.SequentialService/CreateSequentialModuleOnServer',
                request_serializer=mytorch_dot_nn_dot_nn__msg__types__pb2.NNLayers.SerializeToString,
                response_deserializer=shared__msg__types__pb2.UUID.FromString,
                _registered_method=True)


class SequentialServiceServicer(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    def CreateSequentialModuleOnServer(self, request, context):
        """create a torch.nn.Sequential module on the server and return its UUID to the client
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SequentialServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateSequentialModuleOnServer': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateSequentialModuleOnServer,
                    request_deserializer=mytorch_dot_nn_dot_nn__msg__types__pb2.NNLayers.FromString,
                    response_serializer=shared__msg__types__pb2.UUID.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mytorch.SequentialService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mytorch.SequentialService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SequentialService(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    @staticmethod
    def CreateSequentialModuleOnServer(request,
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
            '/mytorch.SequentialService/CreateSequentialModuleOnServer',
            mytorch_dot_nn_dot_nn__msg__types__pb2.NNLayers.SerializeToString,
            shared__msg__types__pb2.UUID.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
