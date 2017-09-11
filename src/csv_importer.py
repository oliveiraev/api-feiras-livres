# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Importa um csv para a base de dados."""


import os
import sys
import csv
import pprint

try:
    import src.application
    import src.models.feiras
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    import src.application
    import src.models.feiras


def file_to_data(file_path):
    u"""Processa um caminho de arquivo e retorna uma lista de dicionários."""
    data = []
    for file_row in csv.DictReader(open(file_path)):
        data_row = {}
        for key, value in file_row.items():
            try:
                data_row[key.lower()] = value
            except AttributeError:
                print("Skipping invalid row...")
                pprint.pprint(file_row)
                data_row = None
                break
        if data_row:
            data.append(data_row)
    return data


def data_to_db(*lines, **row):
    u"""Obtém uma lista de dicionários ou um dicionário e cadasta na app."""
    for line in lines:
        data_to_db(**line)
    if not [v for v in row.values() if v]:
        print("skipping empty row...")
        return
    src.application.db.session.add(src.models.feiras.Feira(**row))


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        data_to_db(*file_to_data(filename))
    src.application.db.session.commit()
