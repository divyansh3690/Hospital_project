from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from .auth import get_current_user, get_user_exception
import model
from database import engine, SessionLocal

router = FastAPI()

model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/doctors",
    responses={404: {"description": "Not found"}}
)


class ui_Doctors(BaseModel):
    name: str
    specialization: str

    class Config: {
        "user_demo": {
            "name": "XYZ",
            "specialization": "abc"
        }
    }



class patient_response(BaseModel):
    name: str
    age: int
    disease: str
    room_id: int

    class Config:
        orm_mode = True



class doctor_response(BaseModel):
    id:int
    name: str
    specialization: str

    class Config:
        orm_mode = True


class patient_schema(patient_response):
    doctor: List[doctor_response]

class doctor_schema(doctor_response):
    patient: List[patient_response]



@router.get("/", tags=["doctors"], response_model=List[doctor_schema])
async def get_all_doctors(db: Session = Depends(get_db)):
    doctor = db.query(model.Doctors).options(joinedload(model.Doctors.patient)).all()
    return doctor


@router.post("/", tags=["doctors"])
async def add_new_doctor(doctor: ui_Doctors, db: Session = Depends(get_db), adm: dict = Depends(get_current_user)):
    if not adm:
        return get_user_exception()

    doctor_model = model.Doctors()
    doctor_model.name = doctor.name
    doctor_model.specialization = doctor.specialization

    db.add(doctor_model)
    db.commit()

    return successful_response(201)


@router.put("/", tags=["doctors"])
async def edit_doctor_details(id: int, doctor: ui_Doctors, adm: dict = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    if not adm:
        return get_user_exception()
    req_doc = db.query(model.Doctors).filter(id == model.Doctors.id).first()
    if not req_doc:
        return get_postnotfound_exception()
    req_doc.name = doctor.name
    req_doc.specialization = doctor.specialization
    db.commit()

    return successful_response(201)


@router.delete("/", tags=["doctors"])
async def delete_patient_details(id: int, db: Session = Depends(get_db), adm: dict = Depends(get_current_user)):
    if not adm:
        return get_user_exception()
    req_post = db.query(model.Doctors).filter(id == model.Doctors.id).first()
    if not req_post:
        return get_postnotfound_exception()
    db.query(model.Doctors).filter(id == model.Doctors.id).delete()
    db.commit()

    return successful_response(201)


def get_postnotfound_exception():
    HTTPException(status_code=201,
                  detail="Post not found")


def successful_response(status_code):
    return {
        "status_response": status_code,
        "details": "Successful"
    }


























































