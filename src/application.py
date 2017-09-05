# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
# pylint: disable=invalid-name
u"""Definição e configuração da aplicação."""


import flask


app = flask.Flask("src")


@app.route("/")
def hello():
    u"""Método de teste da aplicação."""
    return flask.jsonify([])
