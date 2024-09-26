from django.core.cache import cache

from rest_framework.mixins import status
import pytest

from . import tasks
from creatures import settings
from creatures.celery import app as celery_app


@pytest.mark.parametrize('nest_diff_expect', (1,),
                         indirect=('nest_diff_expect',))
def test_autocreation_nest(
        django_user_model, nest_diff_expect):
    @nest_diff_expect
    def wrapped():
        user = django_user_model.objects.create(
            username='someuser',
            email='some@mail.com',
            password='S0meStr0ngPassw0rd')
        assert user.nests.exists()
        first_nest = user.nests.filter(name=settings.FIRST_NEST_NAME).first()
        assert first_nest.owner == user
        assert (first_nest.new_creature_birth_process ==
                settings.BIRTH_PROCESS_TO_APPEAR)

    wrapped()


def test_owner_can_start_new_creature_creation(
        url_nest,
        created_nest,
        created_owner_client,
        delete_redis_n_celery_keys_nest):
    response = created_owner_client.post(
        url_nest,
        content_type='application/json',
        data={'name': 'Creatures name',
              'description': 'Creatures description'})
    assert response.status_code == status.HTTP_201_CREATED
    task_id = cache.get(settings.BIRTH_KEY.format(nest=created_nest), False)
    assert task_id
    assert cache.get(task_id, False)
