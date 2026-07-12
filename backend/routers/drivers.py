from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


@router.post("/")
def create_driver(
    driver: schemas.DriverCreate,
    db: Session = Depends(get_db)
):

    existing_driver = db.query(models.Driver).filter(
        models.Driver.license_number == driver.license_number
    ).first()

    if existing_driver:
        raise HTTPException(
            status_code=400,
            detail="Driver license number already exists"
        )

    new_driver = models.Driver(
        name=driver.name,
        license_number=driver.license_number,
        license_category=driver.license_category,
        license_expiry_date=driver.license_expiry_date,
        contact_number=driver.contact_number,
        safety_score=driver.safety_score,
        status="Available"
    )

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)

    return {
        "message": "Driver created successfully",
        "driver": new_driver
    }
@router.get("/")
def get_all_drivers(
    db: Session = Depends(get_db)
):

    drivers = db.query(models.Driver).all()

    return {
        "total_drivers": len(drivers),
        "drivers": drivers
    }
@router.get("/{driver_id}")
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver
@router.put("/{driver_id}")
def update_driver(
    driver_id: int,
    driver_data: schemas.DriverUpdate,
    db: Session = Depends(get_db)
):

    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    duplicate_driver = db.query(models.Driver).filter(
        models.Driver.license_number == driver_data.license_number,
        models.Driver.id != driver_id
    ).first()

    if duplicate_driver:
        raise HTTPException(
            status_code=400,
            detail="Driver license number already exists"
        )

    driver.name = driver_data.name
    driver.license_number = driver_data.license_number
    driver.license_category = driver_data.license_category
    driver.license_expiry_date = driver_data.license_expiry_date
    driver.contact_number = driver_data.contact_number
    driver.safety_score = driver_data.safety_score
    driver.status = driver_data.status

    db.commit()
    db.refresh(driver)

    return {
        "message": "Driver updated successfully",
        "driver": driver
    }


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    db.delete(driver)
    db.commit()

    return {
        "message": "Driver deleted successfully"
    }