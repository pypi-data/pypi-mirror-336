# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from gRPC_impl.mytorchvision.datasets import datasets_pb2 as mytorchvision_dot_datasets_dot_datasets__pb2

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
        + f' but the generated code in mytorchvision/datasets/datasets_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DatasetsServiceStub(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateImageFolderOnServer = channel.unary_unary(
                '/mytorchvision.DatasetsService/CreateImageFolderOnServer',
                request_serializer=mytorchvision_dot_datasets_dot_datasets__pb2.CreateImageFolderRequest.SerializeToString,
                response_deserializer=mytorchvision_dot_datasets_dot_datasets__pb2.GrpcImageFolder.FromString,
                _registered_method=True)
        self.CreateCIFAR10onServer = channel.unary_unary(
                '/mytorchvision.DatasetsService/CreateCIFAR10onServer',
                request_serializer=mytorchvision_dot_datasets_dot_datasets__pb2.CreateCIFAR10Request.SerializeToString,
                response_deserializer=mytorchvision_dot_datasets_dot_datasets__pb2.GrpcCIFAR10.FromString,
                _registered_method=True)


class DatasetsServiceServicer(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    def CreateImageFolderOnServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateCIFAR10onServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatasetsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateImageFolderOnServer': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateImageFolderOnServer,
                    request_deserializer=mytorchvision_dot_datasets_dot_datasets__pb2.CreateImageFolderRequest.FromString,
                    response_serializer=mytorchvision_dot_datasets_dot_datasets__pb2.GrpcImageFolder.SerializeToString,
            ),
            'CreateCIFAR10onServer': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCIFAR10onServer,
                    request_deserializer=mytorchvision_dot_datasets_dot_datasets__pb2.CreateCIFAR10Request.FromString,
                    response_serializer=mytorchvision_dot_datasets_dot_datasets__pb2.GrpcCIFAR10.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mytorchvision.DatasetsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mytorchvision.DatasetsService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DatasetsService(object):
    """/////////////////////////////////////////////////////////////////////////////////
    Service definition
    /////////////////////////////////////////////////////////////////////////////////
    """

    @staticmethod
    def CreateImageFolderOnServer(request,
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
            '/mytorchvision.DatasetsService/CreateImageFolderOnServer',
            mytorchvision_dot_datasets_dot_datasets__pb2.CreateImageFolderRequest.SerializeToString,
            mytorchvision_dot_datasets_dot_datasets__pb2.GrpcImageFolder.FromString,
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
    def CreateCIFAR10onServer(request,
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
            '/mytorchvision.DatasetsService/CreateCIFAR10onServer',
            mytorchvision_dot_datasets_dot_datasets__pb2.CreateCIFAR10Request.SerializeToString,
            mytorchvision_dot_datasets_dot_datasets__pb2.GrpcCIFAR10.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
