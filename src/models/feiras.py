# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Manipuladores de feiras."""


import sqlalchemy.exc
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
        u"""Inicializador da instância popula os campos recebidos."""
        self.update(**fields)
        Model.__init__(self)


try:
    Feira.query.get(0)
except sqlalchemy.exc.OperationalError:
    Feira.__table__.create(db.get_engine(), True)
    db.session.commit()
