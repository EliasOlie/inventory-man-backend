from datetime import date
from uuid import uuid4

class Company:

    """
    Classe que controla a nível de aplicação o registro de empresas
    """
    
    def __init__(self, name: str, email: str, cnpj: str, address: str = 'Não informado') -> None:
        self.id = uuid4()
        self.name = name
        self.email = email
        self.cnpj = cnpj
        self.address = address
        self.created_at = date.today()
        self.modified_at = date.today()
        self.email_verified = False
        

    def db_repr(self) -> str:
        """
        Retorna uma querie pronta com todos os dados para ser inserida no DB
        """
        return f"'{self.id}','{self.name}','{self.email}','{self.cnpj}','{self.address}','{self.created_at}','{self.modified_at}','{self.email_verified}'"


if __name__ == '__main__':
    c1 = Company('ETC', 'etc@cte.com', '15.051.325/0001-12', 'Rua Dr Genu, centro, Pesqueira-PE 55200-000')
    print(c1.db_repr())