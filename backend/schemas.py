from pydantic import BaseModel


class VehicleCreate(BaseModel):
    registration_number: str
    vehicle_name: str
    vehicle_type: str
    max_load_capacity: float
    odometer: float
    acquisition_cost: float

class VehicleUpdate(BaseModel):
    registration_number: str
    vehicle_name: str
    vehicle_type: str
    max_load_capacity: float
    odometer: float
    acquisition_cost: float
    status: str