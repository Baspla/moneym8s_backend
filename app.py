from flask import Flask, request, jsonify
from ariadne.explorer import ExplorerGraphiQL
from ariadne import graphql_sync, load_schema_from_path, snake_case_fallback_resolvers, make_executable_schema, \
    ObjectType

import models
from database import db, migrate
from queries import query, user, DebugDirective

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs,query,user, snake_case_fallback_resolvers,directives={"DEBUG":DebugDirective})
explorer_html = ExplorerGraphiQL().html(None)

@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request, "userid": 1337},
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route('/')
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run()
