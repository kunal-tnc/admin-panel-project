from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class ServiceBase(BaseModel):
    """
    Base model for defining the basic structure of a service.
    """

    name: str
    description: Optional[str] = None


class ServiceCreate(BaseModel):
    """
    Model for creating a new service.
    """

    name: str
    description: str


class Service(ServiceBase):
    """
    Represents a service entity with its unique identifier.
    """

    id: int

    class Config:
        orm_mode = True


class ServiceUpdate(BaseModel):
    """
    Pydantic model for updating an existing service.
    """

    name: str
    description: str


# Pydantic model for output serialization (response data)
class ServiceResponse(BaseModel):
    """
    Pydantic model for serializing service data for response.
    """

    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


# Pydantic models
class PortfolioBase(BaseModel):
    """
    Base model for defining the basic structure of a portfolio entry.
    """

    project_name: str
    client_name: str
    date: date
    skills: str
    description_1: Optional[str] = None
    description_2: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    """
    Model for creating a new portfolio entry.
    Inherits attributes from PortfolioBase.
    """

    pass


class PortfolioUpdate(PortfolioBase):
    """
    Model for updating an existing portfolio entry.
    Inherits attributes from PortfolioBase.
    """

    pass


class Portfolio(PortfolioBase):
    """
    Represents a portfolio entry with a unique identifier.
    """

    id: int

    class Config:
        orm_mode = True


class TestimonialCreate(BaseModel):
    """
    Represents a testimonial creation request schema.
    """

    client_name: str
    message: str
    client_designation: str
    client_company: str
    date: date
    client_image: Optional[str] = None


class Testimonial(BaseModel):
    """
    Represents a testimonial response schema.
    """

    id: int
    client_name: str
    message: str
    client_designation: str
    client_company: str
    date: date
    client_image: Optional[str] = None

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    """
    Base schema for contact information.
    """

    name: str
    email: EmailStr
    phone: str
    message: str


class ContactCreate(ContactBase):
    """
    Schema for creating a new contact entry.
    """

    pass


class Contact(ContactBase):
    """
    Schema for a contact entry with ID for response.
    """

    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """
    Base schema for user information.
    """

    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """

    password: str


class User(UserBase):
    """
    Schema for a user with additional attributes for response.
    """

    id: int
    disabled: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """
    Schema for user login credentials.
    """

    username: str
    password: str
