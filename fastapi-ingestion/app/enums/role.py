import enum


class RoleName(enum.Enum):
    admin = "admin"
    passenger = "passenger"
    driver = "driver"


class RoleTitle(enum.Enum):
    admin = "Admin"
    passenger = "Passenger"
    driver = "Driver"