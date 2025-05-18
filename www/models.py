from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base



Base = declarative_base()



class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(20))
    lname = Column(String(25))
    specialization = Column(String(70))
    title = Column(String(150))
    experience = Column(String(7))
    price = Column(DECIMAL)

    # Можно добавить image_url чтобы не укащывать в html -----------

    appointments = relationship("Appointment", back_populates="doctor")





class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    patient = relationship("Patient", back_populates="user", uselist=False)




class Patient(Base):

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(20))
    lname = Column(String(25))
    phone = Column(String(16))
    dms = Column(String(16))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")



class Appointment(Base):

    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    patients_id = Column(Integer, ForeignKey("patients.id"))
    doctors_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    duration = Column(Integer, default=20)  # минут примема впрача 20
    status = Column(String, default="active")  # Активный или отмененынй 
    
    # СВЯЗИИИИИИИИИИИИИИ-------------------------------------


    patient = relationship("Patient", back_populates="appointments", foreign_keys=[patients_id])
    doctor = relationship("Doctor", back_populates="appointments", foreign_keys=[doctors_id]) 



























    