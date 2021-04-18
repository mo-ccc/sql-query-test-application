from main import ma, db
from marshmallow import fields, post_dump
from models.Question import Question
import sql_metadata

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        #load_only = ("answer_as_query", )
    answer_as_query = fields.String()

    # this massive function takes the answer_as_query
    # and parses all the tables from the query
    # then generates a schema for each table
    # and adds it all to the json being dumped
    @post_dump
    def generate_schema_from_query(self, data, **kwargs):
        query = data.pop("answer_as_query", None)
        tables = sql_metadata.get_query_tables(query)
        tables_dict = {}

        
        with db.session.connection().connection.cursor() as curs:
            curs.execute("""SET search_path TO secondary_schema;""")
            for x in tables:
                curs.execute(f"""SELECT column_name, data_type 
                FROM (SELECT * FROM information_schema.columns
                WHERE table_schema NOT IN ('information_schema','pg_catalog')
                ORDER BY table_schema, table_name) AS c WHERE table_name='{x}';
                """)
                tables_dict[x] = curs.fetchall()
        data["tables"] = tables_dict

        return data