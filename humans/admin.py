from typing import Any

from sqladmin import ModelView
from sqladmin.forms import ModelConverter, converts
from sqlalchemy.orm import ColumnProperty
from wtforms.fields import PasswordField
from wtforms.fields.core import UnboundField

from data.headquarter import Headquarter
from data.region import Region
from data.user import User


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
    column_exclude_list = '__all__'
