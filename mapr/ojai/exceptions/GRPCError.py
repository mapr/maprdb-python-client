from grpc import RpcError


class GRPCError(RpcError):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message
