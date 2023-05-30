# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import server_pb2 as server__pb2


class ServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/primary_blocking.Server/Read',
                request_serializer=server__pb2.ReadRequest.SerializeToString,
                response_deserializer=server__pb2.ReadResponse.FromString,
                )
        self.Write = channel.unary_unary(
                '/primary_blocking.Server/Write',
                request_serializer=server__pb2.WriteRequest.SerializeToString,
                response_deserializer=server__pb2.WriteResponse.FromString,
                )
        self.Delete = channel.unary_unary(
                '/primary_blocking.Server/Delete',
                request_serializer=server__pb2.DeleteRequest.SerializeToString,
                response_deserializer=server__pb2.DeleteResponse.FromString,
                )
        self.PrimaryWrite = channel.unary_unary(
                '/primary_blocking.Server/PrimaryWrite',
                request_serializer=server__pb2.PrimaryWriteRequest.SerializeToString,
                response_deserializer=server__pb2.WriteResponse.FromString,
                )
        self.PrimaryDelete = channel.unary_unary(
                '/primary_blocking.Server/PrimaryDelete',
                request_serializer=server__pb2.PrimaryDeleteRequest.SerializeToString,
                response_deserializer=server__pb2.DeleteResponse.FromString,
                )
        self.NewJoinee = channel.unary_unary(
                '/primary_blocking.Server/NewJoinee',
                request_serializer=server__pb2.ReplicaAddress.SerializeToString,
                response_deserializer=server__pb2.JoinResponse.FromString,
                )


class ServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PrimaryWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PrimaryDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NewJoinee(self, request, context):
        """only for the primary replica
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=server__pb2.ReadRequest.FromString,
                    response_serializer=server__pb2.ReadResponse.SerializeToString,
            ),
            'Write': grpc.unary_unary_rpc_method_handler(
                    servicer.Write,
                    request_deserializer=server__pb2.WriteRequest.FromString,
                    response_serializer=server__pb2.WriteResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=server__pb2.DeleteRequest.FromString,
                    response_serializer=server__pb2.DeleteResponse.SerializeToString,
            ),
            'PrimaryWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.PrimaryWrite,
                    request_deserializer=server__pb2.PrimaryWriteRequest.FromString,
                    response_serializer=server__pb2.WriteResponse.SerializeToString,
            ),
            'PrimaryDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.PrimaryDelete,
                    request_deserializer=server__pb2.PrimaryDeleteRequest.FromString,
                    response_serializer=server__pb2.DeleteResponse.SerializeToString,
            ),
            'NewJoinee': grpc.unary_unary_rpc_method_handler(
                    servicer.NewJoinee,
                    request_deserializer=server__pb2.ReplicaAddress.FromString,
                    response_serializer=server__pb2.JoinResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'primary_blocking.Server', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Server(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/primary_blocking.Server/Read',
            server__pb2.ReadRequest.SerializeToString,
            server__pb2.ReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Write(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/primary_blocking.Server/Write',
            server__pb2.WriteRequest.SerializeToString,
            server__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/primary_blocking.Server/Delete',
            server__pb2.DeleteRequest.SerializeToString,
            server__pb2.DeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PrimaryWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/primary_blocking.Server/PrimaryWrite',
            server__pb2.PrimaryWriteRequest.SerializeToString,
            server__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PrimaryDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/primary_blocking.Server/PrimaryDelete',
            server__pb2.PrimaryDeleteRequest.SerializeToString,
            server__pb2.DeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NewJoinee(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/primary_blocking.Server/NewJoinee',
            server__pb2.ReplicaAddress.SerializeToString,
            server__pb2.JoinResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
