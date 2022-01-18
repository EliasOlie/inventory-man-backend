from datetime import timezone, timedelta, datetime
import inspect
import json
from uuid import uuid4

try:
    from .secure import SecurityUtils
except ModuleNotFoundError:
    from secure import SecurityUtils
except ImportError:
    from secure import SecurityUtils

class User: 
    def __init__(self, user_name: str, user_email: str, user_password: str, user_company: str, user_role:str='Funcionário') -> None:
        self.user_id = uuid4()
        self.user_name = user_name
        self.user_email = user_email
        self.user_company = user_company
        self.user_role = user_role
        self.user_password = SecurityUtils(user_password).get_hashedpsw()
        
        fuso_horario = timezone(timedelta(hours=-3))
        date = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')
        
        self.created_at = date
        self.modified_at = date
        self.is_active = True
        self.email_verified = False
        
    def db_obj_repr(self) -> object:
        attr = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        useds = [a for a in attr if not(a[0].startswith('__') and a[0].endswith('__'))]
        usr_obj = {}
        for used in useds:
            usr_obj[f"{used[0]}"] = used[1]
        
        usr_obj['user_id'] = str(usr_obj['user_id'])
        usr_obj = json.dumps(usr_obj, default=str, ensure_ascii=False)

        return usr_obj
    
if __name__ == '__main__':
    test = User('elias', 'e@.cm', '1234', 'ETC')
    print(test.db_obj_repr())