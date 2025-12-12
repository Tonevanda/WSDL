from rdflib import *
from retrieve_informacaobase import *
from retrieve_bio import *

POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")


def convert_infobase_to_rdf(xml_obj, g):

    g, leg_uri = build_legislature(xml_obj,g)
    g = build_parliamentary_groups(xml_obj, g)
    g = build_electoral_circles(xml_obj, g, leg_uri)
    g = build_legislative_session(xml_obj, g, leg_uri)
    g = build_mp(xml_obj, g, leg_uri)

    return g

def convert_bio_to_rdf(xml_obj, g):

    g = build_occupation(xml_obj, g)
    g = build_habilitations(xml_obj, g)

    return g