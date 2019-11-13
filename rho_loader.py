
import os
from common.genemarkermatrix import GeneMarkerMatrix
from utils.elasticsearch import load_records

import click


def get_rho(filename=None):
    if not filename:
        package_directory = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(package_directory, "markers.yaml")
    assert os.path.exists(filename), "Rho yaml not found."
    matrix = GeneMarkerMatrix.read_yaml(filename)
    return matrix


def get_rho_celltypes():
    rho = get_rho()
    return rho.cells


def get_rho_all_markers():
    rho = get_rho()
    return dict(rho.marker_list)


@click.command()
@click.option('--filename', default=None, help='Path to marker yaml')
@click.option('--host', default='localhost', help='Hostname for Elasticsearch server')
@click.option('--port', default=9200, help='Port for Elasticsearch server')
def load_rho(filename, host, port):
    print("======================= LOADING RHO")
    rho = get_rho_all_markers()

    records = []
    for celltype, markers in rho.items():
        print(celltype + ": " + str(len(markers)) + " markers")
        celltype_records = [{"celltype": celltype,
                             "marker": marker} for marker in markers]

        records.extend(celltype_records)

    load_records("rho_markers", records, host=host, port=port)


if __name__ == "__main__":
    load_rho()
