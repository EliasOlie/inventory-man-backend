import inspect
import json
from uuid import uuid4

class Product:
    def __init__(self, p_belongs:str, p_name:str, p_price:str, p_amount:str, p_desc:str="Não informado") -> None:
        self.product_id = uuid4()
        self.product_belongs = p_belongs
        self.product_name = p_name
        self.product_price = p_price
        self.product_amount = p_amount
        self.product_description = p_desc
        
    def db_repr(self):
        return f"'{self.product_belongs}','{self.product_name}','{self.product_description}','{self.product_price}','{self.product_amount}'"
    
    def db_obj_repr(self) -> object:
        attr = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        useds = [a for a in attr if not(a[0].startswith('__') and a[0].endswith('__'))]
        usr_obj = {}
        for used in useds:
            if useds.index(used) == len(useds)-1:
                usr_obj[f"{used[0]}"] = used[1]
               
            else:
                usr_obj[f"{used[0]}"] = used[1]

        usr_obj = json.dumps(usr_obj, default=str, ensure_ascii=False)

        return usr_obj

if __name__ == '__main__':
    p1 = Product('bc62118e-3743-4b19-9262-cfe92822a74a','EPDV', 100.0, 1, "Serviço")
    
    print(p1.db_obj_repr())