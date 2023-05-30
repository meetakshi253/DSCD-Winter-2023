# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import mapper_pb2 as mapper__pb2


class MapperStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.map = channel.unary_unary(
                '/mapReduce.Mapper/map',
                request_serializer=mapper__pb2.MapRequest.SerializeToString,
                response_deserializer=mapper__pb2.MapResponse.FromString,
                )


class MapperServicer(object):
    """Missing associated documentation comment in .proto file."""

    def map(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MapperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'map': grpc.unary_unary_rpc_method_handler(
                    servicer.map,
                    request_deserializer=mapper__pb2.MapRequest.FromString,
                    response_serializer=mapper__pb2.MapResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mapReduce.Mapper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Mapper(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def map(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mapReduce.Mapper/map',
            mapper__pb2.MapRequest.SerializeToString,
            mapper__pb2.MapResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
