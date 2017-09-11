# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Passos de execução via código (API)."""

import re
import requests
from features.environment import before_scenario, when, then


@before_scenario
def setup_request(unused_context, scenario):
    u"""Inicia uma requisição limpa para cada cenário."""
    scenario.request = requests.PreparedRequest()
    scenario.request.prepare_method("GET")
    scenario.request.prepare_headers({})
    scenario.request.data = dict()


@when(u"request data is")
def fill_request(context):
    u"""Preenche os campos para a requisição."""
    step = u"When request {} is {}"
    for row in context.table.rows:
        for idx, value in enumerate(row):
            field = context.table.headings[idx]
            context.execute_steps(step.format(field, value))


@when(u"I request {url}")
def execute_request(context, url):
    u"""Executa a requisição."""
    url = "http://127.0.0.1:{}/{}".format(
        context.server.options.get("port"),
        url[int(url.startswith("/")):]
    )
    request = context.scenario.request
    request.prepare_url(url, {})
    request.prepare_cookies(None)
    request.prepare_body(None, request.headers, context.scenario.request.data)
    context.scenario.response = requests.Session().send(request)


@when(u"I post to {url}")
def post(context, url):
    u"""Executa uma requisição POST."""
    context.execute_steps(u"When request method is POST")
    context.execute_steps(u"When I request {}".format(url))


@then(u"response body should match {}")
def assert_response_body(context, body):
    u"""Testa o resultado da requisição contra uma regex."""
    match = re.compile(body, re.MULTILINE)
    response = context.scenario.response.text
    assert match.search(response), "Expected {}, got {}".format(body, response)


@then(u"response body should match")
def assert_response_text(context):
    u"""Testa o resultado da requisição contra uma regex multilinha."""
    assert_response_body(context, context.text)


@then(u"response code should be {}")
def assert_response_status(context, code):
    u"""Testa o código de resposta da requisição."""
    code = int(code)
    status = context.scenario.response.status_code
    assert code == status, "Expected {}, got {}".format(code, status)


@when(u"request method is {}")
def set_request_method(context, method):
    u"""Altera o verbo HTTP da requisição."""
    context.scenario.request.prepare_method(method)


@when(u"request {} is {}")
def set_data_field(context, field, value):
    u"""Define um par chave=valor para a próxima requisição."""
    context.scenario.request.data[field] = value


@when(u"I delete {url}")
def delete(context, url):
    u"""Define o verbo HTTP como DELETE e executa a requisição."""
    context.execute_steps(u"When request method is DELETE")
    context.execute_steps(u"When I request {}".format(url))
