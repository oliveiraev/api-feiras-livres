# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Manipuladores de feiras."""


import flask
from src.models import feiras
from src.application import app


@app.route("/feiras", methods=["GET"])
@app.route("/feiras/", methods=["GET"])
def retrieve():
    u"""Controller para listagem e filtro de feiras."""
    return flask.jsonify([row.as_dict() for row in feiras.Feira.query.all()])
