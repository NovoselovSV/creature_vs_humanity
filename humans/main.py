from fastapi import FastAPI

from debug_toolbar.middleware import DebugToolbarMiddleware
from sqladmin import Admin

from SQL_db.database import Base, engine
from admin import (
    AdminAuth,
    GroupAdmin,
    HeadquarterAdmin,
    RegionAdmin,
    UnitAdmin,
    UserAdmin)
from web import (groups, headquarters, regions, units, users)
import service.events # noqa
import settings

app = FastAPI(debug=True)

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
    authentication_backend=AdminAuth(
        settings.SECRET_KEY))

admin.add_view(UserAdmin)
admin.add_view(RegionAdmin)
admin.add_view(HeadquarterAdmin)
admin.add_view(GroupAdmin)
admin.add_view(UnitAdmin)
