from enum import Enum


class GetHostPoolResponseLoadBalancerType(str, Enum):
    BREADTH_FIRST = "BreadthFirst"
    DEPTH_FIRST = "DepthFirst"

    def __str__(self) -> str:
        return str(self.value)
