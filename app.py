import requests
from flask import Flask, request, jsonify
from ariadne.explorer import ExplorerGraphiQL
from ariadne import graphql_sync, load_schema_from_path, snake_case_fallback_resolvers, make_executable_schema

from api.database import db, migrate
from api.models import User
from api.queries import query, user, DebugDirective

app = Flask(__name__)
app.config.from_pyfile('config.py')


db.init_app(app)
migrate.init_app(app, db)

type_defs = load_schema_from_path("api/schema.graphql")
schema = make_executable_schema(type_defs, query, user, snake_case_fallback_resolvers,
                                directives={"DEBUG": DebugDirective})
explorer_html = ExplorerGraphiQL().html(None)


@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200


@app.route("/auth", methods=["POST"])
def auth():
    # Get Guard Token
    # get user data from guard.timmorgner.de/sso
    # check if user exists in database
    # if not, create user
    # set user id in session
    # return ok

    if request.body is None:
        return jsonify({"error": "No token provided"}), 400
    token = request.body.decode("utf-8")
    if token is None:
        return jsonify({"error": "No token provided"}), 400
    response = requests.get(app.config["SSO_URL"], params={"token": token})
    if response.status_code != 200:
        return jsonify({"error": "Invalid token"}), 400
    userdata = response.json()
    if userdata is None:
        return jsonify({"error": "Invalid token"}), 400
    userobj = User.query.filter(User.guard_id==userdata.id).first()
    if userobj is None:
        userobj = User(guard_id=userdata.id, username=userdata.name)
        db.session.add(userobj)
        db.session.commit()
    return jsonify({"id": userobj.id}), 200


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
