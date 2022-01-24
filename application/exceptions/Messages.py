from application.models.Response import Response

NOT_FOUND: Response = Response(404, {"Message": "This resource was not found"}, True)
UNAUNTHORIZED: Response = Response(403, {"Message": "You don't have access to this resource"}, True)
BAD_REQUEST: Response = Response(400, {"Message": "This request is not understandable, check you request and try again"}, True)