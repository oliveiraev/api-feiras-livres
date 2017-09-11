# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
# pylint: disable=invalid-name
u"""Definição e configuração da aplicação."""


import os
import flask
import flask_sqlalchemy


os.environ.setdefault("DSN", "sqlite:///feiras-sp.sqlite")

app = flask.Flask("src")
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get("DSN").format(**globals()),
    SQLALCHEMY_POOL_RECYCLE=28000,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db = flask_sqlalchemy.SQLAlchemy(app)
