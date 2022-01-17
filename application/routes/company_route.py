from fastapi import APIRouter, Depends

from .auth_route import auth_handler
from application.models.ApiCompany import ApiCompany, CompanyOperation
from application.models.ApiAuthSchema import AuthRes
from application.models.Company import Company
from application.models.Response import Response, INVALID_CREDENTIALS
from infrastructure.DB import DB

router = APIRouter(
    tags=["Company"],
    prefix='/company'
)

@router.post('/create')
def create_company(c:ApiCompany):
    this_company = Company(c.name, c.email, c.cnpj, c.address)
    transaction = DB.insert('company', this_company.db_repr())
    if transaction != 0:
        return Response(400, {"MSG": "Something went wrong :/"})
    return Response(201)

@router.get('/')
def read_company(c: AuthRes = Depends(auth_handler.auth_wrapper)):   
    try:
        transaction = DB.read_one('company', f"company_name = '{c['user_company']}'", _json=True)
        employees = DB.read('iuser', f"user_company = '{c['user_company']}'", 'user_id, user_name, user_role, is_active', True)
        products = DB.read('products', f"product_belongs = '{c['user_company']}'", 'product_id, product_name, product_description, product_price, product_amount', True)
        hist = DB.read('producthist', f"product_belongs = '{c['user_company']}'", _json=True)
        user = DB.read_one('iuser', f"user_id = '{c['user_id']}'", 'user_id, user_name, user_role, is_active', True)
        if c['user_role'] == 'Dono' and transaction:
            return Response(200, {"Company": transaction, "Employees": employees, "Products": products, "History":hist, "User":user})
        if transaction:
            employees = DB.read_one('iuser', f"user_name = '{c['user_name']}'", 'user_id, user_name, user_role, is_active', True)
            return Response(200, {"Company": transaction, "Employees": [employees], "Products": products, "History":hist, "User":user})
            
        return Response(400, {"MSG": "Company not found, or you're not logged"}, error=True)
    except(AttributeError, TypeError):
        return INVALID_CREDENTIALS

@router.get('/delete')
def delete_company(c: AuthRes = Depends(auth_handler.auth_wrapper)):
    try:
        if c['user_role'] == 'Dono':
            transaction = DB.delete('company', f"company_name = '{c['user_company']}' cascade")
        else:
            return Response(403, {"MSG": "You don't have access to this resource"}, True)
        if transaction != 0:
            return Response(400, {"MSG": "Company not found, or you're not logged"}, True)
        return Response(200)
    except(AttributeError, TypeError):
        return INVALID_CREDENTIALS
    
@router.put('/settings')
def update_company(c:CompanyOperation, C: AuthRes = Depends(auth_handler.auth_wrapper)):
    try:
        if C['user_role'] == 'Dono':
            transaction = DB.update('company', c.field, c.value, f"company_name = '{C['user_company']}'")
        else:
            return Response(403, {"MSG": "You don't have access to this resource"}, True)
        if transaction != 0:
            return Response(400, {"MSG": "Something went wrong :/"}, True)
        
        return Response(200)
    except(AttributeError, TypeError):
        return INVALID_CREDENTIALS
    