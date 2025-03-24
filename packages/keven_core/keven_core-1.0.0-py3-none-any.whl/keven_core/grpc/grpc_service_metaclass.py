from types import FunctionType
import grpc
import logging
from functools import wraps
from google.protobuf import empty_pb2 as pbEmpty


class GRPCServiceMeta(type):
    def __new__(cls, class_name, bases, class_dict):
        return cls.process_methods(bases, class_dict, class_name)

    @staticmethod
    def wrapper(method):
        @wraps(method)
        def wrapped(self, request, context):
            logging.info(f"gRPC Request: {method.__name__} - Payload: {request}")
            try:
                response = method(self, request, context)
                logging.info(f"gRPC Response: {response}")
                return response
            except Exception as e:
                logging.error(f"gRPC Error in {method.__name__}: {str(e)}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return pbEmpty.Empty()

        return wrapped

    @classmethod
    def process_methods(cls, bases, class_dict, class_name):
        new_class_dict = {
            "commit": lambda self: None,
            "rollback": lambda self: None,
            "remove": lambda self: None,
        }
        for attribute_name, attribute in class_dict.items():
            if (
                isinstance(attribute, FunctionType)
                and attribute_name[0].isupper()
            ):
                attribute = GRPCServiceMeta.wrapper(attribute)
            new_class_dict[attribute_name] = attribute

        res_class = type.__new__(cls, class_name, bases, new_class_dict)
        return res_class
