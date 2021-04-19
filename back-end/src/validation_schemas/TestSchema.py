from main import ma
from models.Test import Test
from .QuestionSchema import QuestionSchema

class TestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Test

    question = ma.Nested(QuestionSchema())