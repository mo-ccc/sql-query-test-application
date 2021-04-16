from main import ma
from marshmallow import fields, post_dump
from models.Question import Question
import sql_metadata

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        #load_only = ("answer_as_query", )
    answer_as_query = fields.String()

    @post_dump
    def generate_schema_from_query(self, data, **kwargs):
        query = data.pop("answer_as_query", None)
        data["tables"] = sql_metadata.get_query_tables(query)
        return data