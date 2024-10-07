import pytest
from pytest_lazy_fixtures import lf

from beast.models import Beast
from creatures import settings
from nest.tasks import create_creature

NEW_C_CREATURES_NAME = 'The creature'
NEW_C_CREATURES_DESCRIPTION = 'The description'


@pytest.mark.parametrize('make_diff_expect', (1,),
                         indirect=('make_diff_expect',))
def test_correct_birth(
        created_owner, created_nest, make_diff_expect):
    @make_diff_expect
    def wrapped():
        key = settings.BIRTH_KEY.format(nest=created_nest)
        create_creature.apply(args=(created_nest.id,
                              {'owner': created_owner.id,
                               'name': NEW_C_CREATURES_NAME,
                               'description': NEW_C_CREATURES_DESCRIPTION},
                              key))

    wrapped(Beast)


@pytest.mark.parametrize('incorrect_parametr, make_diff_expect',
                         (({'nest_id': -1}, 0),
                          ({'owner_id': -1}, 0),
                          ({'name': NEW_C_CREATURES_NAME}, 1)),
                         indirect=('make_diff_expect',))
def test_uncorrect_birth(
        created_owner,
        created_nest,
        make_diff_expect,
        incorrect_parametr):
    @make_diff_expect(Beast)
    def wrapped():
        if 'name' in incorrect_parametr:
            Beast.objects.create(
                owner=created_owner,
                name=NEW_C_CREATURES_NAME,
                description=NEW_C_CREATURES_DESCRIPTION,
                nest=created_nest)
        key = settings.BIRTH_KEY.format(nest=created_nest)
        create_creature.apply(args=(
            incorrect_parametr.get('nest_id', created_nest.id),
            {'owner': incorrect_parametr.get('owner_id', created_owner.id),
             'name': incorrect_parametr.get('name', NEW_C_CREATURES_NAME),
             'description': NEW_C_CREATURES_DESCRIPTION},
            key))

    wrapped()
