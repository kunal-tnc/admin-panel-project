# This web works for the management admin panel (dashboard) and manages the data with the use of CRUD.

This project demonstrates using Fast API for web development and pSql for data storage. Specifically, it manages data from the website admin panel.
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)



## Installation

To run this project, you need to have the following installed on your machine:

- Python 3.x
- PostgreSQL


## Install Required Python Packages
- pip install -r requirements.txt 

## Usage
1. Update the path to the postgresql executable in the **database.py**:
* SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"

2. Update the FastApi_SECRET_KEY in the **config.py**:
* FastApi_SECRET_KEY = "test787987"

4. Run the project:
* uvicorn app.main:app --reload

### Clone the Repository

```sh
mkdir fastapi
cd fastapi
python -m venv venv
source venv/bin/activate
git clone https://github.com/kunal-tnc/admin-panel-project.git
cd admin-panel-project