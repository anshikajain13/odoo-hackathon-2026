from sqlalchemy import Column, Integer, String, Float

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