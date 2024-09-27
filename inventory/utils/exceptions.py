from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': response.data.get('detail', 'An error occurred.'),
                'errors': response.data
            }
        }
        return Response(custom_response_data, status=response.status_code)

    # Handle any unexpected exceptions not caught by DRF's handler
    return Response(
        {'error': {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                   'message': 'An internal server error occurred.'}},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
