# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Utilitários para os manipuladores."""


import functools
import flask


def json_response(method):
    u"""Envelopa o retorno de um controller em uma resposta JSON."""
    @functools.wraps(method)
    def wrapped_method(*args, **kwargs):
        u"""Processa o método original, gera uma responsta em JSOn e retorna."""
        response = flask.jsonify(method(*args, **kwargs))
        if args and hasattr(args[0], "code"):
            response.status_code = args[0].code
        return response
    return wrapped_method
