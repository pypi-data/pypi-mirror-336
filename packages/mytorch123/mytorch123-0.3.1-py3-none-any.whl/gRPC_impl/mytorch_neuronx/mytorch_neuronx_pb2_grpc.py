# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from gRPC_impl.mytorch_neuronx import mytorch_neuronx_pb2 as mytorch__neuronx_dot_mytorch__neuronx__pb2

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
        + f' but the generated code in mytorch_neuronx/mytorch_neuronx_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class CqtorchNeuronxServiceStub(object):
    """/////////////////////////////////////////////
    The MyTorch API / service definition
    /////////////////////////////////////////////
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.trace = channel.unary_unary(
                '/mytorch_neuronx.CqtorchNeuronxService/trace',
                request_serializer=mytorch__neuronx_dot_mytorch__neuronx__pb2.TraceRequest.SerializeToString,
                response_deserializer=mytorch__neuronx_dot_mytorch__neuronx__pb2.TraceResponse.FromString,
                _registered_method=True)


class CqtorchNeuronxServiceServicer(object):
    """/////////////////////////////////////////////
    The MyTorch API / service definition
    /////////////////////////////////////////////
    """

    def trace(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CqtorchNeuronxServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'trace': grpc.unary_unary_rpc_method_handler(
                    servicer.trace,
                    request_deserializer=mytorch__neuronx_dot_mytorch__neuronx__pb2.TraceRequest.FromString,
                    response_serializer=mytorch__neuronx_dot_mytorch__neuronx__pb2.TraceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mytorch_neuronx.CqtorchNeuronxService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mytorch_neuronx.CqtorchNeuronxService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CqtorchNeuronxService(object):
    """/////////////////////////////////////////////
    The MyTorch API / service definition
    /////////////////////////////////////////////
    """

    @staticmethod
    def trace(request,
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
            '/mytorch_neuronx.CqtorchNeuronxService/trace',
            mytorch__neuronx_dot_mytorch__neuronx__pb2.TraceRequest.SerializeToString,
            mytorch__neuronx_dot_mytorch__neuronx__pb2.TraceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
