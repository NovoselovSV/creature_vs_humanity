import click

from SQL_db.database import get_db
from data.user import User


@click.command()
@click.option('--username', prompt='Your username')
@click.option('--password', prompt='Your password')
@click.option('--email', prompt='Your email')
def create_admin(username, password, email):
    session = next(get_db())
    db_user = User(
        username=username,
        password=password,
        email=email,
        is_admin=True)
    session.add(db_user)
    session.commit()


if __name__ == '__main__':
    create_admin()
