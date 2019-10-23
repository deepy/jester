from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from jester import db
from jester.reports.models import User, Testsuite, Testcase, Source

bp = Blueprint("reports", __name__)


@bp.route("/")
def index():
    return "Heyo"


@bp.route("/all")
def all():
    return Testsuite.query.all()


def from_json(json):
    import datetime
    suite = Testsuite()
    suite.name = json['name']
    suite.tests = json['tests']
    suite.failures = json['failures']
    suite.skipped = json['skipped']
    suite.errors = json['errors']
    suite.hostname = json['hostname']
    suite.stdout = json.get('stdout')
    suite.stderr = json.get('stderr')
    suite.time = json['time']
    suite.timestamp = datetime.datetime.fromisoformat(json['timestamp'])
    testcases = []
    for testcase in json['testcases']:
        testcases.append(Testcase(**testcase))
    suite.testcases = testcases
    if json.get('source'):
        source = Source.query.filter(Source.name == json['source']['name']).first()
        if not source:
            source = Source(name=json['source']['name'], value=json['source']['value'])
        suite.source = source
    return suite


@bp.route('/post', methods=['POST'])
def post():
    db.session.add(from_json(request.get_json()))
    db.session.commit()
    return "success!"


@bp.route('/report/<name>')
def report(name):
    # source = Source.query.filter(Source.name == name).all()
    # if not source:
    #     return []
    result = Source.query.with_entities(Source.id, Testcase.name, Testcase.classname, Testcase.result) \
        .join(Testsuite.source)\
        .join(Testcase, Testsuite.testcases).filter(Source.name == name)
    print(result)
    print(result.all())
    return ''

@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db.session.query(
            User.query.filter_by(username=username).exists()
        ).scalar():
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, create the user and go to the login page
            db.session.add(User(username=username, password=password))
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not user.check_password(password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))

