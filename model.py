from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, null
from database import Base

# link = Table('link', Base.metadata,
#              Column('patient_id', ForeignKey('patients.id'), primary_key=True),
#              Column('doctor_id', ForeignKey('doctors.id'), primary_key=True)
#              )


class Patients(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    disease = Column(String)
    email_id=Column(String)
    room_id = Column(Integer)
    payment_status =Column(Integer)
    order_id=Column(String,default="null")
    amount=Column(Integer,default=0)
    doctor = relationship("Doctors", back_populates="patient", secondary="link")


class Doctors(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)
    patient = relationship("Patients", back_populates="doctor", secondary="link")


class Admin(Base):
    __tablename__ = "admin"
    username = Column(String, primary_key=True, index=True)
    hashed_pass = Column(String, index=True)

class link(Base):
    __tablename__ = "link"
    doctors_id = Column(ForeignKey('doctors.id'), primary_key=True)
    patient_id = Column(ForeignKey('patients.id'), primary_key=True)






# Notes
#
# We define the link table using SQLAlchemy’s Table() class (“declarative”), and we define the books and authors tables using
# inheritance (“declarative style”). We could’ve used imperative style only or declarative style only,
# In the junction table, we declared the primary key as the pair of columns (book_id, author_id).
# Because of this, every (book_id, author_id) pair in the table must be unique.
