from datetime import datetime
#from roman import fromRoman, InvalidRomanNumeralError
import xml.etree.ElementTree as ET
from rdflib import *
from xml_object import XMLObject
POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")
#from database.legislatura import Legislatura

"""def get_leg_number(id: str):

    #Convert a Roman numeral ID to an integer.
    #Returns None if the ID is not a valid Roman numeral.

    try:
        return fromRoman(id) if id else None
    except InvalidRomanNumeralError:
        return None
"""

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
    bid = get_bid(xml_obj)
    id = get_id(xml_obj)
    display_start_date = get_start_date(xml_obj)
    display_end_date = get_end_date(xml_obj)
    ended = True if display_end_date else False

    # Get the start and end dates in timestamp format
    start_date = datetime.fromtimestamp(datetime.strptime(display_start_date, "%Y-%m-%d").timestamp()) if display_start_date else None
    end_date = datetime.fromtimestamp(datetime.strptime(display_end_date, "%Y-%m-%d").timestamp()) if display_end_date else None

    return bid, id, start_date, end_date, display_start_date, display_end_date, ended


    """
    """

#ef build_legislature(xml_obj: XMLObject):
#   """
#   Build a Legislatura object from the XML tree.
#   """
#
#   legislature_element = xml_obj.find_first_element_by_name('DetalheLegislatura')
#
#   # Get the general information
#   bid, id, start_date, end_date, display_start_date, display_end_date, ended = get_legislature_info(legislature_element)
#
#   # Get the parties
#   parties = get_parties(xml_obj)
#
#   # Get the legNumber from the ID
#   leg_number = get_leg_number(id)
#
#   # Create the Legislatura object
#   legislatura = Legislatura(
#       BID=bid,
#       id=id,
#       startDate=start_date,
#       endDate=end_date,
#       displayStartDate=display_start_date,
#       displayEndDate=display_end_date,
#       parties=parties,
#       ended=ended,
#       legNumber=leg_number
#   )
#
#   legislatura.store()

#def retrieve_informacaobase(xml_obj: XMLObject):
#    """
#    Get the legislatures from the XML file.
#    """
#
#    build_legislature(xml_obj)


def build_parliamentary_groups(xml_obj: XMLObject, g:Graph):
    parliamentary_groups = get_parties(xml_obj)

    for party_id, party_name in parliamentary_groups.items():
        party_uri = POLI[party_id]
        g.add((party_uri, RDF.type, POLI.ParliamentaryGroup))
        g.add((party_uri, RDFS.label, Literal(party_name, lang="pt"))) 

    return g