from fastapi import FastAPI

from sqladmin import Admin

from admin import UserAdmin
from SQL_db.database import Base, SessionLocal, engine
from web import users

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users.router)

admin = Admin(app, engine)

admin.add_view(UserAdmin)
