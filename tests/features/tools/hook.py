# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Testes para o módulo Hook."""

import abc
import re
import unittest
import behave.configuration
import behave.runner
import behave.model
from features.tools.hook import Hook


class TestHook(unittest.TestCase):
    """Testes para a classe features.tools.hook.Hook."""

    def __init__(self, *args, **kwargs):
        """Inicializa o hook de teste e o contexto do behave."""
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.hook = Hook()
        config = behave.configuration.Configuration()
        self.context = behave.runner.Context(behave.runner.Runner(config))

    def test_get_registrar_return(self):
        u"""Chamar o hook como um decorator deve retornar o método decorado."""
        assert self.hook.get_registrar().__call__(self) is self

    def test_empty_registrar_to_string(self):
        u"""Chamar o hook sem um nome retorna o registrador padrão."""
        assert len(self.hook.callbacks.get("")) is 0
        self.hook.get_registrar().__call__(self)
        assert len(self.hook.callbacks.get("")) is 1

    def test_named_get_registrar(self):
        """Teste para um registrador nomeado."""
        assert len(self.hook.callbacks.get("callback_name", [])) is 0
        self.hook.get_registrar("callback_name").__call__(self)
        assert len(self.hook.callbacks.get("callback_name", [])) is 1

    def test_avoid_duplicated_register(self):
        u"""Obtém apenas callbacks únicos num mesmo registrador."""
        registrar = self.hook.get_registrar("callback_name")
        assert len(self.hook.callbacks.get("callback_name", [])) is 0
        registrar(self.hook.execute)
        assert len(self.hook.callbacks.get("callback_name", [])) is 1
        registrar(self.hook.execute)
        assert len(self.hook.callbacks.get("callback_name", [])) is 1

    def test_empty_execution(self):
        u"""
        Execução dos hooks sem um parâmetro adicional.

        Esta execução acontece nos hooks before_all e after_all
        """
        self.hook.callbacks.get("").append(self.hook.get_registrar)
        assert self.hook.execute(self.context).pop().__name__ == "registrar"

    def test_named_execution(self):
        u"""Execução dos hooks com tags."""
        self.hook.callbacks["tag_name"] = [hasattr]
        assert self.hook.execute(self.context, "tag_name") == [False]

    def test_model_execution(self):
        u"""Execução dos hooks com models (Features, Scenarios e Steps)."""
        models = [
            behave.model.Feature(__file__, 0, u"", u"feature"),
            behave.model.Scenario(__file__, 0, u"", u"scenario"),
            behave.model.Step(__file__, 0, u"", u"given", u"step")
        ]
        for model in models:
            self.hook.callbacks[model.name] = [abc.abstractproperty]
            for result in self.hook.execute(self.context, model):
                assert result.fget is self.context
                assert result.fset is model

    def test_multiple_execution(self):
        u"""Teste de execução de um hook com mais de um callback registrado."""
        self.hook.callbacks.get("").append(self.hook.get_registrar)
        self.hook.callbacks.get("").append(self.hook.get_callbacks)
        result = self.hook.execute(self.context)
        assert len(result) == 2
        assert hasattr(result[0], "__call__")
        assert hasattr(result[1], "__iter__")

    def test_simple_callback_query(self):
        u"""Obtém os callbacks sem precisar informar um nome de registro."""
        assert len(self.hook.get_callbacks()) is 0
        self.hook.callbacks.get("").append(self.hook.__init__)
        assert len(self.hook.get_callbacks()) is 1

    def test_get_unregistered_callback(self):
        u"""Quando solicitar um registro inválido, retorna o registro padrão."""
        assert len(self.hook.get_callbacks("unregistered")) is 0
        self.hook.callbacks.get("").append(self.__class__)
        assert len(self.hook.get_callbacks("unregistered")) is 1

    def test_registered_callback_query(self):
        u"""Um registro nomeado retornar também o registro padrão."""
        self.hook.callbacks.get("").append(self.__init__)
        self.hook.callbacks["registered"] = [self.hook.__init__]
        assert len(self.hook.get_callbacks("registered")) == 2

    def test_unique_callback_list(self):
        u"""Obtém apenas callbacks unicos entre o registro desejado e padrão."""
        assert len(self.hook.get_callbacks("registered")) is 0
        self.hook.callbacks.get("").append(self.hook.execute)
        assert len(self.hook.get_callbacks("registered")) is 1
        self.hook.callbacks["registered"] = [self.hook.execute]
        assert len(self.hook.get_callbacks("registered")) is 1
        self.hook.callbacks.get("registered").append(self.__class__)
        assert len(self.hook.get_callbacks("registered")) == 2
        self.hook.callbacks.get("").append(self.__class__)
        assert len(self.hook.get_callbacks("registered")) == 2

    def test_usage(self):
        """Teste para os usos como decorator."""
        assert self.hook() is self.hook
        registrar = self.hook("get_registrar")
        assert re.search(r"<function .*registrar", str(registrar))
        assert len(self.hook.callbacks.get("")) is 0
        not_callable = True
        assert self.hook(not_callable) is self.hook
        assert len(self.hook.callbacks.get("")) is 0
        assert self.hook(abc.abstractproperty) is abc.abstractproperty
        assert len(self.hook.callbacks.get("")) is 1
        simple_call = self.hook(self.context)
        for result in simple_call:
            assert result.fget is self.context
            assert result.fset is None
        tag_call = self.hook(self.context, "tag_name")
        for result in tag_call:
            assert result.fget is self.context
            assert result.fset == "tag_name"
        model = behave.model.Feature(__file__, 0, u"", u"feature")
        model_call = self.hook(self.context, model)
        for result in model_call:
            assert result.fget is self.context
            assert result.fset is model
