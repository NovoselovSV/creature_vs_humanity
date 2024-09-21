import asyncio
from functools import wraps

import click

from data.user import User
from data.region import Region  # noqa
from data.headquarter import Headquarter  # noqa
from data.group import Group  # noqa
from service.shortcuts import aget_db
from service.users import get_user_username


def make_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@click.command()
@click.option('--username', prompt='Your username')
@click.option('--password', prompt='Your password')
@click.option('--email', prompt='Your email')
@make_sync
async def create_admin(username, password, email):
    async with aget_db() as session:
        if await get_user_username(session, username):
            click.echo('This username already obtained.')
            return
        db_user = User(
            username=username,
            password=password,
            email=email,
            is_admin=True)
        session.add(db_user)
        await session.commit()


if __name__ == '__main__':
    create_admin()
