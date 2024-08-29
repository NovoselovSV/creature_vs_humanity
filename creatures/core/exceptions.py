from rest_framework import status
from rest_framework.exceptions import APIException


class NotEnoughException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Not enough something'
    default_code = 'errors'


class BusyException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Already busy'
    default_code = 'errors'
