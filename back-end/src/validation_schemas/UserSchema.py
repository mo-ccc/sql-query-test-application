from main import ma
from models.User import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    email = ma.Email(required=True)