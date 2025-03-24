# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from gRPC_impl.mytorch.nn import module_pb2 as mytorch_dot_nn_dot_module__pb2
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
        + f' but the generated code in mytorch/nn/module_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ModuleServiceStub(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Forward = channel.unary_unary(
                '/mytorch.ModuleService/Forward',
                request_serializer=mytorch_dot_nn_dot_nn__msg__types__pb2.ForwardPassRequest.SerializeToString,
                response_deserializer=shared__msg__types__pb2.GrpcTensor.FromString,
                _registered_method=True)
        self.CreateModuleOnServer = channel.unary_unary(
                '/mytorch.ModuleService/CreateModuleOnServer',
                request_serializer=shared__msg__types__pb2.Empty.SerializeToString,
                response_deserializer=shared__msg__types__pb2.UUID.FromString,
                _registered_method=True)
        self.GetStateDict = channel.unary_unary(
                '/mytorch.ModuleService/GetStateDict',
                request_serializer=shared__msg__types__pb2.UUID.SerializeToString,
                response_deserializer=mytorch_dot_nn_dot_nn__msg__types__pb2.SerializedStateDict.FromString,
                _registered_method=True)
        self.Eval = channel.unary_unary(
                '/mytorch.ModuleService/Eval',
                request_serializer=shared__msg__types__pb2.UUID.SerializeToString,
                response_deserializer=shared__msg__types__pb2.Empty.FromString,
                _registered_method=True)
        self.ToDevice = channel.unary_unary(
                '/mytorch.ModuleService/ToDevice',
                request_serializer=mytorch_dot_nn_dot_module__pb2.ModuleToDeviceRequest.SerializeToString,
                response_deserializer=shared__msg__types__pb2.Empty.FromString,
                _registered_method=True)
        self.GetParameters = channel.unary_unary(
                '/mytorch.ModuleService/GetParameters',
                request_serializer=shared__msg__types__pb2.UUID.SerializeToString,
                response_deserializer=mytorch_dot_nn_dot_module__pb2.Parameters.FromString,
                _registered_method=True)
        self.half = channel.unary_unary(
                '/mytorch.ModuleService/half',
                request_serializer=mytorch_dot_nn_dot_module__pb2.half_request.SerializeToString,
                response_deserializer=mytorch_dot_nn_dot_module__pb2.half_response.FromString,
                _registered_method=True)
        self.delete = channel.unary_unary(
                '/mytorch.ModuleService/delete',
                request_serializer=shared__msg__types__pb2.UUID.SerializeToString,
                response_deserializer=shared__msg__types__pb2.Empty.FromString,
                _registered_method=True)


class ModuleServiceServicer(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    def Forward(self, request, context):
        """model.forward() or model(x)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateModuleOnServer(self, request, context):
        """torch.nn.Module()
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStateDict(self, request, context):
        """model.state_dict()
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Eval(self, request, context):
        """model.eval()
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ToDevice(self, request, context):
        """model.to(device)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetParameters(self, request, context):
        """model.parameters()
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def half(self, request, context):
        """model.half()
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """removes object from ObjectStorage and deletes it
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ModuleServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Forward': grpc.unary_unary_rpc_method_handler(
                    servicer.Forward,
                    request_deserializer=mytorch_dot_nn_dot_nn__msg__types__pb2.ForwardPassRequest.FromString,
                    response_serializer=shared__msg__types__pb2.GrpcTensor.SerializeToString,
            ),
            'CreateModuleOnServer': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateModuleOnServer,
                    request_deserializer=shared__msg__types__pb2.Empty.FromString,
                    response_serializer=shared__msg__types__pb2.UUID.SerializeToString,
            ),
            'GetStateDict': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStateDict,
                    request_deserializer=shared__msg__types__pb2.UUID.FromString,
                    response_serializer=mytorch_dot_nn_dot_nn__msg__types__pb2.SerializedStateDict.SerializeToString,
            ),
            'Eval': grpc.unary_unary_rpc_method_handler(
                    servicer.Eval,
                    request_deserializer=shared__msg__types__pb2.UUID.FromString,
                    response_serializer=shared__msg__types__pb2.Empty.SerializeToString,
            ),
            'ToDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.ToDevice,
                    request_deserializer=mytorch_dot_nn_dot_module__pb2.ModuleToDeviceRequest.FromString,
                    response_serializer=shared__msg__types__pb2.Empty.SerializeToString,
            ),
            'GetParameters': grpc.unary_unary_rpc_method_handler(
                    servicer.GetParameters,
                    request_deserializer=shared__msg__types__pb2.UUID.FromString,
                    response_serializer=mytorch_dot_nn_dot_module__pb2.Parameters.SerializeToString,
            ),
            'half': grpc.unary_unary_rpc_method_handler(
                    servicer.half,
                    request_deserializer=mytorch_dot_nn_dot_module__pb2.half_request.FromString,
                    response_serializer=mytorch_dot_nn_dot_module__pb2.half_response.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=shared__msg__types__pb2.UUID.FromString,
                    response_serializer=shared__msg__types__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mytorch.ModuleService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mytorch.ModuleService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ModuleService(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    @staticmethod
    def Forward(request,
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
            '/mytorch.ModuleService/Forward',
            mytorch_dot_nn_dot_nn__msg__types__pb2.ForwardPassRequest.SerializeToString,
            shared__msg__types__pb2.GrpcTensor.FromString,
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
    def CreateModuleOnServer(request,
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
            '/mytorch.ModuleService/CreateModuleOnServer',
            shared__msg__types__pb2.Empty.SerializeToString,
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

    @staticmethod
    def GetStateDict(request,
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
            '/mytorch.ModuleService/GetStateDict',
            shared__msg__types__pb2.UUID.SerializeToString,
            mytorch_dot_nn_dot_nn__msg__types__pb2.SerializedStateDict.FromString,
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
    def Eval(request,
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
            '/mytorch.ModuleService/Eval',
            shared__msg__types__pb2.UUID.SerializeToString,
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
    def ToDevice(request,
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
            '/mytorch.ModuleService/ToDevice',
            mytorch_dot_nn_dot_module__pb2.ModuleToDeviceRequest.SerializeToString,
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
    def GetParameters(request,
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
            '/mytorch.ModuleService/GetParameters',
            shared__msg__types__pb2.UUID.SerializeToString,
            mytorch_dot_nn_dot_module__pb2.Parameters.FromString,
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
    def half(request,
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
            '/mytorch.ModuleService/half',
            mytorch_dot_nn_dot_module__pb2.half_request.SerializeToString,
            mytorch_dot_nn_dot_module__pb2.half_response.FromString,
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
    def delete(request,
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
            '/mytorch.ModuleService/delete',
            shared__msg__types__pb2.UUID.SerializeToString,
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
