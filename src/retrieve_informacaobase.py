from datetime import datetime
from roman import fromRoman, InvalidRomanNumeralError
import xml.etree.ElementTree as ET
from rdflib import *
from xml_object import XMLObject
from linking import *

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

def get_attribute(session: XMLObject, type: str):
    element = session.find_first_element_by_name(type)
    return element.get_string() if element else None

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
    start_date = get_start_date(xml_obj)
    end_date = get_end_date(xml_obj)

    return id, start_date, end_date

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
    element = xml_obj.find_first_element_by_name('SessoesLegislativas')

    session_map = {}
    for session in element.find_elements_by_name('pt_gov_ar_objectos_SessaoLegislativaOut'):
        start_date = get_attribute(session, 'dataInicio')
        end_date = get_attribute(session, 'dataFim')
        number = get_attribute(session, 'numSessao')
        session_map[number] = start_date, end_date

    return session_map

def get_mp_info(xml_obj: XMLObject):
    def get_attribute(session: XMLObject, type: str):
        element = session.find_first_element_by_name(type)
        return element.get_string() if element else None

    element = xml_obj.find_first_element_by_name('Deputados')

    mps = {}
    for mp in element.find_elements_by_name("DadosDeputadoOrgaoPlenario"):
        id = get_attribute(xml_obj, 'DepId')
        bid = get_attribute(xml_obj, 'DepCadId')
        parliamentaryName = get_attribute(xml_obj, 'DepNomeParlamentar')
        name = get_attribute(xml_obj, 'DepNomeCompleto')

    pass

def build_legislature(xml_obj:XMLObject, g:Graph):
    legislature_element = xml_obj.find_first_element_by_name('DetalheLegislatura')

    # Get the general information
    id, start_date, end_date = get_legislature_info(legislature_element)

    legislature_uri = POLI[id]
    g.add((legislature_uri, RDF.type, POLI.Legislature))
    g.add((legislature_uri, RDFS.label, Literal(id + " Legislatura", lang="pt")))
    g.add((legislature_uri, RDFS.label, Literal(id + " Legislature", lang="en")))
    g.add((legislature_uri, SCHEMA.position, Literal(get_leg_number(id), datatype=XSD.int)))
    g.add((legislature_uri, SCHEMA.startDate, Literal(start_date, datatype=XSD.date)))
    if end_date: g.add((legislature_uri, SCHEMA.endDate, Literal(end_date, datatype=XSD.date)))

    return g, legislature_uri

def build_parliamentary_groups(xml_obj: XMLObject, g:Graph,):
    parliamentary_groups = get_parties(xml_obj)

    for party_id, party_name in parliamentary_groups.items():
        party_uri = POLI[party_id]
        g.add((party_uri, RDF.type, POLI.ParliamentaryGroup))
        g.add((party_uri, SKOS.prefLabel, Literal(party_name, lang="pt")))
        g.add((party_uri, SKOS.altLabel, Literal(party_id, lang="pt")))

    return g

def build_electoral_circles(xml_obj: XMLObject, g:Graph, leg_uri: URIRef):
    circles = get_electoral_circles_info(xml_obj)
    leg_id = str(leg_uri).split('/')[-1]

    for id, name in circles.items():
        uri_name = name.replace(' ', '_')

        uri = POLI[uri_name]
        g.add((uri, RDF.type, POLI.ElectoralCircle))
        g.add((uri, RDFS.label, Literal(name, lang="pt")))
        g.add((uri, DCTERMS.identifier, Literal(id, datatype=XSD.float)))
        g.add((uri, POLI.legislature, leg_uri))

        wd_link = get_electoral_circles_link(name)
        if wd_link is not None: g.add((uri, OWL.sameAs, "http://www.wikidata.org/wiki/"+wd_link))
    
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
        if items[1] is not None: g.add((uri, SCHEMA.endDate, Literal(items[1], datatype=XSD.date)))
        g.add((uri, POLI.legislature, leg_uri))

    return g

def build_mp(xml_obj: XMLObject, g:Graph, leg_uri: URIRef):
    def build_membership(mp: XMLObject, ctx_uri, g: Graph):

        element = mp.find_first_element_by_name('DepGP')

        for pg in element.find_elements_by_name("pt_ar_wsgode_objectos_DadosSituacaoGP"):
            acronym = get_attribute(pg, 'gpSigla')
            pg_uri = POLI[acronym]
            start_date = get_attribute(pg, 'gpDtInicio')
            end_date = get_attribute(pg, 'gpDtFim')

            
            bnode = BNode()
            g.add((bnode, RDF.type, POLI.Membership))
            g.add((bnode, POLI.group, pg_uri))
            g.add((bnode, SCHEMA.startDate, Literal(start_date, datatype=XSD.date)))
            if end_date is not None: g.add((bnode, SCHEMA.endDate, Literal(end_date, datatype=XSD.date)))


            g.add((ctx_uri, POLI.membership, bnode))
        
        return g

    def build_situation(mp: XMLObject, ctx_uri, g: Graph):
        element = mp.find_first_element_by_name('DepSituacao')
        
        for st in element.find_elements_by_name("pt_ar_wsgode_objectos_DadosSituacaoDeputado"):
            situation = get_attribute(st, 'sioDes')
            clean_sit = situation.replace(" ", "_").replace("(","_").replace(")","").replace(".","")
            sit_uri = POLI[clean_sit]
            start_date = get_attribute(st, 'sioDtInicio')
            end_date = get_attribute(st, 'sioDtFim')

            g.add((sit_uri, RDF.type, SKOS.Concept))
            g.add((sit_uri, SKOS.prefLabel, Literal(situation, lang="pt")))
            g.add((sit_uri, SKOS.inScheme, POLI["SituationTypeScheme"]))

            bnode = BNode()
            g.add((bnode, RDF.type, POLI.Situation))
            g.add((bnode, POLI.hasSituationType, sit_uri))
            g.add((bnode, SCHEMA.startDate, Literal(start_date, datatype=XSD.date)))
            if end_date is not None: g.add((bnode, SCHEMA.endDate, Literal(end_date, datatype=XSD.date)))

            g.add((ctx_uri, POLI.situation, bnode))

        return g

    def build_duty(mp: XMLObject, ctx_uri: BNode, g: Graph):
        element = mp.find_first_element_by_name('DepCargo')

        if element is None: return g
        
        for st in element.find_elements_by_name("pt_ar_wsgode_objectos_DadosCargoDeputado"):
            duty = get_attribute(st, 'carDes')
            duty_clean = duty.replace(" ", "_").replace("(","_").replace(")","")
            id = int(float(get_attribute(st, 'carId')))
            duty_uri = POLI[duty_clean]
            start_date = get_attribute(st, 'carDtInicio')
            end_date = get_attribute(st, 'carDtFim')

            g.add((duty_uri, RDF.type, SKOS.Concept))
            g.add((duty_uri, SKOS.prefLabel, Literal(duty, lang="pt")))
            g.add((duty_uri, SKOS.inScheme, POLI["DutyTypeScheme"]))
            g.add((duty_uri, DCTERMS.identifier, Literal(id, datatype=XSD.int) ))

            bnode = BNode()

            g.add((bnode, RDF.type, POLI.Duty))
            g.add((bnode, POLI.situationType, duty_uri))
            g.add((bnode, SCHEMA.startDate, Literal(start_date, datatype=XSD.date)))
            if end_date is not None: g.add((bnode, SCHEMA.endDate, Literal(end_date, datatype=XSD.date)))

            g.add((ctx_uri, POLI.duty, bnode))

        return g
    
    leg_id = str(leg_uri).split('/')[-1]
    element = xml_obj.find_first_element_by_name('Deputados')

    for mp in element.find_elements_by_name("DadosDeputadoOrgaoPlenario"):
        id = int(float(get_attribute(mp, 'DepId')))
        bid = int(float(get_attribute(mp, 'DepCadId')))
        parliamentaryName = get_attribute(mp, 'DepNomeParlamentar')
        name = get_attribute(mp, 'DepNomeCompleto')
        clean_name = name.replace(' ','_').replace("’","").replace(",","").replace(".","")
        ec = get_attribute(mp, 'DepCPDes').replace(' ', '_')
        ec_uri = POLI[f"{ec}_{leg_id}"]

        uri = POLI[clean_name]
        g.add((uri, RDF.type, POLI.MoP))
        g.add((uri, SCHEMA.name, Literal(name, datatype=XSD.string)))
        g.add((uri, POLI.parliamentaryName, Literal(parliamentaryName, datatype=XSD.string)))
        g.add((uri, POLI.bid, Literal(bid, datatype=XSD.int)))
        g.add((uri, DCTERMS.identifier, Literal(int(id), datatype=XSD.int)))

        ctx = BNode()
        g.add((ctx, POLI.legislature, leg_uri))
        g.add((ctx, POLI.electoralCircle, ec_uri))

        g = build_membership(mp, ctx, g)
        g = build_situation(mp, ctx, g)
        g = build_duty(mp, ctx, g)

    return g