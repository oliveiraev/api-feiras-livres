# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Manipuladores de feiras."""


import flask
import werkzeug.exceptions
import src.handlers
from src.models import feiras
from src.application import app, db


@app.route("/feiras", methods=["GET"])
@app.route("/feiras/", methods=["GET"])
@src.handlers.json_response
def retrieve():
    u"""Controller para listagem e filtro de feiras."""
    filters = {}
    for param in "distrito", "regiao5", "nome_feira", "bairro":
        if param not in flask.request.args:
            continue
        filters[param] = flask.request.args[param]
    rows = feiras.Feira.query.filter_by(**filters)
    return [row.as_dict() for row in rows]


def on_json_loading_failed(decode_error):
    u"""Intercepta erros de processamento de request e dispara um erro 400."""
    raise werkzeug.exceptions.BadRequest(str(decode_error))


def get_post_data():
    u"""Caso não hajam dados válidos na requisição, dispara um erro 400."""
    flask.request.on_json_loading_failed = on_json_loading_failed
    post_data = flask.request.get_json()
    if not post_data:
        raise werkzeug.exceptions.BadRequest({
            "message": "Empty or invalid JSON post data."
        })
    return post_data


@app.route("/feiras", methods=["POST"])
def register():
    u"""Cadastro de uma nova feira."""
    row = feiras.Feira(**get_post_data())
    db.session.add(row)
    db.session.commit()
    return flask.jsonify(row.as_dict()), 201


def get_row(row_id):
    u"""Tenta obter uma feira ou dispara um erro 404 caso contrário."""
    row = feiras.Feira.query.get(row_id)
    if row is None:
        raise werkzeug.exceptions.NotFound()
    return row


@app.route("/feiras/<int:row_id>", methods=["GET"])
@src.handlers.json_response
def entity(row_id):
    u"""Exibição de uma única feira em específico."""
    return get_row(row_id).as_dict()


@app.route("/feiras/<int:row_id>", methods=["POST", "PUT"])
def update(row_id):
    u"""Atualização das informações de uma feira já cadastrada."""
    row = get_row(row_id)
    row.update(**get_post_data())
    db.session.commit()
    return flask.jsonify(row.as_dict()), 200


@app.route("/feiras/<int:row_id>", methods=["DELETE"])
def remove(row_id):
    u"""Exclusão de uma feira cadastrada."""
    db.session.delete(get_row(row_id))
    db.session.commit()
    return flask.Response(status=202, mimetype="application/json")
