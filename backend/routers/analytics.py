from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    total_vehicles = db.query(models.Vehicle).count()

    available_vehicles = db.query(models.Vehicle).filter(
        models.Vehicle.status == "Available"
    ).count()

    vehicles_on_trip = db.query(models.Vehicle).filter(
        models.Vehicle.status == "On Trip"
    ).count()

    vehicles_in_maintenance = db.query(models.Vehicle).filter(
        models.Vehicle.status == "Maintenance"
    ).count()

    total_drivers = db.query(models.Driver).count()

    available_drivers = db.query(models.Driver).filter(
        models.Driver.status == "Available"
    ).count()

    total_trips = db.query(models.Trip).count()

    draft_trips = db.query(models.Trip).filter(
        models.Trip.status == "Draft"
    ).count()

    dispatched_trips = db.query(models.Trip).filter(
        models.Trip.status == "Dispatched"
    ).count()

    completed_trips = db.query(models.Trip).filter(
        models.Trip.status == "Completed"
    ).count()

    total_maintenance = db.query(
        models.Maintenance
    ).count()

    return {
        "fleet": {
            "total": total_vehicles,
            "available": available_vehicles,
            "on_trip": vehicles_on_trip,
            "maintenance": vehicles_in_maintenance
        },
        "drivers": {
            "total": total_drivers,
            "available": available_drivers
        },
        "trips": {
            "total": total_trips,
            "draft": draft_trips,
            "dispatched": dispatched_trips,
            "completed": completed_trips
        },
        "maintenance": {
            "total": total_maintenance
        }
    }