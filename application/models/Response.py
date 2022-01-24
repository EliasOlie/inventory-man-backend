import json

class Response():
    def __init__(self, status:int, data:object=None, error:bool=False) -> None:
        self.status = status
        self.data = data
        self.error = error

    def __repr__(self):
        return json.dumps({"data":self.data, "status": self.status, "error": self.error})
##Sobrescrever a response do proprio fastapi?

if __name__ == '__main__':
    print(Response(400, {"Hello": "World"}, True))
    print(Response(400, {"Hello": "World"}, False))
    print(Response(400))