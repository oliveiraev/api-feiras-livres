# -*- coding: utf-8 -*-
# vim: sta sts=2 sw=2 et ai si ff=unix eol fenc=utf-8 nobomb ft=cucumber
Feature: Entry testing
  Scenario: Entry listing
    When I request /feiras
    Then response body should match
    """
    \[(
      {
        "areap": "\d+",\s
        "bairro": ".*?",\s
        "coddist": "\d+",\s
        "codsubpref": "\d+",\s
        "distrito": ".*?",\s
        "id": \d+,\s
        "lat": "-?\d+",\s
        "logradouro": ".*?",\s
        "long": "-?\d+",\s
        "nome_feira": ".*?",\s
        "numero": ".*?",\s
        "referencia": ".*?",\s
        "regiao5": ".*?",\s
        "regiao8": ".*?",\s
        "registro": ".*?",\s
        "setcens": "\d+",\s
        "subprefe": ".*?"
      }(,\s)?){500}
    ]
    """

  Scenario: Entry search
    When I request /feiras?distrito=JABAQUARA
    Then response body should match
    """
    \[]
    """
    When I request /feiras?regiao5=Norte
    Then response body should match
    """
    \[]
    """
    When I request /feiras?nome_feira=LIMOEIRO
    Then response body should match
    """
    \[]
    """
    When I request /feiras?bairro=BUTANTA
    Then response body should match
    """
    \[]
    """

  Scenario: Invalid entry ID
    When I request /feiras/99999999
    Then response code should be 404
    And response body should match
    """
    {
      "error": "Not found."
    }
    """

  Scenario: Entry insertion
    When request data is
        | bairro | distrito |
        | bairro | distrito |
    And I post to /feiras
    Then response code should be 201
    And response body should match
    """
    {}
    """

  Scenario: Entry validation
    When request data is
        | numero |
        | NaN    |
    And I post to /feiras
    Then response code should be 400
    And response body should match
    """
    {
      "error": "Bad request."
    }
    """

  Scenario: Entry update
    When request data is
        | numero |
        | 123456 |
    And I post to /feiras/1
    Then response code should be 200
    And response body should match
    """
    {}
    """

  Scenario: Entry deletion
    When I request /feiras/1
    Then response code should be 200
    When I delete /feiras/1
    Then response code should be 202
    When I request /feiras/1
    Then response code should be 404
