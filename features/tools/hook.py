# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
"""
Aprimora o mecanismo de hooks do behave.

https://pythonhosted.org/behave/tutorial.html#environmental-controls
"""

import re
import collections
import inspect
import behave.runner


class Hook(object):
    """Armazena callbacks para determinados eventos do behave."""

    def __init__(self):
        u"""Inicializa o registro padrão."""
        self.callbacks = collections.OrderedDict(**dict({"": []}))

    def __call__(self, *args):
        """Decide o que fazer com o(s) argumento(s) recebido(s)."""
        if not args:
            return self
        if isinstance(args[0], str):
            return self.get_registrar(args[0])
        if callable(args[0]):
            return self.get_registrar().__call__(args[0])
        if isinstance(args[0], behave.runner.Context):
            return self.execute(args[0], *args[1:])
        return self()

    def get_registrar(self, name=""):
        u"""
        Obtém um registrador nomeado.

        Retorna uma closure para adicionar um método à lista de registros
        nomeados, além de retornar o próprio parâmetro como resultado.
        :param name: Nome do registro de callbacks
        :type name: str
        :return: um método que registrará o callback no registro solicitado
        :rtype: callable
        """
        def registrar(callback):
            u"""
            Registra um callback.

            :param callback: O callback a ser registrado
            :type callback: callable
            :return: O próprio callback, isto permite encadeamento de decorators
            :rtype: callable
            """
            self._append_if_unique(callback, self.callbacks[name])
            return callback

        name = str(name)
        if name not in self.callbacks:
            self.callbacks[name] = []
        return registrar

    @staticmethod
    def _append_if_unique(callback, target_list):
        unique = True
        for existing in set(target_list):
            if inspect.getsource(existing) == inspect.getsource(callback):
                unique = False
                break
        if unique:
            target_list.append(callback)

    def execute(self, context, complement=None):
        u"""
        Executa os callbacks encontrados no registro obtido.

        :param context: Contexto de execução do teste, recebido pelo behave
        :type context: Context
        :param complement: Pode ser uma Tag, Feature, Scenario ou Step
        :return: Uma lista contendo o resultado da execução dos callbacks
        registrados, recebendo ```context``` e ```complement``` como parâmetros
        :rtype: list
        """
        name = str(complement or "")
        if hasattr(complement, "name"):
            name = complement.name
        callback_list = self.get_callbacks(name)
        if complement is None:
            return [callback(context) for callback in callback_list]
        return [callback(context, complement) for callback in callback_list]

    def get_callbacks(self, name=""):
        u"""
        Retorna os callbacks únicos registrados além do registro padrão.

        :param name: O nome do registro desejado
        :type name: str
        :return: A lista filtrada de callbacks únicos registrados
        :rtype: list
        """
        callbacks = []
        for matcher in self.callbacks.keys():
            if not re.search(matcher, str(name)):
                continue
            for callback in self.callbacks.get(matcher):
                self._append_if_unique(callback, callbacks)
        return callbacks


BEFORE_ALL = Hook()
BEFORE_TAG = Hook()
BEFORE_STEP = Hook()
BEFORE_SCENARIO = Hook()
BEFORE_FEATURE = Hook()
AFTER_FEATURE = Hook()
AFTER_SCENARIO = Hook()
AFTER_STEP = Hook()
AFTER_TAG = Hook()
AFTER_ALL = Hook()
