from mapr.ojai.exceptions.GRPCError import GRPCError


class InvalidArgumentError(GRPCError):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message
