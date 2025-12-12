from datetime import datetime
from roman import fromRoman, InvalidRomanNumeralError
import xml.etree.ElementTree as ET
from rdflib import *
from xml_object import XMLObject

POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")
SCHEMA = Namespace("https://schema.org/")

def build_occupation(xml_obj, g):
    pass

def build_habilitations(xml_obj, g):
    pass