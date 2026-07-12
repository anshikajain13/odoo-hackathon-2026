from pydantic import BaseModel
from datetime import date


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
from datetime import date


class DriverCreate(BaseModel):
    name: str
    license_number: str
    license_category: str
    license_expiry_date: date
    contact_number: str
    safety_score: float = 100
class DriverUpdate(BaseModel):
    name: str
    license_number: str
    license_category: str
    license_expiry_date: date
    contact_number: str
    safety_score: float
    status: str
class TripCreate(BaseModel):
    vehicle_id: int
    driver_id: int
    origin: str
    destination: str
    cargo_weight: float
    trip_date: date


class TripUpdate(BaseModel):
    vehicle_id: int
    driver_id: int
    origin: str
    destination: str
    cargo_weight: float
    trip_date: date
    status: str
class MaintenanceCreate(BaseModel):
    vehicle_id: int
    issue: str
    service_date: date
    cost: float


class MaintenanceUpdate(BaseModel):
    issue: str
    service_date: date
    cost: float
    status: str