class UserDTO:
    def __init__(self, id: str, email: str):
        self.id = id
        self.email = email

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email
        }
    
    @staticmethod
    def from_dict(data: dict) -> "UserDTO":
        userDTO = UserDTO(
            id = data['id'],
            email = data['email']
        )       
        return userDTO