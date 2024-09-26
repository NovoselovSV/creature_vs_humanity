import pytest

from area.models import Area
from creatures import settings


@pytest.mark.parametrize('area_diff_expect', (1,),
                         indirect=('area_diff_expect',))
def test_autocreation_nest(
        django_user_model, area_diff_expect):
    @area_diff_expect
    def wrapped():
        django_user_model.objects.create(
            username='someuser',
            email='some@mail.com',
            password='S0meStr0ngPassw0rd')
        area = Area.objects.first()
        assert area.name == settings.FIRST_AREA_NAME
        assert area.description == settings.FIRST_AREA_DESCRIPTION

    wrapped()
