import strawberry
from typing import Generic, TypeVar

T = TypeVar('T', bound=strawberry.type)

@strawberry.type
class ResponseObject:
    id: int
    status: bool
    message: str
    data: T

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
