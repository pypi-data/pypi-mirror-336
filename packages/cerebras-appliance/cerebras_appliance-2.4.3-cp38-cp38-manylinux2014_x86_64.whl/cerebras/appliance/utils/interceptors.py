# Copyright 2016-2024 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""gRPC channel interceptors."""

import grpc

from cerebras.appliance.errors import PicklableRpcError


class ExceptionFormattingInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):  # pylint: disable=no-init
    """gRPC interceptor class that replaces pure gRPC error with a custom gRPC exception."""

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercept "Single request, single response" RPC calls."""
        try:
            # Make the RPC call
            return continuation(client_call_details, request)
        except grpc.RpcError as e:
            raise PicklableRpcError.from_grpc_error(e) from None

    def intercept_unary_stream(
        self, continuation, client_call_details, request
    ):
        """Intercept "Single request, streaming response" RPC calls."""
        try:
            yield from continuation(client_call_details, request)
        except grpc.RpcError as e:
            raise PicklableRpcError.from_grpc_error(e) from None

    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        """Intercept "Streaming request, single response" RPC calls."""
        try:
            return continuation(client_call_details, request_iterator)
        except grpc.RpcError as e:
            raise PicklableRpcError.from_grpc_error(e) from None

    def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        """Intercept "Streaming request, streaming response" RPC calls."""
        try:
            yield from continuation(client_call_details, request_iterator)
        except grpc.RpcError as e:
            raise PicklableRpcError.from_grpc_error(e) from None
