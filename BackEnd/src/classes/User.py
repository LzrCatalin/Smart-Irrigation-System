class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password
        }
    
    @staticmethod
    def from_dict(data: dict) -> "User":
        user = User(
            email = data['email'],
            password = data['password']
        )
        return user