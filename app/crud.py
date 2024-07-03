from sqlalchemy.orm import Session

from . import auth, models, schemas


def get_user_id(db: Session, user_id: int):
    """
    Retrieve a user from the database by username.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


# Service CRUD operations
def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def get_services(db: Session, skip: int = 0, limit: int = 10):
    services = (
        db.query(models.Service)
        .order_by(models.Service.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return services


def create_service(db: Session, service: schemas.ServiceCreate) -> models.Service:
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, service_id: int, service: schemas.ServiceCreate):
    db_service = (
        db.query(models.Service).filter(models.Service.id == service_id).first()
    )
    if db_service:
        for key, value in service.dict().items():
            setattr(db_service, key, value)
        db.commit()
        db.refresh(db_service)
    return db_service


def delete_service(db: Session, service_id: int):
    db_service = (
        db.query(models.Service).filter(models.Service.id == service_id).first()
    )
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service


# Portfolio CRUD operations
def get_portfolio(db: Session, portfolio_id: int):
    return (
        db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    )


def get_portfolios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Portfolio).offset(skip).limit(limit).all()


def create_portfolio(
    db: Session, portfolio: schemas.PortfolioCreate
) -> models.Portfolio:
    db_portfolio = models.Portfolio(**portfolio.dict())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def update_portfolio(
    db: Session, portfolio_id: int, portfolio_update: schemas.PortfolioUpdate
) -> models.Portfolio:
    db_portfolio = (
        db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    )
    if not db_portfolio:
        return None

    update_data = portfolio_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_portfolio, key, value)

    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def delete_portfolio(db: Session, portfolio_id: int) -> bool:
    db_portfolio = (
        db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    )
    if db_portfolio is None:
        return False
    db.delete(db_portfolio)
    db.commit()
    return True


# Testimonial CRUD operations
def get_testimonial(db: Session, testimonial_id: int):
    return (
        db.query(models.Testimonial)
        .filter(models.Testimonial.id == testimonial_id)
        .first()
    )


def get_testimonials(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Testimonial).offset(skip).limit(limit).all()


def create_testimonial(
    db: Session, testimonial: schemas.TestimonialCreate
) -> models.Testimonial:
    db_testimonial = models.Testimonial(**testimonial.dict())
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


def update_testimonial(
    db: Session, testimonial_id: int, testimonial: schemas.TestimonialCreate
):
    db_testimonial = (
        db.query(models.Testimonial)
        .filter(models.Testimonial.id == testimonial_id)
        .first()
    )
    if db_testimonial:
        for key, value in testimonial.dict().items():
            setattr(db_testimonial, key, value)
        db.commit()
        db.refresh(db_testimonial)
    return db_testimonial


def delete_testimonial(db: Session, testimonial_id: int):
    db_testimonial = (
        db.query(models.Testimonial)
        .filter(models.Testimonial.id == testimonial_id)
        .first()
    )
    if db_testimonial:
        db.delete(db_testimonial)
        db.commit()
    return db_testimonial


# Contact CRUD operations
def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: schemas.ContactCreate):
    db_contact = (
        db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    )
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = (
        db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    )
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def get_user(db: Session, username: str):
    """
    Retrieve a user from the database by username.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.
    """
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.
    """
    return db.query(models.User).filter(models.User.username == username).first()
