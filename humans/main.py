import os
from fastapi import FastAPI
from debug_toolbar.middleware import DebugToolbarMiddleware
from sqladmin import Admin

import admin as a
import service.events  # noqa
import settings
from SQL_db.database import Base, engine
from web import (groups, headquarters, regions, units, users)

app = FastAPI(debug=settings.DEBUG)

if 'PYTEST_VERSION' not in os.environ:
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

admin.add_view(a.UserAdmin)
admin.add_view(a.RegionAdmin)
admin.add_view(a.HeadquarterAdmin)
admin.add_view(a.GroupAdmin)
admin.add_view(a.UnitAdmin)
