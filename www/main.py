from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models
import os
from passlib.hash import bcrypt
from fastapi.responses import RedirectResponse
from fastapi import Form
from datetime import datetime, time, timedelta, date
from typing import List
from fastapi import HTTPException

app = FastAPI()



# Подключаем стат файлы и шаблоныыыыыыыыыы ---------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")



#  ЗАвисимость получения сессии бд --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        

# Определние всех специализаций -----------------------------------------------------------


def spec_to_specialization(spec):
    mapping = {
        "androlog": "Андролог",
        "akusher-ginekolog": "Акушер-гинеколог",
        "gastroenterolog": "Гастроэнтеролог",
        "ginekolog": "Гинеколог",
        "dermatolog": "Дерматолог",
        "dietolog": "Диетолог",
        "allergolog-immunolog": "Иммунолог",
        "kardiolog": "Кардиолог",
        "kosmetolog": "Косметолог",
        "mammolog": "Маммолог",
        "manualiniy-terapevt": "Мануальный терапевт",
        "nevrolog": "Невролог",
        "onkolog": "Онколог",
        "ortoped": "Ортопед",
        "otolaringolog": "Отоларинголог",
        "oftalmolog": "Офтальмолог",
        "proktolog": "Проктолог",
        "psikhoterapeft": "Психотерапевт",
        "revmatolog": "Ревматолог",
        "rentgen": "Рентгенолог",
        "terapeft": "Терапевт",
        "travmatolog-ortoped": "Травматолог-ортопед",
        "urolog": "Уролог",
        "urolog-androlog": "Уролог-андролог",
        "uzi": "УЗИ",
        "khirurg": "Хирург",
        "endokrinolog": "Эндокринолог"
    }

    return mapping.get(spec.lower(), spec.capitalize())




# Фу-я для проверки авторизацимииииииииииииииииииииииии------------------------------------------------------


def is_authenticated(request):
    return request.cookies.get("user_id") is not None



@app.get("/direction/{spec}.html")

def read_direction(spec: str, request: Request, db: Session = Depends(get_db)):

    specialization = spec_to_specialization(spec)

    print(f"Searching for specialization: {specialization}")  # Вывордка отлкадки

    doctors = db.query(models.Doctor).filter(
        func.lower(models.Doctor.specialization) == specialization.lower()
    ).all()

    print(f"Found doctors: {doctors}")  # Выводка отладки 

    return templates.TemplateResponse(f"direction/{spec}.html", {"request": request, "doctors": doctors, "auth": is_authenticated(request)})




@app.get("/")


def read_index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request, "auth": is_authenticated(request)})



@app.get("/profile/register")

def register_form(request: Request):
    return templates.TemplateResponse("profile/register.html", {"request": request, "auth": is_authenticated(request)})



@app.post("/profile/register")

def register_user(request: Request, db: Session = Depends(get_db),
                  username: str = Form(...), email: str = Form(...), password: str = Form(...),
                  first_name: str = Form(...), last_name: str = Form(...), phone: str = Form(...), dms: str = Form(...)):
    
    # ПРоВЕРКА НА СУЩЕСТВОВАНИЕ ПОЛЬЗОВАТЕЛЯ _--------------------------------------------------------------------

    user_exists = db.query(models.User).filter((models.User.username == username) | (models.User.email == email)).first()

    if user_exists:
        return templates.TemplateResponse("profile/register.html", {"request": request, "error": "Пользователь с таким именем или email уже существует"})
    hashed_password = bcrypt.hash(password)

    user = models.User(username=username, email=email, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    patient = models.Patient(fname=first_name, lname=last_name, phone=phone, dms=dms, user_id=user.id)

    db.add(patient)
    db.commit()

    return RedirectResponse("/profile/login", status_code=303)


@app.get("/profile/login")

def login_form(request: Request):
    return templates.TemplateResponse("profile/login.html", {"request": request, "auth": is_authenticated(request)})



@app.post("/profile/login")

def login_user(request: Request, db: Session = Depends(get_db),
               username: str = Form(...), password: str = Form(...)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not bcrypt.verify(password, user.password):
        return templates.TemplateResponse("profile/login.html", {"request": request, "error": "Неверный логин или пароль"})
    
    response = RedirectResponse("/profile/me", status_code=303)

    response.set_cookie(key="user_id", value=str(user.id), httponly=True, max_age=60*60*24*30)


    return response





@app.get("/profile/me")

def profile_me(request: Request, db: Session = Depends(get_db)):

    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/profile/login", status_code=303)
    
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()

    patient = db.query(models.Patient).filter(models.Patient.user_id == int(user_id)).first()

    if not user or not patient:

        response = RedirectResponse("/profile/login", status_code=303)
        response.delete_cookie("user_id", path="/")
        return response
    
    appointments = db.query(models.Appointment).filter(
        models.Appointment.patients_id == patient.id
    ).order_by(models.Appointment.date, models.Appointment.time).all()


    return templates.TemplateResponse("profile/profile.html", {"request": request, "user": user, "patient": patient, "appointments": appointments, "auth": True})




@app.get("/profile/logout")

def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user_id", path="/")
    return response




@app.post("/profile/update")

def update_profile(request: Request, db: Session = Depends(get_db),
                  lname: str = Form(...), fname: str = Form(...), phone: str = Form(...), dms: str = Form(...)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/profile/login", status_code=303)
    patient = db.query(models.Patient).filter(models.Patient.user_id == int(user_id)).first()

    if not patient:
        return RedirectResponse("/profile/me", status_code=303)
    
    patient.lname = lname
    patient.fname = fname
    patient.phone = phone
    patient.dms = dms
    db.commit()


    return RedirectResponse("/profile/me", status_code=303)




@app.post("/profile/change-password")

def change_password(request: Request, db: Session = Depends(get_db),
                   old_password: str = Form(...), new_password: str = Form(...), new_password2: str = Form(...)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/profile/login", status_code=303)
    
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    patient = db.query(models.Patient).filter(models.Patient.user_id == int(user_id)).first()

    if not user or not patient:

        return RedirectResponse("/profile/login", status_code=303)
    
    if not bcrypt.verify(old_password, user.password):

        return templates.TemplateResponse("profile/profile.html", {"request": request, "user": user, "patient": patient, "auth": True, "error": "Старый пароль неверен"})
    
    if new_password != new_password2:

        return templates.TemplateResponse("profile/profile.html", {"request": request, "user": user, "patient": patient, "auth": True, "error": "Пароли не совпадают"})
    
    user.password = bcrypt.hash(new_password)

    db.commit()


    return RedirectResponse("/profile/me", status_code=303)



def generate_time_slots(start_time: time = time(9, 0), end_time: time = time(17, 0), slot_minutes: int = 20) -> List[time]:

    slots = []

    current = datetime.combine(date.today(), start_time)

    end = datetime.combine(date.today(), end_time)

    while current < end:
        slots.append(current.time())
        current += timedelta(minutes=slot_minutes)


    return slots



def get_available_slots(doctor_id: int, appointment_date: date, db: Session) -> List[time]:

    all_slots = generate_time_slots()

    booked_appointments = db.query(models.Appointment).filter(
        models.Appointment.doctors_id == doctor_id,
        models.Appointment.date == appointment_date,
        models.Appointment.status == "запланировано"
    ).all()

    booked_times = {app.time for app in booked_appointments}


    return [slot for slot in all_slots if slot not in booked_times]









@app.get("/appointment/book/{doctor_id}")

async def book_appointment_form(

    request: Request,
    doctor_id: int,
    appointment_date: str = None,
    db: Session = Depends(get_db)

):
    # ИНФА ДОКТОРОВЙ ----------------------------------------------------------
    
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    

    
    # АНАЛзы даты или использование сегоднея --------------------------------------------------------------

    try:
        selected_date = datetime.strptime(appointment_date, "%Y-%m-%d").date() if appointment_date else date.today()

    except ValueError:
        selected_date = date.today()




    
    # ПОЛУЧКА ДОступных слотов-------------------------------------------------------------

    available_slots = get_available_slots(doctor_id, selected_date, db)
    
    return templates.TemplateResponse(

        "appointment_booking.html",

        {
            "request": request,
            "doctor": doctor,
            "selected_date": selected_date,
            "available_slots": available_slots,
            "auth": request.cookies.get("user_id") is not None
        }
    )





@app.post("/appointment/book/{doctor_id}")


async def book_appointment(
    request: Request,
    doctor_id: int,
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    db: Session = Depends(get_db)
):
    

    user_id = request.cookies.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Please login to book an appointment")
    
    patient = db.query(models.Patient).filter(models.Patient.user_id == user_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    try:
        date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(appointment_time, "%H:%M").time()

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date or time format")
    
    available_slots = get_available_slots(doctor_id, date_obj, db)

    if time_obj not in available_slots:
        raise HTTPException(status_code=400, detail="This time slot is no longer available")
    

    appointment = models.Appointment(

        patients_id=patient.id,
        doctors_id=doctor_id,
        date=date_obj,
        time=time_obj,
        status="запланировано"

    )

    db.add(appointment)
    db.commit()


    return RedirectResponse(url="/profile/appointments", status_code=303)





@app.get("/profile/appointments")


async def user_appointments(

    request: Request,
    db: Session = Depends(get_db)

):
    
    return RedirectResponse(url="/profile/me", status_code=303)






@app.post("/appointment/cancel/{appointment_id}")


async def cancel_appointment(

    request: Request,
    appointment_id: int,
    db: Session = Depends(get_db)

):
    

    user_id = request.cookies.get("user_id")


    if not user_id:
        raise HTTPException(status_code=401, detail="Please login to cancel an appointment")
    

    patient = db.query(models.Patient).filter(models.Patient.user_id == user_id).first()


    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    appointment = db.query(models.Appointment).filter(

        models.Appointment.id == appointment_id,
        models.Appointment.patients_id == patient.id

    ).first()


    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = "отменена"

    db.commit()

    
    return RedirectResponse(url="/profile/me", status_code=303) 




































