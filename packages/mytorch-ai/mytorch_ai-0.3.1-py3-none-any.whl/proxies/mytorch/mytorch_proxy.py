###############################################################################
# Copyright (c) 2024 MyTorch Systems Inc. All rights reserved.
###############################################################################

"""
This proxy provides a proxy for the MyTorchService gRPC service.
It allows the client to call specified torch operations on the server via gRPC.
"""

from connection_utils.server_connection import ServerConnection, wrap_with_error_handler
from gRPC_impl.mytorch import mytorch_pb2_grpc, mytorch_pb2
from gRPC_impl import shared_msg_types_pb2
from torch.Tensor import Tensor
from utils.logger import Logger
from utils import data_transform_utils
import json

from proxies.base_proxy import BaseProxy

class MyTorchProxy (BaseProxy):

    def __init__(self):
        self.channel = ServerConnection.get_active_connection()
        self.stub = mytorch_pb2_grpc.MyTorchServiceStub(self.channel)
        self.logger = Logger.get_logger()


    # OLD rand() - this works, but the new rand() uses generic_call instead.
    #@wrap_with_error_handler
    #def rand(self, sizes: list) -> Tensor:
    #    self.logger.debug(f"randn: shape={sizes}")
    #    request = shared_msg_types_pb2.TensorShape()
    #    request.shape.extend([val for val in sizes])
    #    response: shared_msg_types_pb2.GrpcTensor = self.stub.rand(request)
    #    return Tensor(response.uuid, response.shape, response.dtype)

    @wrap_with_error_handler
    def rand(self, *size: int):
        """Example usage of generic_call for a specific function."""
        uuid, shape, dtype = self.generic_call("torch", "rand", *size)
        return Tensor(uuid, shape, dtype)
    
    @wrap_with_error_handler
    def randn(self, sizes: list) -> Tensor:
        self.logger.debug(f"randn: shape={sizes}")
        request = shared_msg_types_pb2.TensorShape()
        request.shape.extend([val for val in sizes])
        response: shared_msg_types_pb2.GrpcTensor = self.stub.randn(request)
        return Tensor(response.uuid, response.shape, response.dtype)

    @wrap_with_error_handler
    def zeros(self, *size: int):
        uuid, shape, dtype = self.generic_call("torch", "zeros", *size)
        return Tensor(uuid, shape, dtype)
    
    @wrap_with_error_handler
    def from_numpy(self, np_array) -> Tensor:
        request = data_transform_utils.serialize_numpy_array(np_array)
        response: shared_msg_types_pb2.GrpcTensor = self.stub.from_numpy(request)
        tensor = Tensor(response.uuid, response.shape, response.dtype)
        tensor._retrieved_data = np_array # since we already have the data, we don't need to fetch it again
        return tensor

    @wrap_with_error_handler
    def max(self, tensor: Tensor, dim: int) -> tuple[Tensor, Tensor]:
        request = shared_msg_types_pb2.TensorIDAndDim(tensor_uuid=tensor.uuid, dim=dim)
        response: shared_msg_types_pb2.TwoGrpcTensors = self.stub.max(request)
        max_value = Tensor(response.tensor1.uuid, response.tensor1.shape, response.tensor1.dtype)
        max_indices = Tensor(response.tensor2.uuid, response.tensor2.shape, response.tensor2.dtype)
        return max_value, max_indices

    @wrap_with_error_handler
    def arange(self, start, end, step) -> Tensor:
        request = mytorch_pb2.ARangeRequest(start=start, end=end, step=step)
        response_tensor: shared_msg_types_pb2.GrpcTensor = self.stub.arange(request)
        return Tensor(response_tensor.uuid, response_tensor.shape, response_tensor.dtype)

    @wrap_with_error_handler
    def meshgrid(self, tensor_uuids, indexing) -> tuple:
        request = shared_msg_types_pb2.TensorIDsAndDim()
        request.tensor_uuids.extend(tensor_uuids)
        request.dim = indexing
        response: shared_msg_types_pb2.MultipleGrpcTensors = self.stub.meshgrid(request)
        tensors = [Tensor(tensor.uuid, tensor.shape, tensor.dtype) for tensor in response.tensors]
        return tuple(tensors)

    @wrap_with_error_handler
    def reshape(self, tensor: Tensor, shape: tuple) -> Tensor:
        request = shared_msg_types_pb2.ReshapeRequest(tensor_uuid=tensor.uuid, shape=shape)
        response: shared_msg_types_pb2.GrpcTensor = self.stub.reshape(request)
        return Tensor(response.uuid, response.shape, response.dtype)

    @wrap_with_error_handler
    def cat(self, tensors: list, dim: int) -> Tensor:
        request = shared_msg_types_pb2.TensorIDsAndDim()
        request.tensor_uuids.extend([tensor.uuid for tensor in tensors])
        request.dim = dim
        response: shared_msg_types_pb2.GrpcTensor = self.stub.cat(request)
        return Tensor(response.uuid, response.shape, response.dtype)

    @wrap_with_error_handler
    def argmax(self, tensor: Tensor, dim: int, keepdim: bool) -> Tensor:
        request = mytorch_pb2.ArgMaxRequest(tensor_uuid=tensor.uuid, dim=dim, keepdim=keepdim)
        response: shared_msg_types_pb2.GrpcTensor = self.stub.argmax(request)
        return Tensor(response.uuid, response.shape, response.dtype)

    #@wrap_with_error_handler
    #def matmul(self, tensor1: Tensor, tensor2: Tensor) -> Tensor:
    #    request = shared_msg_types_pb2.TwoTensorIDs()
    #    request.tensor1_uuid = tensor1.uuid
    #    request.tensor2_uuid = tensor2.uuid
    #    response: shared_msg_types_pb2.GrpcTensor = self.stub.matmul(request)
    #    return Tensor(response.uuid, response.shape, response.dtype)

    @wrap_with_error_handler
    def matmul(self, tensor1: Tensor, tensor2: Tensor) -> Tensor:
        """Example usage of generic_call for a specific function."""
        uuid, shape, dtype = self.generic_call("torch", "matmul", tensor1.uuid, tensor2.uuid)
        return Tensor(uuid, shape, dtype)
    
    @wrap_with_error_handler
    def load(self, file_path: str) -> dict:
        self.logger.error("load: Not implemented")
        return {}

    @wrap_with_error_handler
    def save(self, file_path: str, state_dict: dict):
        self.logger.error("save: Not implemented")
        return None

    @wrap_with_error_handler
    def allclose(self, input: Tensor, other: Tensor, rtol: float = 1e-05, atol: float = 1e-08, equal_nan: bool = False) -> bool:
        request = mytorch_pb2.AllCloseRequest(tensor1_uuid=input.uuid, tensor2_uuid=other.uuid, rtol=rtol, atol=atol, equal_nan=equal_nan)
        response = self.stub.allclose(request)
        return response.value

    @wrap_with_error_handler
    def unsqueeze(self, tensor: Tensor, dim: int) -> Tensor:
        request = shared_msg_types_pb2.TensorIDAndDim(tensor_uuid=tensor.uuid, dim=dim)
        response: shared_msg_types_pb2.GrpcTensor = self.stub.unsqueeze(request)
        return Tensor(response.uuid, response.shape, response.dtype)

    def repeat_interleave(self, tensor: Tensor, repeats: int, dim: int) -> Tensor:
        request = mytorch_pb2.RepeatInterleaveRequest(tensor_uuid=tensor.uuid, repeats=repeats, dim=dim)
        response: shared_msg_types_pb2.GrpcTensor = self.stub.repeat_interleave(request)
        return Tensor(response.uuid, response.shape, response.dtype)


    ### CACHEQ methods:

    @wrap_with_error_handler
    def scaffolding_server_get_timing_statistics(self, run_id: str) -> str:
        request = shared_msg_types_pb2.StringValue()
        request.value = run_id
        return self.stub.scaffolding_server_get_timing_statistics(request) 
    
    @wrap_with_error_handler
    def scaffolding_server_initialize_timing_statistics(self, run_id: str):
        request = shared_msg_types_pb2.StringValue()
        request.value = run_id
        self.stub.scaffolding_server_initialize_timing_statistics(request)
