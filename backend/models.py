from sqlalchemy import Column, Integer, String, Float, Date

from database import Base


class Vehicle(Base):

    __tablename__ = "vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    registration_number = Column(
        String,
        unique=True,
        nullable=False
    )

    vehicle_name = Column(
        String,
        nullable=False
    )

    vehicle_type = Column(
        String,
        nullable=False
    )

    max_load_capacity = Column(
        Float,
        nullable=False
    )

    odometer = Column(
        Float,
        default=0
    )

    acquisition_cost = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        default="Available"
    )

class Driver(Base):

    __tablename__ = "drivers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    license_number = Column(
        String,
        unique=True,
        nullable=False
    )

    license_category = Column(
        String,
        nullable=False
    )

    license_expiry_date = Column(
        Date,
        nullable=False
    )

    contact_number = Column(
        String,
        nullable=False
    )

    safety_score = Column(
        Float,
        default=100
    )

    status = Column(
        String,
        default="Available"
    )
class Trip(Base):

    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        nullable=False
    )

    driver_id = Column(
        Integer,
        nullable=False
    )

    origin = Column(
        String,
        nullable=False
    )

    destination = Column(
        String,
        nullable=False
    )

    cargo_weight = Column(
        Float,
        nullable=False
    )

    trip_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String,
        default="Draft"
    )