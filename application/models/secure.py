from hashlib import sha256

class SecurityUtils():
    """
    Classe para cuidar da segurança de maneira mais simples
    """
    
    def __init__(self, password: str) -> None:
        self.password = password

    def get_hashedpsw(self):
        return sha256(bytearray(self.password, 'utf-8')).hexdigest()

if __name__ == '__main__':
    s1 = SecurityUtils('123').get_hashedpsw()
    print(s1)
    