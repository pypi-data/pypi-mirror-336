import functools
import logging
import os
import traceback

import grpc
from grpc._channel import _InactiveRpcError

from grpc_registry_protos.grand_central.permissions_svc.permissions_pb2 import CheckPermissionRequest
from grpc_registry_protos.grand_central.permissions_svc.permissions_pb2_grpc import (PermissionServiceStub)
from keven_core.exceptions.communications import CannotContactPermissionService
from keven_core.permissions.abstracts.permission_checker import PermissionChecker


class GRPCPermissionChecker(PermissionChecker):
    """
    This communicates with the Permissions Microservice.  It verifies whether
    as user has access to a resource of whether they have a specific permission
    """

    def __init__(self, service="permission-service:80"):
        server = os.getenv("GRPC_PERMISSIONS_SERVICE") or service

        self.channel = grpc.insecure_channel(server)
        self.stub = PermissionServiceStub(self.channel)

    @functools.lru_cache(maxsize=128)
    def check_permission(
        self,
        person_id,
        acting_as_role_id,
        permission_requested: str,
        resource_id,
    ) -> bool:

        if person_id == "System":
            return True

        request = CheckPermissionRequest()
        request.person_id = person_id
        if acting_as_role_id:
            request.acting_as_role_id = acting_as_role_id
        request.permission_requested = permission_requested
        if resource_id:
            request.resource_id = resource_id
        try:
            response = self.stub.check_permission(request)
        except _InactiveRpcError:
            logging.error(traceback.format_exc())
            raise CannotContactPermissionService()
        return response.is_permission_granted

    def get_resources_by_permission_name(self, name) -> list:
        pass

