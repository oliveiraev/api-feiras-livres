# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Manipuladores de feiras."""


import werkzeug.exceptions
import sqlalchemy.exc
import flask_validator
from src.models import db, Model


class Feira(Model):  # pylint: disable=too-few-public-methods
    u"""Definição da tabela de feiras."""

    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(254))
    lat = db.Column(db.String(254))
    setcens = db.Column(db.String(254))
    areap = db.Column(db.String(254))
    coddist = db.Column(db.String(254))
    distrito = db.Column(db.String(254))
    codsubpref = db.Column(db.String(254))
    subprefe = db.Column(db.String(254))
    regiao5 = db.Column(db.String(254))
    regiao8 = db.Column(db.String(254))
    nome_feira = db.Column(db.String(254))
    registro = db.Column(db.String(254))
    logradouro = db.Column(db.String(254))
    numero = db.Column(db.String(254))
    bairro = db.Column(db.String(254))
    referencia = db.Column(db.String(254))

    def __init__(self, **fields):
        u"""Valida os campos numéricos antes de definir seus valores."""
        try:
            for field in "id", "coddist", "codsubpref":
                if field not in fields:
                    continue
                fields[field] = int(fields[field])
        except (ValueError, TypeError):
            message_template = "Incorrect value for {}: \"{}\""
            message = message_template.format(field, fields[field])
            raise werkzeug.exceptions.BadRequest(description=message)
        self.update(**fields)
        Model.__init__(self)

    @classmethod
    def __declare_last__(cls):
        u"""Validação do flask_validator."""
        flask_validator.ValidateNumeric(cls.id)
        flask_validator.ValidateNumeric(cls.coddist)
        flask_validator.ValidateNumeric(cls.codsubpref)


try:
    Feira.query.get(0)
except sqlalchemy.exc.OperationalError:
    Feira.__table__.create(db.get_engine(), True)
    db.session.commit()
