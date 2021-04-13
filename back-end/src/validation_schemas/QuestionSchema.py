from main import ma
from models.Question import Question

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question