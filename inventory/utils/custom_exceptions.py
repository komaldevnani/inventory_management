from rest_framework.exceptions import APIException
from rest_framework import status

class ItemNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested inventory item does not exist.'
    default_code = 'item_not_found'

class InvalidDataException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid data provided.'
    default_code = 'invalid_data'
