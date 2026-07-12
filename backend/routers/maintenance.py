from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post("/")
def create_maintenance(
    maintenance: schemas.MaintenanceCreate,
    db: Session = Depends(get_db)
):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == maintenance.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    if vehicle.status == "On Trip":
        raise HTTPException(
            status_code=400,
            detail="Vehicle on trip cannot be sent for maintenance"
        )

    new_maintenance = models.Maintenance(
        vehicle_id=maintenance.vehicle_id,
        issue=maintenance.issue,
        service_date=maintenance.service_date,
        cost=maintenance.cost,
        status="Scheduled"
    )

    vehicle.status = "Maintenance"

    db.add(new_maintenance)
    db.commit()
    db.refresh(new_maintenance)

    return {
        "message": "Maintenance scheduled successfully",
        "maintenance": new_maintenance
    }


@router.get("/")
def get_all_maintenance(
    db: Session = Depends(get_db)
):

    maintenance_records = db.query(
        models.Maintenance
    ).all()

    return {
        "total_records": len(maintenance_records),
        "maintenance": maintenance_records
    }


@router.get("/{maintenance_id}")
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    maintenance = db.query(models.Maintenance).filter(
        models.Maintenance.id == maintenance_id
    ).first()

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    return maintenance


@router.put("/{maintenance_id}/complete")
def complete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    maintenance = db.query(models.Maintenance).filter(
        models.Maintenance.id == maintenance_id
    ).first()

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    if maintenance.status == "Completed":
        raise HTTPException(
            status_code=400,
            detail="Maintenance already completed"
        )

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == maintenance.vehicle_id
    ).first()

    maintenance.status = "Completed"
    vehicle.status = "Available"

    db.commit()
    db.refresh(maintenance)

    return {
        "message": "Maintenance completed successfully",
        "maintenance": maintenance
    }


@router.delete("/{maintenance_id}")
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    maintenance = db.query(models.Maintenance).filter(
        models.Maintenance.id == maintenance_id
    ).first()

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    db.delete(maintenance)
    db.commit()

    return {
        "message": "Maintenance record deleted successfully"
    }