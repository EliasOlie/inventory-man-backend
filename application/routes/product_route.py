import json
from fastapi import APIRouter, Depends
from datetime import datetime, timezone, timedelta

from application.models.ApiAuthSchema import AuthRes
from application.models.ApiProduct import ApiProduct, ProductOperation
from application.models.Response import Response
from application.models.Product import Product
from application.routes.auth_route import auth_handler
from application.exceptions.Messages import BAD_REQUEST, NOT_FOUND, UNAUNTHORIZED
from infrastructure.DB import DB

router = APIRouter(
    tags=["Products"],
    prefix='/products'
)

@router.post('/create')
def create_product(p:ApiProduct, c: AuthRes = Depends(auth_handler.auth_wrapper)):
    fuso_horario = timezone(timedelta(hours=-3))
    date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
    this_product = Product(c['user_company'], p.name, p.price, p.amount, p.description)    
    transaction = DB.create_user('products',this_product.db_obj_repr())    
    #Date handling
    data = json.loads(this_product.db_obj_repr())
    data['created_at'] = date
    data['modified_by'] = c['user_name']
    data['operation'] = 'insertion'
    data = json.dumps(data)
    history = DB.create_user('producthist',data)    
    if transaction != 0 or history != 0:
        return BAD_REQUEST   
    return Response(201)

@router.get('/')
def list_products(c: AuthRes = Depends(auth_handler.auth_wrapper)):
    transaction = DB.read('products', f"product_belongs = '{c['user_company']}'", _json=True)
    if transaction:
        return Response(200, transaction)
    return BAD_REQUEST

@router.get('/product/{id}')
def read_product(id,c: AuthRes = Depends(auth_handler.auth_wrapper)):
    transaction = DB.read_one('products', f"product_id = '{id}'", _json=True)
    if transaction and transaction['product_belongs'] == c['user_company']:
        return Response(200, transaction)
    return BAD_REQUEST

@router.get('/delete/{id}')
def delete_product(id, c: AuthRes = Depends(auth_handler.auth_wrapper)):
    fuso_horario = timezone(timedelta(hours=-3))
    date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
    if c['user_role'] == 'Dono':
        data = DB.read_one('products', f"product_id = '{id}'", _json=True)
        if c['user_company'] == data['product_belongs']:
            transaction = DB.delete('products', f"product_id = '{id}'")
            if transaction != 0:
                return NOT_FOUND
            data['created_at'] = date
            data['product_price'] = str(data['product_price'])
            data['modified_by'] = c['user_name']
            data['operation'] = 'deletion'
            data = json.dumps(data)
            hist = DB.create_user('producthist', data)
            if hist != 0:
                return BAD_REQUEST
        return Response(200)
    return UNAUNTHORIZED

def hand(table,field, value, j):
    try:
        transaction = DB.read_one(table, f"{field} = '{value}'", _json=j)
        return transaction
    except Exception:
        return BAD_REQUEST

@router.put('/product/settings')
def update_product(c:ProductOperation, t: AuthRes = Depends(auth_handler.auth_wrapper)):
    fuso_horario = timezone(timedelta(hours=-3))
    date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
    if t['user_role'] == 'Dono':
        transaction = DB.update('products', c.field, c.value, f"product_id = '{c.id}'")
        if transaction == 0:
            data = hand('products', c.field, c.value, True)
            if type(data) == Exception:
                return BAD_REQUEST
            data['created_at'] = date
            data['product_price'] = str(data['product_price'])
            data['modified_by'] = t['user_name']
            data['operation'] = 'updating'
            data = json.dumps(data)
            hist = DB.create_user('producthist', data)
            if hist != 0:
                return BAD_REQUEST
            return Response(200)
        else:
            return NOT_FOUND
    return UNAUNTHORIZED

@router.post('/product')
def get_product_by_name(c: ProductOperation, u:AuthRes = Depends(auth_handler.auth_wrapper)):
    transaction = DB.read_one('products', f"product_name = '{c.value}' and product_belongs = '{u['user_company']}'", _json=True)
    if transaction:
        return Response(200, transaction)    
    return UNAUNTHORIZED
    
@router.get('/history')
def get_history(u:AuthRes = Depends(auth_handler.auth_wrapper)):
    transaction = DB.read('producthist', f"product_belongs = '{u['user_company']}'", _json=True)
    if transaction:
        return Response(200, {"Response":transaction})
    else:
        return BAD_REQUEST

@router.post('/product/{id}/entry') #<- Bugando atualizando todos :p
def registrar_entrada(id, c: ProductOperation, u:AuthRes = Depends(auth_handler.auth_wrapper)):
    product = DB.read_one('products', f"product_id = '{id}'", _json=True)
    amount = product['product_amount']
    if u['user_company'] == product['product_belongs']:
        transaction = DB.update('products', 'product_amount', amount+int(c.value), f"product_id = '{id}'")
    
    if transaction == 0: 
        fuso_horario = timezone(timedelta(hours=-3))
        date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
        data = hand('products', 'product_id', id, True)
        if type(data) == Exception:
            return BAD_REQUEST
        data['created_at'] = date
        data['product_price'] = str(data['product_price'])
        data['product_amount'] = c.value
        data['modified_by'] = u['user_name']
        data['operation'] = 'entry'
        data = json.dumps(data)
        hist = DB.create_user('producthist', data)
        if hist != 0:
            DB.rb()
            return BAD_REQUEST
        return Response(200)
    else:
        return BAD_REQUEST
    
@router.post('/product/{id}/output')
def registrar_saida(id, c: ProductOperation, u:AuthRes = Depends(auth_handler.auth_wrapper)):
    product = DB.read_one('products', f"product_id = '{id}'", _json=True)
    if u['user_company'] == product['product_belongs']:
        amount = product['product_amount']
        if amount - int(c.value) < 0:
            return Response(400, {"message": "You cannot sell more products than you have"}, True)
        else:
            transaction = DB.update('products', 'product_amount', amount-int(c.value), f"product_id = '{id}'")
    
    if transaction == 0: 
        fuso_horario = timezone(timedelta(hours=-3))
        date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
        data = hand('products', 'product_id', id, True)
        if type(data) == Exception:
            return BAD_REQUEST
        data['created_at'] = date
        data['product_price'] = str(data['product_price'])
        data['product_amount'] = c.value
        data['modified_by'] = u['user_name']
        data['operation'] = 'output'
        data = json.dumps(data)
        hist = DB.create_user('producthist', data)
        if hist != 0:
            DB.rb()
            return BAD_REQUEST
        return Response(200)
    else:
        return BAD_REQUEST