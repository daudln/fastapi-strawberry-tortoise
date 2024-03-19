import json
from typing import Generic, TypeVar

import strawberry

T = TypeVar('T', bound=strawberry.type)


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
        
        return cls(id=-1, status=False, message='Invalid response ID')


class Response(Generic[T]):
    def __init__(self, data: T, status: bool = True, message: str = "Success"):
        self.data = data
        self.status = status
        self.message = message

    @staticmethod
    def from_data(data: T, status: bool = True, message: str = "Success") -> 'Response':
        return Response(data=data, status=status, message=message)

    @staticmethod
    def from_error(message: str = "Error") -> 'Response':
        return Response(status=False, message=message)

    def to_dict(self):
        return {
            'status': self.status,
            'message': self.message,
            'data': strawberry.asdict(self.data)
        }

def create_response_object(data: T, status: bool = True, message: str = "Success") -> ResponseObject:
    return ResponseObject(data=data, status=status, message=message)
