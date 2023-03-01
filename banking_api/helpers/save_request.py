import json
from banking_api.models.request import Request


def save_request(request_endpoint, request_method, request_data, response):
    """Save the request made to the Belvo API"""
    Request.objects.create(
        endpoint=request_endpoint,
        method=request_method,
        data=request_data,
        response=response,
    )
