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
    filters = {}
    for param in "distrito", "regiao5", "nome_feira", "bairro":
        if param not in flask.request.args:
            continue
        filters[param] = flask.request.args[param]
    rows = feiras.Feira.query.filter_by(**filters)
    return flask.jsonify([row.as_dict() for row in rows])
