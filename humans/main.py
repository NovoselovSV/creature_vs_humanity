from fastapi import FastAPI

from sqladmin import Admin

from admin import RegionAdmin, UserAdmin
from SQL_db.database import Base, engine
from web import regions, users

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(regions.router)

admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(RegionAdmin)
