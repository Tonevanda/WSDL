from rdflib import *
from retrieve_informacaobase import *

POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")


def convert_to_rdf(xml_obj):
    g = Graph()
    g.bind("poli", POLI)
    g.parse("../resources/poliontology.ttl", format="turtle")

    g, leg_uri = build_legislature(xml_obj,g)
    g = build_parliamentary_groups(xml_obj,g, leg_uri)
    g = build_electoral_circles(xml_obj, g, leg_uri)
    g = build_legislative_session(xml_obj, g, leg_uri)

    g.serialize(destination="test.ttl", format="turtle")


class Converter():
    def __init__(self):
        pass

    def convert(self, data):
        # Placeholder for conversion logic
        return data    