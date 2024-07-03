from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the application.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)


class Service(Base):
    """
    Represents a service in the application.
    """

    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class Portfolio(Base):
    """
    Represents a portfolio in the application.
    """

    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    skills = Column(String(255), nullable=False)
    description_1 = Column(Text, nullable=True)
    description_2 = Column(Text, nullable=True)


class Testimonial(Base):
    """
    Represents a testimonials in the application.
    """

    __tablename__ = "testimonials"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    client_designation = Column(String(255), nullable=False)
    client_company = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    client_image = Column(String(255), nullable=True)


class Contact(Base):
    """
    Represents a contacts in the application.
    """

    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
