import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

START_UNIT_HEALTH = 10
START_UNIT_ATTACK = 20
EARN_RECRUITMENT_PROCESS = 1
EARN_EXPIRIENCE = 2
RECRUITMENT_PROCESS_TO_NEW_UNIT = 100
RECRUITMENT_PROCESS_TO_NEW_HQ = 1000
EXPIRIENCE_TO_LEVEL_UP = 100
LEVEL_UP_TABLE = {'health': 10,
                  'attack': 10}
REDIS_GROUP_KEY = 'group_{group_id}_on_mission'
REDIS_GROUP_MISSION_SECOND = 3
MULT_TASK_TIME = 3
REDIS_HQ_KEY = 'hq_{hq_id}_working'
REDIS_HQ_WORKING_SECOND = 60
