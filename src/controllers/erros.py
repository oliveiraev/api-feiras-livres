# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Descrição de rotas para páginas de erro."""


from werkzeug import exceptions
from src import app
from src.handlers import json_response


@app.errorhandler(exceptions.BadRequest)
@json_response
def bad_request(err):
    u"""Erro disparado em requisições não autenticadas."""
    return {"error": getattr(err, "description", "Bad request.")}


@app.errorhandler(exceptions.NotFound)
@json_response
def not_found(unused_error):
    u"""Erro disparado em requisições a endereços inválidos."""
    return {"error": "Not found."}


@app.errorhandler(exceptions.MethodNotAllowed)
@json_response
def invalid_method(unused_error):
    u"""Erro disparado ao acessar um endpoint por um método não suportado."""
    return {"error": "Method not allowed."}


@app.errorhandler(exceptions.InternalServerError)
@json_response
def gone(err):
    u"""Erro disparado ao acessar um recurso marcado para exclusão."""
    setattr(err, "code", 500)
    return {"error": getattr(err, "description", "Internal server error.")}
