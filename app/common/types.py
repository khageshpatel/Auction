import enum

class AuctionStatus(enum.Enum):
    WAITING = "WAITING"
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"
    REVOKED = "REVOKED"