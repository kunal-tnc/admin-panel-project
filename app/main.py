import bcrypt
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import crud, models, schemas
from .database import engine, get_db

# Create all the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.post("/register/", response_model=schemas.User)
def register_user(
    user: schemas.UserCreate, db: Session = Depends(get_db), request: Request = None
):
    """
    Register a new user in the database.
    """
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    created_user = crud.create_user(db=db, user=user)
    if created_user:
        return RedirectResponse(url="/", status_code=200)

    raise HTTPException(status_code=500, detail="Failed to create user")


@app.get("/register/", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Serve the user registration page.
    """
    return templates.TemplateResponse("register.html", {"request": request})




def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


@app.post("/")
async def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Handle user login and authentication.
    """
    user = crud.get_user_by_username(db, user_login.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
    }


@app.get("/api/user", response_model=schemas.User)
def get_user(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Handle get user by user_id.
    """
    user = crud.get_user_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"username": user.username})


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/index", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/service", response_class=HTMLResponse)
async def service_page(request: Request):
    return templates.TemplateResponse("apps-new-project.html", {"request": request})


# Service endpoints
@app.post("/services/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    """
    Handle create the services.
    """
    service_data = crud.create_service(db=db, service=service)
    return schemas.Service.from_orm(service_data)


@app.get("/services/{service_id}", response_model=schemas.Service)
def read_service(request: Request, service_id: int, db: Session = Depends(get_db)):
    """
    Handle get service by service_id.
    """
    db_service = crud.get_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return templates.TemplateResponse(
        "apps-service.html", {"request": request, "service": db_service}
    )


@app.get("/service_table/", response_class=HTMLResponse)
async def service_table_view(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Handle get service list.
    """
    services = crud.get_services(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "service_table.html", {"request": request, "services": services}
    )


@app.put("/services/{service_id}", response_model=schemas.Service)
def update_service(
    service_id: int, service: schemas.ServiceCreate, db: Session = Depends(get_db)
):
    """
    Handle update service by service_id.
    """
    db_service = crud.get_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    updated_service = crud.update_service(db, service_id=service_id, service=service)
    return updated_service


@app.delete("/services/{service_id}", response_model=schemas.Service)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    """
    Handle delete service by service_id.
    """
    db_service = crud.delete_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


# Portfolio endpoints


@app.get("/portfolios", response_class=HTMLResponse)
async def portfolios_page(request: Request):
    return templates.TemplateResponse("apps-new-portfolio.html", {"request": request})


@app.post("/portfolios/", response_model=schemas.Portfolio)
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    """
    Handle create portfolios.
    """
    portfolio_data = crud.create_portfolio(db=db, portfolio=portfolio)
    return schemas.Portfolio.from_orm(portfolio_data)


@app.get("/portfolios/{portfolio_id}", response_model=schemas.Portfolio)
def read_portfolio(request: Request, portfolio_id: int, db: Session = Depends(get_db)):
    """
    Handle get portfolios by portfolio_id.
    """
    db_portfolio = crud.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return templates.TemplateResponse(
        "update_portfolio.html", {"request": request, "db_portfolio": db_portfolio}
    )


@app.get("/portfolios_table/", response_class=HTMLResponse)
async def portfolios_table_view(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Handle get portfolios list.
    """
    Portfolios = crud.get_portfolios(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "portfolio_table.html", {"request": request, "Portfolios": Portfolios}
    )


@app.put("/portfolios/{portfolio_id}", response_model=schemas.Portfolio)
def update_portfolio(
    portfolio_id: int,
    portfolio_update: schemas.PortfolioUpdate,
    db: Session = Depends(get_db),
):
    """
    Handle update portfolios by portfolio_id.
    """
    portfolio_data = crud.update_portfolio(
        db=db, portfolio_id=portfolio_id, portfolio_update=portfolio_update
    )
    if portfolio_data is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return schemas.Portfolio.from_orm(portfolio_data)


@app.delete("/portfolios/{portfolio_id}", response_model=None, status_code=204)
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """
    Handle delete portfolios by portfolio_id.
    """
    result = crud.delete_portfolio(db=db, portfolio_id=portfolio_id)
    if not result:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return None


# Testimonial endpoints
@app.get("/testimonials", response_class=HTMLResponse)
async def testimonials_page(request: Request):
    return templates.TemplateResponse("testimonials_new.html", {"request": request})


@app.post("/testimonials/", response_model=schemas.Testimonial)
def create_testimonial(
    testimonial: schemas.TestimonialCreate, db: Session = Depends(get_db)
):
    """
    Handle create testimonials.
    """
    testimonial_data = crud.create_testimonial(db=db, testimonial=testimonial)
    return schemas.Testimonial.from_orm(testimonial_data)


@app.get("/testimonials/{testimonial_id}", response_model=schemas.Testimonial)
def read_testimonial(
    request: Request, testimonial_id: int, db: Session = Depends(get_db)
):
    """
    Handle get testimonials by testimonial_id.
    """
    db_testimonial = crud.get_testimonial(db, testimonial_id=testimonial_id)
    if db_testimonial is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return templates.TemplateResponse(
        "update_testimonials.html", {"request": request, "testimonial": db_testimonial}
    )


@app.get("/testimonials_table/", response_class=HTMLResponse)
def read_testimonials(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Handle create testimonials.
    """
    testimonials = crud.get_testimonials(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "testimonials_table.html", {"request": request, "Testimonials": testimonials}
    )


@app.put("/testimonials/{testimonial_id}", response_model=schemas.Testimonial)
def update_testimonial(
    testimonial_id: int,
    testimonial: schemas.TestimonialCreate,
    db: Session = Depends(get_db),
):
    """
    Handle update testimonials by testimonial_id.
    """
    db_testimonial = crud.update_testimonial(
        db, testimonial_id=testimonial_id, testimonial=testimonial
    )
    if db_testimonial is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return schemas.Testimonial.from_orm(db_testimonial)


@app.delete("/testimonials/{testimonial_id}", response_model=None, status_code=204)
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    """
    Handle delete testimonials by testimonial_id.
    """
    db_testimonial = crud.delete_testimonial(db, testimonial_id=testimonial_id)
    if db_testimonial is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return db_testimonial


# Contact endpoints
@app.get("/contacts", response_class=HTMLResponse)
async def contacts_page(request: Request):
    return templates.TemplateResponse("contacts_new.html", {"request": request})


@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """
    Handle create contacts.
    """
    contacts_data = crud.create_contact(db=db, contact=contact)
    return schemas.Contact.from_orm(contacts_data)


@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(request: Request, contact_id: int, db: Session = Depends(get_db)):
    """
    Handle get contacts by contact_id.
    """
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return templates.TemplateResponse(
        "update_contacts.html", {"request": request, "db_contact": db_contact}
    )


@app.get("/contacts_table/", response_class=HTMLResponse)
def read_contacts(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Handle list of contacts.
    """
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "contact_table.html", {"request": request, "contacts": contacts}
    )


@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)
):
    """
    Handle update contacts by contact_id.
    """
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=None, status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Handle delete contacts by contact_id.
    """
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
