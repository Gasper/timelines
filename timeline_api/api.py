import json
import graphql_api

from flask import Flask, request, make_response, abort
from db.mongo_db import MongoDatabase

flask_app = Flask(__name__)
db = MongoDatabase()


@flask_app.route('/graphql', methods=['POST'])
def graphql():
    graphql_query = request.get_data(as_text=True)
    query_result = graphql_api.schema.execute(graphql_query, context={'database': db})
    if query_result.errors:
        abort(500)
    response = make_response(json.dumps(query_result.data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    flask_app.run(debug=True)
