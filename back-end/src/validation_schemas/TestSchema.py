from main import ma
from models.Test import Test
from marshmallow import fields
from .QuestionSchema import QuestionSchema

class TestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Test

    question = fields.Nested(QuestionSchema())