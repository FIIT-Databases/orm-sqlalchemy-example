# SQLAlchemy ORM Example

This repository demonstrates the use of SQLAlchemy ORM, which use the
[data mapper](https://martinfowler.com/eaaCatalog/dataMapper.html) pattern as architectural design.

The example is based on the data model according to the repository
[orm-django-example](https://github.com/FIIT-Databases/orm-django-example).

You can find examples in the `app.py` file.

The project utilizes [poetry](https://python-poetry.org/) for package management. It retrieves database credential
s from the environment variable `POSTGRES_CONNECTION`. Here is an example of how to set up the project on Linux:

```shell
# Clone the repository
git clone git@github.com:FIIT-Databases/orm-sqlalchemy-example.git orm_example
cd orm_example

# Set up Python virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
poetry install

# Set the POSTGRES_CONNECTION environment variable with your database credentials
export POSTGRES_CONNECTION="postgresql+psycopg://postgres@localhost:5432/dbs_orm_sqlalchemy"

# Run the example
flask example
```

---
With ❤️ FIIT STU
