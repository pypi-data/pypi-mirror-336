# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from gRPC_impl.mytorch.hub import hub_pb2 as mytorch_dot_hub_dot_hub__pb2

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
        + f' but the generated code in mytorch/hub/hub_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class HubServiceStub(object):
    """/////////////////////////////////////////////
    Services
    /////////////////////////////////////////////
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.loadModel = channel.unary_unary(
                '/mytorch.HubService/loadModel',
                request_serializer=mytorch_dot_hub_dot_hub__pb2.ModelLoadRequest.SerializeToString,
                response_deserializer=mytorch_dot_hub_dot_hub__pb2.ModelLoadResponse.FromString,
                _registered_method=True)


class HubServiceServicer(object):
    """/////////////////////////////////////////////
    Services
    /////////////////////////////////////////////
    """

    def loadModel(self, request, context):
        """example call: torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HubServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'loadModel': grpc.unary_unary_rpc_method_handler(
                    servicer.loadModel,
                    request_deserializer=mytorch_dot_hub_dot_hub__pb2.ModelLoadRequest.FromString,
                    response_serializer=mytorch_dot_hub_dot_hub__pb2.ModelLoadResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mytorch.HubService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mytorch.HubService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class HubService(object):
    """/////////////////////////////////////////////
    Services
    /////////////////////////////////////////////
    """

    @staticmethod
    def loadModel(request,
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
            '/mytorch.HubService/loadModel',
            mytorch_dot_hub_dot_hub__pb2.ModelLoadRequest.SerializeToString,
            mytorch_dot_hub_dot_hub__pb2.ModelLoadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
