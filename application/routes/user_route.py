from fastapi import APIRouter, Depends
from datetime import timezone, timedelta, datetime

from application.models.ApiAuthSchema import AuthRes
from application.models.ApiUser import ApiUser, UserOperation, UserOp
from application.models.Response import Response
from application.models.User import User
from application.models.secure import SecurityUtils
from application.routes.auth_route import auth_handler
from application.exceptions.Messages import BAD_REQUEST, NOT_FOUND, UNAUNTHORIZED
from infrastructure.DB import DB

router = APIRouter(
    tags=["User"],
    prefix='/user'
)

@router.post('/create')
def create_user(u:ApiUser):
    this_user = User(u.name, u.email, u.password, u.company, u.role)
    transaction = DB.create_user('iuser', this_user.db_obj_repr())
    if transaction != 0:
        return BAD_REQUEST
    
    return Response(201)

@router.get('/')
def read_user(u: AuthRes = Depends(auth_handler.auth_wrapper)):
    try:
        transaction = DB.read_one('iuser', f"user_id = '{u['user_id']}'", _json=True)
        transaction.pop('user_password')
        if len(transaction) >= 1:
            return Response(200, transaction)
        return NOT_FOUND
    
    except (AttributeError, TypeError):
        return INVALID_CREDENTIALS

@router.get('/{id}')
def read_specific_user(id, u: AuthRes = Depends(auth_handler.auth_wrapper)):
    try:
        if u['user_role'] == 'Dono':
            transaction = DB.read_one('iuser', f"user_id = '{id}'", _json=True)
            transaction.pop('user_password')
            
            if len(transaction) >= 1:
                return Response(200, transaction)
        return NOT_FOUND
    
    except (AttributeError, TypeError):
        return INVALID_CREDENTIALS

@router.get('/delete/{id}')
def delete_user(id, u: AuthRes = Depends(auth_handler.auth_wrapper)):
    try:
        if u['user_role'] == 'Dono':
            transaction = DB.delete('iuser', f"user_id = '{id}'")
            if transaction != 0:
                return NOT_FOUND   
            return Response(200)
        else:
            return UNAUNTHORIZED
    except(AttributeError, TypeError):
        return INVALID_CREDENTIALS
    
@router.post('/delete/user')
def delete_user(c: UserOperation,u: AuthRes = Depends(auth_handler.auth_wrapper)):
    try:
        transaction = DB.read_one('iuser', f"user_id = '{u['user_id']}'")
        if u['user_role'] == 'Dono':
            DB.delete('iuser', f"user_id = '{c['user_deletion']}'")
        else:
            return UNAUNTHORIZED
        if transaction != 0:
            return NOT_FOUND
        
        return Response(200)
    except(AttributeError, TypeError):
        return INVALID_CREDENTIALS

@router.put('/settings/user')
def update_specific_user(c: UserOp,u: AuthRes = Depends(auth_handler.auth_wrapper)):
    fuso_horario = timezone(timedelta(hours=-3))
    date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
    try:
        if u['user_role'] == 'Dono':
            change = DB.update('iuser', c.field, c.value, f"user_id = '{c.id}'")
            update = DB.update('iuser', 'modified_at', date, f"user_id = '{u['user_id']}'")
        else: 
            if c.field != 'user_name':
                return UNAUNTHORIZED
            else:
                change = DB.update('iuser', c.field, c.value, f"user_id = '{c.id}'")
                update = DB.update('iuser', 'modified_at', date, f"user_id = '{u['user_id']}'")            
        if change != 0 or update != 0:
            return NOT_FOUND
        
        return Response(200, {"data": c})
    except Exception as e:
        print(e)
        return BAD_REQUEST
    
@router.put('/settings')
def update_user(c:UserOperation, u: AuthRes = Depends(auth_handler.auth_wrapper)):
    fuso_horario = timezone(timedelta(hours=-3))
    date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
    try:
        if c.field == 'user_role' and u['user_role'] != 'Dono':
            return UNAUNTHORIZED
        transaction = DB.update('iuser', c.field, c.value, f"user_id = '{u['user_id']}'")
        update = DB.update('iuser', 'modified_at', date, f"user_id = '{u['user_id']}'")
        if transaction != 0 or update != 0:
            return BAD_REQUEST
        
        return Response(200)
    except(AttributeError, TypeError):
        return INVALID_CREDENTIALS
    
@router.post('/recover')
def reset_password(c: UserOperation,u: AuthRes = Depends(auth_handler.auth_wrapper)):
    fuso_horario = timezone(timedelta(hours=-3))
    date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')    
    verify = DB.login('iuser', u['user_email'])
    if not verify:
        return NOT_FOUND
    if len(verify) == 1:
        if auth_handler.verify_password(c.extra, verify[0]):
            transaction = DB.update('iuser', c.field, SecurityUtils(c.value).get_hashedpsw(), f"user_id = '{u['user_id']}'")
            update = DB.update('iuser', 'modified_at', date, f"user_id = '{u['user_id']}'")
            if transaction != 0 or update != 0:
                return BAD_REQUEST
            else:
                return Response(200)
        else:
            return UNAUNTHORIZED