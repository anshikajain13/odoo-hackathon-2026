from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.post("/")
def create_vehicle(
    vehicle: schemas.VehicleCreate,
    db: Session = Depends(get_db)
):

    existing_vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.registration_number == vehicle.registration_number
    ).first()

    if existing_vehicle:
        raise HTTPException(
            status_code=400,
            detail="Vehicle registration number already exists"
        )

    new_vehicle = models.Vehicle(
        registration_number=vehicle.registration_number,
        vehicle_name=vehicle.vehicle_name,
        vehicle_type=vehicle.vehicle_type,
        max_load_capacity=vehicle.max_load_capacity,
        odometer=vehicle.odometer,
        acquisition_cost=vehicle.acquisition_cost,
        status="Available"
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return {
        "message": "Vehicle created successfully",
        "vehicle": new_vehicle
    }
@router.get("/")
def get_all_vehicles(
    db: Session = Depends(get_db)
):

    vehicles = db.query(models.Vehicle).all()

    return {
        "total_vehicles": len(vehicles),
        "vehicles": vehicles
    }
@router.get("/{vehicle_id}")
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle
@router.put("/{vehicle_id}")
def update_vehicle(
    vehicle_id: int,
    vehicle_data: schemas.VehicleUpdate,
    db: Session = Depends(get_db)
):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    duplicate_vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.registration_number == vehicle_data.registration_number,
        models.Vehicle.id != vehicle_id
    ).first()

    if duplicate_vehicle:
        raise HTTPException(
            status_code=400,
            detail="Vehicle registration number already exists"
        )

    vehicle.registration_number = vehicle_data.registration_number
    vehicle.vehicle_name = vehicle_data.vehicle_name
    vehicle.vehicle_type = vehicle_data.vehicle_type
    vehicle.max_load_capacity = vehicle_data.max_load_capacity
    vehicle.odometer = vehicle_data.odometer
    vehicle.acquisition_cost = vehicle_data.acquisition_cost
    vehicle.status = vehicle_data.status

    db.commit()
    db.refresh(vehicle)

    return {
        "message": "Vehicle updated successfully",
        "vehicle": vehicle
    }
@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehicle deleted successfully"
    }