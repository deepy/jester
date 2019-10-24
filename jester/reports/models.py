import enum

from jester import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)


class Result(enum.Enum):
    success = 0
    skipped = 1
    failure = 2
    error = 3


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suites = db.relationship('Testsuite', backref='source', lazy=True)
    data = db.relationship('Metadata', backref='source', lazy=True)


class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.relationship('Source', backref='source', lazy=True)
    name = db.Column(db.String)
    value = db.Column(db.Integer)


class Testsuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    tests = db.Column(db.Integer)
    failures = db.Column(db.Integer)
    skipped = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    hostname = db.Column(db.String)
    stdout = db.Column(db.String)
    stderr = db.Column(db.String)
    time = db.Column(db.DECIMAL)
    timestamp = db.Column(db.TIMESTAMP)
    testcases = db.relationship('Testcase', backref='testcases', lazy=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=True)


class Testcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    classname = db.Column(db.String, nullable=False)
    result = db.Column(db.Enum(Result))
    time = db.Column(db.DECIMAL)
    message = db.Column(db.String)
    testsuite_id = db.Column(db.Integer, db.ForeignKey('testsuite.id'), nullable=False)
