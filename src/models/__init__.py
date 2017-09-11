# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Definição de models e mapeamento de tabelas ~ classes."""


from src.application import db


class Model(db.Model):  # pylint: disable=too-few-public-methods
    u"""Model base com funções auxiliares."""

    __abstract__ = True

    def update(self, **values):
        u"""Atualiza os próprios valores a partir de chaves=valor."""
        for field, value in values.items():
            if not hasattr(self, field):
                continue
            setattr(self, field, value)
