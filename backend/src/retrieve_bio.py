from rdflib import *
from xml_object import XMLObject

POLI = Namespace("http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/")
SCHEMA = Namespace("https://schema.org/")

RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

def get_attribute(element: XMLObject, type: str):
    elem = element.find_first_element_by_name(type)
    return elem.get_string() if elem else None

def build_habilitations(xml_obj: XMLObject, g: Graph, mop_uri: URIRef):
    habilitations_element = xml_obj.find_first_element_by_name('CadHabilitacoes')
    
    if habilitations_element is None:
        return g
    
    for hab in habilitations_element.find_elements_by_name('DadosHabilitacoes'):
        hab_id = get_attribute(hab, 'HabId')
        hab_des = get_attribute(hab, 'HabDes')
        hab_tipo_id = get_attribute(hab, 'HabTipoId')
        hab_estado = get_attribute(hab, 'HabEstado')
        
        if hab_id and hab_des:
            # Create a BNode for the habilitation
            hab_node = BNode()
            g.add((hab_node, RDF.type, POLI.Habilitation))
            g.add((hab_node, RDFS.label, Literal(hab_des, datatype=XSD.string)))
            g.add((hab_node, POLI.tipoId, Literal(int(float(hab_tipo_id)), datatype=XSD.int)))
            
            # Link to MoP
            g.add((mop_uri, POLI.habilitation, hab_node))
    
    return g

def build_academic_titles(xml_obj: XMLObject, g: Graph, mop_uri: URIRef):
    titles_element = xml_obj.find_first_element_by_name('CadTitulos')
    
    if titles_element is None:
        return g
    
    for title in titles_element.find_elements_by_name('DadosTitulos'):
        tit_id = get_attribute(title, 'TitId')
        tit_des = get_attribute(title, 'TitDes')
        
        if tit_id and tit_des:
            # Create a BNode for the academic title
            title_node = BNode()
            g.add((title_node, RDF.type, POLI.AcademicTitle))
            g.add((title_node, RDFS.label, Literal(tit_des, datatype=XSD.string)))
            
            # Link to MoP
            g.add((mop_uri, POLI.academicTitle, title_node))
    
    return g

def build_roles(xml_obj: XMLObject, g: Graph, mop_uri: URIRef):
    roles_element = xml_obj.find_first_element_by_name('CadCargosFuncoes')
    
    if roles_element is None:
        return g
    
    for role in roles_element.find_elements_by_name('DadosCargosFuncoes'):
        fun_id = get_attribute(role, 'FunId')
        fun_des = get_attribute(role, 'FunDes')
        
        if fun_id and fun_des:
            # Create a BNode for the role
            role_node = BNode()
            g.add((role_node, RDF.type, POLI.Role))
            g.add((role_node, RDFS.label, Literal(fun_des, datatype=XSD.string)))
            
            # Link to MoP
            g.add((mop_uri, POLI.role, role_node))
    
    return g

def build_occupation(xml_obj: XMLObject, g: Graph, mop_uri: URIRef):
    profession = get_attribute(xml_obj, 'CadProfissao')
    
    if profession:
        g.add((mop_uri, SCHEMA.jobTitle, Literal(profession, datatype=XSD.string)))
    
    return g

def build_sex(xml_obj: XMLObject, g: Graph, mop_uri: URIRef):
    sex = get_attribute(xml_obj, 'CadSexo')

    if sex:
        g.add((mop_uri, SCHEMA.gender, Literal(sex, datatype=XSD.string)))

    return g

def build_biographical_data(xml_obj: XMLObject, g: Graph):
    # Find all biographical records
    for bio_record in xml_obj.find_elements_by_name('DadosRegistoBiografico'):
        # Get MoP identification
        name = get_attribute(bio_record, 'CadNomeCompleto')
        
        if not name:
            continue
            
        # Create MoP URI (same pattern as in retrieve_informacaobase.py)
        clean_name = name.replace(' ', '_').replace("'", "").replace(",", "").replace(".", "")
        mop_uri = POLI[clean_name]
        
        has_habilitation = (mop_uri, POLI.habilitation, None) in g
        has_role = (mop_uri, POLI.hasRole, None) in g
        has_title = (mop_uri, POLI.hasAcademicTitle, None) in g
        
        g = build_sex(bio_record, g, mop_uri)
        g = build_occupation(bio_record, g, mop_uri)

        if not has_habilitation:
            g = build_habilitations(bio_record, g, mop_uri)
        
        if not has_role:
            g = build_roles(bio_record, g, mop_uri)
        
        if not has_title:
            g = build_academic_titles(bio_record, g, mop_uri)

    return g