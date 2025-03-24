class CommunicationFailure(Exception):
    pass

class Timeout(CommunicationFailure):
    pass


class DeliveryFailure(CommunicationFailure):
    pass


class ReceiveFailure(CommunicationFailure):
    pass

class CannotContactPermissionService(CommunicationFailure):
    pass