from typing import Any

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from sqladmin.forms import ModelConverter, converts
from sqlalchemy.orm import ColumnProperty
from starlette.requests import Request
from wtforms.fields import PasswordField
from wtforms.fields.core import UnboundField

from SQL_db.database import get_db
from data.group import Group
from data.headquarter import Headquarter
from data.region import Region
from data.unit import Unit
from data.user import User
from service.shortcuts import validate_admin
from settings import pwd_context


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        password = form['password']
        validate_admin(
            next(get_db()),
            form['username'],
            password)
        request.session.update({'token': pwd_context.hash(password)})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get('token')

        if not token:
            return False

        return True


class AdditionalPasswordConverter(ModelConverter):

    @converts('sqlalchemy_utils.types.password.PasswordType')
    def conv_date(
        self, model: type, prop: ColumnProperty, kwargs: dict[str, Any]
    ) -> UnboundField:
        return PasswordField(**kwargs)


class UserAdmin(ModelView, model=User):
    form_converter = AdditionalPasswordConverter
    column_exclude_list = ('password',)


class RegionAdmin(ModelView, model=Region):
    column_list = '__all__'


class HeadquarterAdmin(ModelView, model=Headquarter):
    column_list = '__all__'


class GroupAdmin(ModelView, model=Group):
    column_list = '__all__'


class UnitAdmin(ModelView, model=Unit):
    column_list = '__all__'
