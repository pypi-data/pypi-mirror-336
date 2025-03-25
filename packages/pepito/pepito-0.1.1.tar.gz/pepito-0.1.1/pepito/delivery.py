from pydantic import BaseModel


class Delivery(BaseModel):
    id: int = 1
    is_: int = 1
    element_number: int
    labels: str = "-No-Label-"
    pattern: str = ""


class IrnDelivery(Delivery):
    pattern: str = ".*IRN=([0-9]{1,6}).*"


class DcpDelivery(Delivery):
    pattern: str = ".*DCP=([0-9]{1,6}).*"


class AciDelivery(Delivery):
    pattern: str = ".*ACI=([0-9]{1,6}).*"
