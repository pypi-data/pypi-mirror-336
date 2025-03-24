# Abstract base class for proxy objects, to implement the generic_call approach.
import json
import numpy as np

from connection_utils.server_connection import wrap_with_error_handler
from gRPC_impl import shared_msg_types_pb2
from utils.logger import Logger
from gRPC_impl.mytorch import mytorch_pb2_grpc

class BaseProxy():
    def __init__(self):
        self.logger = Logger.get_logger()

    @wrap_with_error_handler
    def generic_call(self, module: str, method: str, *args):
        """Handles a generic JSON request and returns a dynamic response."""
        method_json = json.dumps({
            "context": module,
            "method": method,
            "args": args
        })

        #self.logger.info(f"Generic Call Request: {method_json}")

        # Create a gRPC request
        request = shared_msg_types_pb2.JsonRequest()
        request.json_payload = method_json

        #self.stub = tensor_pb2_grpc.TensorServiceStub(self.channel)
        # Use the generic stub !!!!!!
        stub = mytorch_pb2_grpc.MyTorchServiceStub(self.channel)

        response: shared_msg_types_pb2.JsonResponse = stub.generic_call(request)

        # Decode JSON response
        result = json.loads(response.json_payload)

        # Handle different types of responses dynamically
        if "error" in result:
            raise RuntimeError(f"Server Error: {result['error']}")

        return self._deserialize_response(result)

    def _deserialize_response(self, response):
        """Converts JSON response back into the appropriate Python type."""
        if response["type"] == "tensor":
 #           return Tensor(response["uuid"], response["shape"], response["dtype"])
            return response["uuid"], response["shape"], response["dtype"]
        elif response["type"] == "scalar":
            return response["value"]
        elif response["type"] == "list":
            return response["value"]
        elif response["type"] == "bool":
            return bool(response["value"])
        else:
            raise ValueError(f"Unknown response type: {response['type']}")

