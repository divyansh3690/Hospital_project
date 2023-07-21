from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
from router import auth, doctors, patients

from router.auth import get_user_exception, get_current_user
import model
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

class patient_payment(BaseModel):
    id: int
    name: str
    payment_status: int
    order_id:str
    amount:int

    # email_id: str
    class Config:
        orm_mode = True

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


model.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)



templates = Jinja2Templates(directory="templates")


@app.get("/payment_gateway", response_class=HTMLResponse,tags=["patients"])
async def read_item(request: Request, order_ID:str,db:Session=Depends(get_db)):
    patient = db.query(model.Patients).filter(order_ID == model.Patients.order_id).first()
        #
        # if not patient:
        #     return get_notfound_exception()

    return templates.TemplateResponse("index.html", {"request": request, "amount": patient.amount,"order_id":order_ID,"name":patient.name,})



@app.get("/")
async def hello():
    return {"This is just backend part of the project. Please type '/docs' to the url to see the endpoint at OpenAPI. "}
#
# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})
def get_notfound_exception():
    raise HTTPException(status_code=404,
                        detail="Entry not found")
