from datetime import datetime
from roman import fromRoman, InvalidRomanNumeralError
import xml.etree.ElementTree as ET
from rdflib import *
from xml_object import XMLObject

POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")
SCHEMA = Namespace("https://schema.org/")
#from database.legislatura import Legislatura

def get_leg_number(id: str):

    #Convert a Roman numeral ID to an integer.
    #Returns None if the ID is not a valid Roman numeral.

    try:
        return fromRoman(id) if id else None
    except InvalidRomanNumeralError:
        return None


def get_bid(xml_obj: XMLObject):
    """
    Get the BID of the legislatura from the XML tree.
    """

    element = xml_obj.find_first_element_by_name('id')

    return element.get_string() if element else None

def get_id(xml_obj: XMLObject):
    """
    Get the ID of the legislatura from the XML tree.
    """
    element = xml_obj.find_first_element_by_name('sigla')

    return element.get_string() if element else None

def get_start_date(xml_obj: XMLObject):
    """
    Get the start date of the legislatura from the XML tree.
    """
    element = xml_obj.find_first_element_by_name('dtini')

    return element.get_string() if element else None

def get_end_date(xml_obj: XMLObject):
    """
    Get the end date of the legislatura from the XML tree.
    """
    element = xml_obj.find_first_element_by_name('dtfim')

    return element.get_string() if element else None

def get_parties(xml_obj: XMLObject):
    """
    Get the parties of the legislatura from the XML tree.
    Returns a dictionary mapping party_id -> party_full_name.
    """

    def get_party_id(party: XMLObject):
        element = party.find_first_element_by_name('sigla')
        return element.get_string() if element else None

    def get_party_full_name(party: XMLObject):
        element = party.find_first_element_by_name('nome')
        return element.get_string() if element else None

    element = xml_obj.find_first_element_by_name('GruposParlamentares')

    parties_map = {}
    for party in element.find_elements_by_name('pt_gov_ar_objectos_GPOut'):
        party_id = get_party_id(party)
        party_full_name = get_party_full_name(party)
        if party_id:
            parties_map[party_id] = party_full_name

    return parties_map

def get_legislature_info(xml_obj: XMLObject):
    """
    Get the general legislature information from the XML tree.
    """

    # Get the ID, like "XVI"
    #bid = get_bid(xml_obj)
    id = get_id(xml_obj)
    display_start_date = get_start_date(xml_obj)
    display_end_date = get_end_date(xml_obj)
    ended = True if display_end_date else False

    # Get the start and end dates in timestamp format
    start_date = datetime.fromtimestamp(datetime.strptime(display_start_date, "%Y-%m-%d").timestamp()) if display_start_date else None
    end_date = datetime.fromtimestamp(datetime.strptime(display_end_date, "%Y-%m-%d").timestamp()) if display_end_date else None

    return id, start_date, end_date, display_start_date, display_end_date, ended

def get_electoral_circles_info(xml_obj: XMLObject):
    def get_id(circle: XMLObject):
        element = circle.find_first_element_by_name('cpId')
        return element.get_string() if element else None
    def get_name(circle: XMLObject):
        element = circle.find_first_element_by_name('cpDes')
        return element.get_string() if element else None

    element = xml_obj.find_first_element_by_name('CirculosEleitorais')

    circles_map = {}
    for circle in element.find_elements_by_name('pt_ar_wsgode_objectos_DadosCirculoEleitoralList'):
        id = get_id(circle)
        name = get_name(circle)
        if id:
            circles_map[id] = name
    
    return circles_map

def get_legislative_session_info(xml_obj: XMLObject):
    def get_session_start_date(session: XMLObject):
        element = session.find_first_element_by_name('dataInicio')
        return element.get_string() if element else None
    def get_session_end_date(session: XMLObject):
        element = session.find_first_element_by_name('dataFim')
        return element.get_string() if element else None
    def get_session_number(session: XMLObject):
        element = session.find_first_element_by_name('numSessao')
        return element.get_string() if element else None

    element = xml_obj.find_first_element_by_name('SessoesLegislativas')

    

    session_map = {}
    for session in element.find_elements_by_name('pt_gov_ar_objectos_SessaoLegislativaOut'):
        display_start_date = get_session_start_date(session)
        display_end_date = get_session_end_date(session)
        ended = True if display_end_date else False

        number = get_session_number(session)

        # Get the start and end dates in timestamp format
        start_date = datetime.fromtimestamp(datetime.strptime(display_start_date, "%Y-%m-%d").timestamp()) if display_start_date else None
        end_date = datetime.fromtimestamp(datetime.strptime(display_end_date, "%Y-%m-%d").timestamp()) if display_end_date else None

        session_map[number] = start_date, end_date, ended

    return session_map

def get_mp_info(xml_obj: XMLObject):

    element = xml_obj.find_first_element_by_name('Deputados')

    pass

def build_legislature(xml_obj:XMLObject, g:Graph):
    legislature_element = xml_obj.find_first_element_by_name('DetalheLegislatura')

    # Get the general information
    id, start_date, end_date, display_start_date, display_end_date, ended = get_legislature_info(legislature_element)

    legislature_uri = POLI[id]
    g.add((legislature_uri, RDF.type, POLI.Legislature))
    g.add((legislature_uri, RDFS.label, Literal(id + " Legislatura", lang="pt")))
    g.add((legislature_uri, RDFS.label, Literal(id + " Legislature", lang="en")))
    g.add((legislature_uri, SCHEMA.position, Literal(get_leg_number(id), datatype=XSD.int)))
    g.add((legislature_uri, SCHEMA.startDate, Literal(start_date, datatype=XSD.date)))
    if not ended: g.add((legislature_uri, SCHEMA.endDate, Literal(end_date, datatype=XSD.date)))

    return g, legislature_uri

def build_parliamentary_groups(xml_obj: XMLObject, g:Graph, leg_uri: URIRef):
    parliamentary_groups = get_parties(xml_obj)
    leg_id = str(leg_uri).split('/')[-1]


    for party_id, party_name in parliamentary_groups.items():
        party_uri = POLI[f"{party_id}_{leg_id}"]
        g.add((party_uri, RDF.type, POLI.ParliamentaryGroup))
        g.add((party_uri, RDFS.label, Literal(f"{party_name} durante a {leg_id} legislatura", lang="pt")))
        g.add((party_uri, RDFS.label, Literal(f"{party_name} during the {leg_id} legislature", lang="en")))
        g.add((party_uri, SKOS.prefLabel, Literal(party_name, lang="pt")))
        g.add((party_uri, SKOS.altLabel, Literal(party_id, lang="pt")))
        g.add((party_uri, POLI.representedInLegislature, leg_uri))

    return g

def build_electoral_circles(xml_obj: XMLObject, g:Graph, leg_uri: URIRef):
    circles = get_electoral_circles_info(xml_obj)
    leg_id = str(leg_uri).split('/')[-1]

    for id, name in circles.items():
        uri_name = name.replace(' ', '_')

        uri = POLI[f"{uri_name}_{leg_id}"]
        g.add((uri, RDF.type, POLI.ElectoralCircle))
        g.add((uri, RDFS.label, Literal(name, lang="pt")))
        g.add((uri, DCTERMS.identifier, Literal(id, datatype=XSD.float)))
        g.add((uri, POLI.inLegislature, leg_uri))
    
    return g

def build_legislative_session(xml_obj: XMLObject, g:Graph, leg_uri: URIRef):
    leg_id = str(leg_uri).split('/')[-1]
    sessions = get_legislative_session_info(xml_obj)

    for session, items in sessions.items():
        uri = POLI[f"{session}_{leg_id}"]
        g.add((uri, RDF.type, POLI.LegislativeSession))
        g.add((uri, RDFS.label, Literal("Sessão legislativa número " + session + " da " + leg_id + " legislatura", lang="pt")))
        g.add((uri, RDFS.label, Literal("Legislative session number " + session + " from the " + leg_id + " legislature", lang="en")))
        g.add((uri, SCHEMA.position, Literal(session, datatype=XSD.int)))
        g.add((uri, SCHEMA.startDate, Literal(items[0], datatype=XSD.date)))
        if not items[2]: g.add((uri, SCHEMA.endDate, Literal(items[1], datatype=XSD.date)))
        g.add((uri, POLI.duringLegislature, leg_uri))

    return g

def build_mp(xml_obj: XMLObject, g:Graph, leg_uri: URIRef):
    leg_id = str(leg_uri).split('/')[-1]

    return g