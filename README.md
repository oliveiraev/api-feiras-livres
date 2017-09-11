# API Restful: Feiras Livres de São Paulo

Bem vindo a bordo deste projeto. Inicie clonando...

```shell
git clone https://github.com/oliveiraev/api-feiras-sp feiras-sp
```

A execução é simples com [docker-compose](https://docs.docker.com/compose/overview/):

```shell
docker-compose up
```

A aplicação estará disponível em instantes em http://localhost/v1/feiras.

A execução com docker também testa escalabilidade horizontal, executando a
aplicação em dois contêineres paralelos atrás de um contêiner Nginx atuando como
load balancer.

A implementação utilizada também facilita o desenvolvimento e execução em
paralelo de futuras iterações da aplicação. Novas versões podem ser prefixadas
com ``/v2``, ``/v3`` sem interferir na execução das versões legadas.

A configuração baseada em variáveis de ambiente permite que se altere o
banco de dados sobrescrevendo uma única variável, bastando alterar o valor
desejado em ``defaults.env``


## #soudev

A stack de desenvolvimento escolhida foi Python3, Flask e SQLite.

A aplicação roda de forma transparente como uma aplicação Flask clássica...

```shell
FLASK_APP=src/application.py flask run
```

Note que, executando desta forma, o banco de dados será um SQLite localizado em
``src/feiras-sp.sqlite`` e as URL's serão mapeadas diretamente para a raiz,
não necessitando do prefixo ``/v1``.

Lembre-se de instalar as dependências através de ``pip install -r
requirements.txt``

**É altamente recomendável o uso de um [virtualenv](https://virtualenv.pypa.io/en/stable/)!!**


### Testes automatizados

A suíte de testes unitários está localizada em ``/tests`` e pode ser executada
com

```shell
python -m unittest discover . '*.py'
```

Também há teste de comportamento para verificar a integração dos processos. A
suíte está em ``/features`` e roda com o [behave](http://pythonhosted.org/behave/):

```shell
behave
```

### Git Hooks

Há uma série de validadores e tarefas automatizadas configuradas que podem ser
instaladas nos hooks de 'pre-commit' e 'pre-push'. Para isto, basta instalar o
[pre-commit](http://pre-commit.com/) e executar

```
pre-commit install -t pre-commit
pre-commit install -t pre-push
```

### Cobertura de código

Execute ``python cover.py`` para obter um relatório de cobertura.

O script executará tanto os testes unitários como os testes de integração.

Caso você tenha instalado os hooks de pre-push, este script impedirá o push
sempre que a cobertura for inferior a 70%.

## API


| Verbo  | Endpoint | Descrição | Retorno |
|--------|----------|-----------|---------|
| GET    | /feiras  | Lista as feiras cadastradas | Status: 200 - Retorna uma lista em JSON |
| GET    | /feiras?parametro=valor  | Filtra as feiras cadastradas | Status: 200 - Retorna uma lista em JSON |
| POST   | /feiras  | Cadastra uma nova feira | Status: 201 - Retorna um objeto em JSON representando a nova feira ou Status: 400 - Caso alguma informação não passe na validação. |
| GET    | /feiras/:id | Lista uma feira em específico | Status: 200 - Um objeto em JSON contendo a feira encontrada ou Status: 404 - Um objeto informando do erro |
| POST   | /feiras/:id | Atualiza uma feira | Status: 202 - Um objeto em JSON representando a feira atualizada ou Status: 400 - Caso alguma informação não passe na validação. |
| DELETE | /feiras/:id | Apaga uma feira | Status: 204 - Vazio ou Status: 404 - Um objeto informando do erro |
