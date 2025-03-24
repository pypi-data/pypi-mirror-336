###############################################################################
# Copyright (c) 2024 MyTorch Systems Inc. All rights reserved.
###############################################################################

"""
This proxy provides a proxy for the Module gRPC service.
It allows the client to call specified torch.nn.Module operations on the server via gRPC.
"""

from connection_utils.server_connection import ServerConnection, wrap_with_error_handler
from gRPC_impl import shared_msg_types_pb2
from gRPC_impl.mytorch import tensor_pb2_grpc, tensor_pb2
from utils.data_transform_utils import deserialize_tensor
from utils.logger import Logger
import numpy as np
import json

from proxies.base_proxy import BaseProxy
class TensorProxy (BaseProxy):

    # Note that is is NOT used to create a tensor on the server side.
    # There are separate static methods for this.
    @wrap_with_error_handler
    def __init__(self, uuid: str):
        self.channel = ServerConnection.get_active_connection()
        self.stub = tensor_pb2_grpc.TensorServiceStub(self.channel)
        self.logger = Logger.get_logger()
        self.uuid = uuid

    @wrap_with_error_handler
    def get_data(self) -> np.ndarray:
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        response: shared_msg_types_pb2.SerializedTensorData = self.stub.get_data(request)
        deserialized_tensor = deserialize_tensor(response.data, response.shape, response.dtype)
        return deserialized_tensor

    @wrap_with_error_handler
    def backward(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        return self.stub.backward(request)

    @wrap_with_error_handler
    def item(self) -> float:
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        return self.stub.item(request).value

    @wrap_with_error_handler
    def float(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.float(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def long(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.long(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def toCuda(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.to_cuda(request)
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def toCpu(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.to_cpu(request)
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def reshape(self, shape: tuple):
        request = shared_msg_types_pb2.ReshapeRequest(tensor_uuid=self.uuid, shape=shape)
        grpc_tensor = self.stub.reshape(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def get_shape(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.get_shape(request)
        # convert the shape from a repeated field to a tuple
        shape = tuple(grpc_tensor.shape)
        return shape

    @wrap_with_error_handler
    def get_dtype(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.get_dtype(request)
        return grpc_tensor.dtype

    @wrap_with_error_handler
    def equal(self, other_uuid: str):
        if not isinstance(other_uuid, str):
            raise ValueError("other_uuid must be a string")
        if self.uuid == other_uuid:
            return True
        request = shared_msg_types_pb2.TwoTensorIDs(tensor1_uuid=self.uuid, tensor2_uuid=other_uuid)
        grpc_tensor = self.stub.equal(request)
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def add(self, other_uuid: str):
        request = shared_msg_types_pb2.TwoTensorIDs(tensor1_uuid=self.uuid, tensor2_uuid=other_uuid)
        grpc_tensor = self.stub.add(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def sum(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        grpc_tensor = self.stub.sum(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype


    @wrap_with_error_handler
    def sub(self, operand: int):
        return self.generic_call("tensor_method", "sub", self.uuid, operand)
    
    # e.g. tensor[0:2,3:,:5]
    @wrap_with_error_handler
    def slice(self, *slicing_specs):
        slice_request = tensor_pb2.SliceRequest()
        slice_request.tensor_uuid = self.uuid

        for slice_tuple in slicing_specs:  # Iterate over the slicing specifications tuple

            # if only one slice is provided, convert it to a tuple
            if isinstance(slice_tuple, slice):
                slice_tuple = (slice_tuple,)

            # loop over the slices in the slicing specification tuple
            for slice_obj in slice_tuple:
                start = slice_obj.start if slice_obj.start is not None else -1  # -1 means open-ended slice
                stop = slice_obj.stop if slice_obj.stop is not None else -1 # -1 means open-ended slice
                step = slice_obj.step if slice_obj.step is not None else 1 # 1 is the default step
                tensor_slice = tensor_pb2.TensorSlice()
                tensor_slice.start = start
                tensor_slice.stop = stop
                tensor_slice.step = step
                slice_request.slices.append(tensor_slice)

        grpc_tensor = self.stub.slice(slice_request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    # e.g. tensor[0]
    @wrap_with_error_handler
    def index(self, idx: int):
        request = shared_msg_types_pb2.TensorIDAndDim(tensor_uuid=self.uuid, dim=idx)
        grpc_tensor = self.stub.index(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def unsqueeze(self, dim: int):
        request = shared_msg_types_pb2.TensorIDAndDim(tensor_uuid=self.uuid, dim=dim)
        grpc_tensor = self.stub.unsqueeze(request)
        # can't return a mytorch.Tensor here because it would create a circular import
        return grpc_tensor.uuid, grpc_tensor.shape, grpc_tensor.dtype

    @wrap_with_error_handler
    def delete(self):
        request = shared_msg_types_pb2.UUID(uuid=self.uuid)
        self.stub.delete(request)