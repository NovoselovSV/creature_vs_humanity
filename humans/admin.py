from typing import Any

from sqladmin import ModelView
from sqladmin.forms import ModelConverter, converts
from sqlalchemy.orm import ColumnProperty
from wtforms.fields import PasswordField
from wtforms.fields.core import UnboundField

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
