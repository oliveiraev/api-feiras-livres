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
    \[(
      {
        "areap": "\d+",\s
        "bairro": ".*?",\s
        "coddist": "\d+",\s
        "codsubpref": "\d+",\s
        "distrito": "JABAQUARA",\s
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
      }(,\s)?){10}
    ]
    """
    When I request /feiras?regiao5=Norte
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
        "regiao5": "Norte",\s
        "regiao8": ".*?",\s
        "registro": ".*?",\s
        "setcens": "\d+",\s
        "subprefe": ".*?"
      }(,\s)?){102}
    ]
    """
    When I request /feiras?nome_feira=LIMOEIRO
    Then response body should match
    """
    \[
      {
        "areap": "3550308005195",\s
        "bairro": "LIMOEIRO",\s
        "coddist": "89",\s
        "codsubpref": "23",\s
        "distrito": "VILA JACUI",\s
        "id": 351,\s
        "lat": "-23506444",\s
        "logradouro": "AV MANOEL DOS SANTOS BRAGA",\s
        "long": "-46469267",\s
        "nome_feira": "LIMOEIRO",\s
        "numero": "251.000000",\s
        "referencia": "PROX GAR ON PENHA S MIGUEL",\s
        "regiao5": "Leste",\s
        "regiao8": "Leste 2",\s
        "registro": "3084-8",\s
        "setcens": "355030887000096",\s
        "subprefe": "SAO MIGUEL"
      }
    ]
    """
    When I request /feiras?bairro=BUTANTA
    Then response body should match
    """
    \[(
      {
        "areap": "\d+",\s
        "bairro": "BUTANTA",\s
        "coddist": "\d+",\s
        "codsubpref": "10",\s
        "distrito": ".*?",\s
        "id": \d+,\s
        "lat": "-?\d+",\s
        "logradouro": ".*?",\s
        "long": "-?\d+",\s
        "nome_feira": ".*?",\s
        "numero": ".*?",\s
        "referencia": ".*?",\s
        "regiao5": "Oeste",\s
        "regiao8": "Oeste",\s
        "registro": ".*?",\s
        "setcens": "\d+",\s
        "subprefe": "BUTANTA"
      }(,\s)?){3}
    ]
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
        | areap         | bairro          | coddist | codsubpref | distrito    | lat       | logradouro    | long      | nome_feira    | numero | referencia             | regiao5 | regiao8 | registro | setcens         | subprefe    |
        | 4000000000000 | JARDIM UMARIZAL | 17      | 17         | CAMPO LIMPO | -23619899 | AVENIDA ANACE | -46756883 | AVENIDA ANACE | 319    | ESTRADA DO CAMPO LIMPO | Sul     | Sul 2   | 6543-2   | 400000000000001 | CAMPO LIMPO |
    And I post to /feiras
    Then response code should be 201
    And response body should match
    """
    {
      "areap": "4000000000000",\s
      "bairro": "JARDIM UMARIZAL",\s
      "coddist": "17",\s
      "codsubpref": "17",\s
      "distrito": "CAMPO LIMPO",\s
      "id": 501,\s
      "lat": "-23619899",\s
      "logradouro": "AVENIDA ANACE",\s
      "long": "-46756883",\s
      "nome_feira": "AVENIDA ANACE",\s
      "numero": "319",\s
      "referencia": "ESTRADA DO CAMPO LIMPO",\s
      "regiao5": "Sul",\s
      "regiao8": "Sul 2",\s
      "registro": "6543-2",\s
      "setcens": "400000000000001",\s
      "subprefe": "CAMPO LIMPO"
    }
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
    {
      "areap": "3550308005040",\s
      "bairro": "VL FORMOSA",\s
      "coddist": "87",\s
      "codsubpref": "26",\s
      "distrito": "VILA FORMOSA",\s
      "id": 1,\s
      "lat": "-23558733",\s
      "logradouro": "RUA MARAGOJIPE",\s
      "long": "-46550164",\s
      "nome_feira": "VILA FORMOSA",\s
      "numero": "123456",\s
      "referencia": "TV RUA PRETORIA",\s
      "regiao5": "Leste",\s
      "regiao8": "Leste 1",\s
      "registro": "4041-0",\s
      "setcens": "355030885000091",\s
      "subprefe": "ARICANDUVA-FORMOSA-CARRAO"
    }
    """

  Scenario: Entry deletion
    When I request /feiras/1
    Then response code should be 200
    When I delete /feiras/1
    Then response code should be 202
    When I request /feiras/1
    Then response code should be 404
