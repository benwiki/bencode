
from dataclasses import dataclass

from eagxf.typedefs import DcClient, DcUser


@dataclass
class Admin:
    client: DcClient
    users: dict[int, DcUser]