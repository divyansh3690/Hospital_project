from typing import List
from datetime import timedelta, datetime
from pytz import timezone
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .auth import get_current_user, get_user_exception
import model
from database import Base, engine, SessionLocal
from .doctors import doctor_response

# email
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from starlette.responses import JSONResponse
import razorpay
from dotenv import dotenv_values

# credentials


RAZORPAY_KEY_ID = "rzp_test_4hU5VZrYmhTnH5"
RAZORPAY_KEY_SECRET = "1QJfKp13xvW1ZnRQICNZvGyR"


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME="divyanshnumb@gmail.com",
    MAIL_PASSWORD="jbomvyfqjcxtixrz",
    MAIL_FROM="divyanshnumb@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

router = APIRouter()

model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/patients",
    responses={404: {"description": "Not found"}}
)


class ui_patient(BaseModel):
    name: str
    age: int
    disease: str
    room_id: int
    # email_id: str
    payment_status: int = Field(gt=-1, lt=2)


class patient_response(BaseModel):
    id: int
    name: str
    age: int
    disease: str
    room_id: int
    payment_status: int
    order_id:str
    # email_id: str

    class Config:
        orm_mode = True



class patient_payment(BaseModel):
    id: int
    name: str
    payment_status: int
    order_id:str
    amount:int

    # email_id: str
    class Config:
        orm_mode = True

class patient_schema(patient_response):
    doctor: List[doctor_response]


class CreateOrder(BaseModel):
    amount: int
    currency: str = "INR"


class VerifyOrder(BaseModel):
    order_id: str


@router.get("/", tags=["patients"], response_model=List[patient_schema])
async def get_all_patients(db: Session = Depends(get_db)):
    patient = db.query(model.Patients) \
        .options(joinedload(model.Patients.doctor)) \
        .all()

    return patient


@router.get("/{patient_id}", tags=["patients"], response_model=patient_schema)
async def get_patient_byid(patient_id: int, db: Session = Depends(get_db)):
    req_post = db.query(model.Patients) \
        .options(joinedload(model.Patients.doctor)) \
        .filter(patient_id == model.Patients.id).all()
    if not req_post:
        return get_notfound_exception()
    return req_post


@router.post("/", tags=["patients"])
async def add_new_patient(email: EmailSchema, patient: ui_patient, db: Session = Depends(get_db),
                          adm: dict = Depends(get_current_user)):
    if not adm:
        return get_user_exception
    patient_model = model.Patients()
    patient_model.name = patient.name
    patient_model.age = patient.age
    patient_model.disease = patient.disease
    patient_model.room_id = patient.room_id
    patient_model.payment_status = patient.payment_status
    # converted list to string because database's email_id takes string and send_mail function takes list .
    patient_model.email_id = listToString(email.dict().get("email"))

    db.add(patient_model)
    db.commit()
    await send_mail(email, patient.name, patient.room_id)
    return successful_response(201)


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


async def send_mail(email: EmailSchema, name: str, room_no: int):
    # appointment is set to two hour late of booking time
    appointment_time = datetime.utcnow() + timedelta(hours=5, minutes=30) + timedelta(hours=2)

    html = f"""
    <p>Dear {name},</p>
  
  <p>We are delighted to confirm your upcoming appointment at Midland Hospital. 
  Your health and well-being are of utmost importance to us, and we appreciate the opportunity
   to provide you with exceptional care. Please review the details of your appointment below:. 
 
  
  <h3>Appointment Details:</h3>
  <ul>
    <li><strong>Patient Name:</strong> {name}</li>
    
    <li><strong>Appointment Date:</strong> {datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')}</li>
    <li><strong>Appointment Time:</strong> {appointment_time.strftime('%H-%M')}</li>
    <li><strong>Room Number:</strong> {room_no}</li>
  </ul>
  
  <p>Please ensure that you arrive at least 15 minutes before your scheduled appointment time to 
  complete any necessary paperwork and check-in procedures. If you anticipate any delays or if you 
  are unable to keep the appointment, kindly notify us at your earliest convenience so that we may 
  accommodate other patients who may be in need of our services.</p>
  <p>We look forward to seeing you.
   Thank you once again for choosing us for your healthcare needs.</p>
  
  <p>Best regards,<br><b>MIDLAND HOSPITAL</b><br>(8299821096)</b></p>
    """

    message = MessageSchema(
        subject=f"Confirmation of Appointment Details -{name}",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Success": "Email sent"}


@router.put("/", tags=["patients"])
async def edit_patient_details(email: EmailSchema, id: int, patient: ui_patient, db: Session = Depends(get_db),
                               adm: dict = Depends(get_current_user)):
    if not adm:
        return get_user_exception()

    req_post = db.query(model.Patients).filter(id == model.Patients.id).first()
    if not req_post:
        return get_notfound_exception()
    req_post.name = patient.name
    req_post.age = patient.age
    req_post.disease = patient.disease
    req_post.room_id = patient.room_id
    req_post.payment_status = patient.payment_status
    req_post.email_id = listToString(email.dict().get("email"))

    db.commit()
    await send_mail(email, patient.name, patient.room_id)
    return successful_response(201)


@router.delete("/", tags=["patients"])
async def delete_patient_details(id: int, db: Session = Depends(get_db), adm: dict = Depends(get_current_user)):
    if not adm:
        return get_user_exception()
    req_post = db.query(model.Patients).filter(id == model.Patients.id).first()
    if not req_post:
        return get_notfound_exception()
    db.query(model.Patients).filter(id == model.Patients.id).delete()
    db.query(model.link).filter(id == model.link.patient_id).delete()

    db.commit()

    return successful_response(201)

@router.post("/doc", tags=["patients"])
async def assign_patients(patient_id: int, doc_id: int, db: Session = Depends(get_db),
                          adm: dict = Depends(get_current_user)):
    if not adm:
        return get_user_exception()
    req_patient = db.query(model.Patients).filter(patient_id == model.Patients.id).first()
    if not req_patient:
        return get_notfound_exception()

    link_value = model.link()
    link_value.patient_id = patient_id
    link_value.doctors_id = doc_id

    db.add(link_value)
    db.commit()

    return successful_response(201)


def get_notfound_exception():
    raise HTTPException(status_code=404,
                        detail="Entry not found")


def successful_response(status_code):
    return {
        "status_response": status_code,
        "details": "Successful"
    }


client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@router.post("/create_order",response_model=patient_payment,tags=["patients"])
async def create_order(input: CreateOrder, id: int, db: Session = Depends(get_db)):
    patient = db.query(model.Patients).filter(id == model.Patients.id).first()
    if not patient:
        return get_user_exception

    payment = client.order.create({'amount': input.amount*100, 'currency': input.currency, 'payment_capture': '1'})

    patient.order_id=payment.get("id")
    patient.amount=payment.get("amount")

    db.commit()
    return db.query(model.Patients).filter(id == model.Patients.id).first()


@router.get("/verify_order/{input}",tags=["patients"])
async def verify_order(input: str,db:Session=Depends(get_db)):
    try:
        order = client.order.fetch(input)

        if order['status'] == 'paid':
            # Payment successful, update your database or do other tasks here
            patient = db.query(model.Patients).filter(input == model.Patients.order_id).first()
            patient.payment_status=1
            db.commit()
            return JSONResponse(status_code=200, content={'message': 'Payment successful'})
        else:
            # Payment failed, handle the failure here
            return JSONResponse(status_code=500, content={'message': 'Payment failed'})
    except Exception as e:
        # Handle any exceptions here
        return JSONResponse(status_code=500, content={'message': str(e)})

