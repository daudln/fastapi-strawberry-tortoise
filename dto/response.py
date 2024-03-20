import json
import strawberry
from typing import Generic, TypeVar

TData = TypeVar('TData')

@strawberry.type
class ResponseObject:
    id: int
    code: int
    status: bool
    message: str
    
    @classmethod
    def get_response(cls, response_id:int):
        with open('assets/response_codes.json', 'r') as file:
            response_data = json.load(file)
        
        matching_response = next((response for response in response_data if response['id'] == response_id), None)
        if matching_response:
            code = matching_response.get('code', '')
            message = matching_response['message']
            status = matching_response['status']
            return cls(id=response_id, code=code, status=status, message=message)
        
        return cls(id=-1, code=0000, status=False, message='Invalid response ID')


@strawberry.type
class Response(Generic[TData]):
    response: ResponseObject
    data: TData | None

    def __init__(self, response: ResponseObject, data: TData|None = None):
        self.response = response
        self.data = data

    @classmethod
    def get_response(cls, response_id:int, data: TData|None = None)-> 'Response[TData]':
        response = ResponseObject.get_response(response_id)
        return cls(data=data, response=response)