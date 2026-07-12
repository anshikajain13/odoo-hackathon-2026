from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

import models
import schemas
from database import get_db


router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


@router.post("/")
def create_trip(
    trip: schemas.TripCreate,
    db: Session = Depends(get_db)
):

    # Check vehicle
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == trip.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    # Check driver
    driver = db.query(models.Driver).filter(
        models.Driver.id == trip.driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    # Capacity validation
    if trip.cargo_weight > vehicle.max_load_capacity:
        raise HTTPException(
            status_code=400,
            detail="Cargo weight exceeds vehicle capacity"
        )

    # Driver licence validation
    if driver.license_expiry_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Driver licence has expired"
        )

    # Vehicle availability
    if vehicle.status != "Available":
        raise HTTPException(
            status_code=400,
            detail="Vehicle is not available"
        )

    # Driver availability
    if driver.status != "Available":
        raise HTTPException(
            status_code=400,
            detail="Driver is not available"
        )

    # Prevent vehicle double booking
    vehicle_trip = db.query(models.Trip).filter(
        models.Trip.vehicle_id == trip.vehicle_id,
        models.Trip.trip_date == trip.trip_date,
        models.Trip.status != "Cancelled"
    ).first()

    if vehicle_trip:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already booked for this date"
        )

    # Prevent driver double booking
    driver_trip = db.query(models.Trip).filter(
        models.Trip.driver_id == trip.driver_id,
        models.Trip.trip_date == trip.trip_date,
        models.Trip.status != "Cancelled"
    ).first()

    if driver_trip:
        raise HTTPException(
            status_code=400,
            detail="Driver already booked for this date"
        )

    new_trip = models.Trip(
        vehicle_id=trip.vehicle_id,
        driver_id=trip.driver_id,
        origin=trip.origin,
        destination=trip.destination,
        cargo_weight=trip.cargo_weight,
        trip_date=trip.trip_date,
        status="Draft"
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {
        "message": "Trip created successfully",
        "trip": new_trip
    }


@router.get("/")
def get_trips(db: Session = Depends(get_db)):

    return db.query(models.Trip).all()


@router.get("/{trip_id}")
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    return trip


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    db.delete(trip)
    db.commit()

    return {
        "message": "Trip deleted successfully"
    }
@router.put("/{trip_id}/dispatch")
def dispatch_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if trip.status != "Draft":
        raise HTTPException(
            status_code=400,
            detail="Only Draft trips can be dispatched"
        )

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(models.Driver).filter(
        models.Driver.id == trip.driver_id
    ).first()

    trip.status = "Dispatched"
    vehicle.status = "On Trip"
    driver.status = "On Trip"

    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip dispatched successfully",
        "trip": trip
    }


@router.put("/{trip_id}/complete")
def complete_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if trip.status != "Dispatched":
        raise HTTPException(
            status_code=400,
            detail="Only dispatched trips can be completed"
        )

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(models.Driver).filter(
        models.Driver.id == trip.driver_id
    ).first()

    trip.status = "Completed"
    vehicle.status = "Available"
    driver.status = "Available"

    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip completed successfully",
        "trip": trip
    }