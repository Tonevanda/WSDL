from rdflib import *
from retrieve_informacaobase import *

POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")


def convert_to_rdf(xml_obj):
    g = Graph()
    g.bind("poli", POLI)
    g.parse("../resources/poliontology.ttl", format="turtle")

    g = build_parliamentary_groups(xml_obj,g)

    g.serialize(destination="test.ttl", format="turtle")


class Converter():
    def __init__(self):
        pass

    def convert(self, data):
        # Placeholder for conversion logic
        return data    