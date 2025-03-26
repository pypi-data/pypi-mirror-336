from typing_extensions import deprecated
from tmo import TmoClient


@deprecated(
    "AoaClient is deprecated, please use TmoClient instead.",
    category=DeprecationWarning,
)
class AoaClient(TmoClient):
    pass
