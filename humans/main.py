from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from debug_toolbar.middleware import DebugToolbarMiddleware
from sqladmin import Admin

from SQL_db.database import Base, engine
from web import (groups, headquarters, regions, units, users)
import admin as a
import service.events  # noqa
import settings

app = FastAPI(debug=settings.DEBUG)

app.add_middleware(DebugToolbarMiddleware, panels=[
                   'debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel'])

app.include_router(users.router)
app.include_router(regions.router)
app.include_router(headquarters.router)
app.include_router(units.router)
app.include_router(groups.router)

admin = Admin(
    app,
    engine,
    authentication_backend=a.AdminAuth(
        settings.SECRET_KEY))

app.mount('/static', StaticFiles(directory='./humans_static'), name='static')

admin.add_view(a.UserAdmin)
admin.add_view(a.RegionAdmin)
admin.add_view(a.HeadquarterAdmin)
admin.add_view(a.GroupAdmin)
admin.add_view(a.UnitAdmin)
