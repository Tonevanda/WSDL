from owlready2 import *

def defineOntology() -> Ontology:

    onto = get_ontology("http://example.org/PoliOntology.owl")
    #schema = get_ontology("https://schema.org/version/latest/schemaorg-current-https.ttl").load()

    schema = get_namespace("https://schema.org/")
    dct = get_namespace("http://purl.org/dc/terms/")
    m4sc = get_namespace("https://example.org/map4scrutiny/core#")
    rdfs = get_namespace("http://www.w3.org/2000/01/rdf-schema#")
    ocd = get_namespace("https://dati.camera.it/ocd/")
    foaf = get_namespace("http://xmlns.com/foaf/0.1/")

    #ocd = get_ontology("https://dati.camera.it/ocd/classi.rdf").load()
    #popolo_event = get_ontology("https://www.popoloproject.com/examples/event.ttl").load()
    #foaf = get_ontology("https://iptc.org/thirdparty/foaf/index.rdf").load()

    with onto:
        

        # ---------- CLASSES ---------- #

        class MoP(schema.Person):
            equivalent_to = [ocd.Deputato]
            label = "Deputado à Assembleia da Républica@pt", "Member of Parliament@en"
            # todo: m4sc:parliamentarian
            # todo: parliament person

        class Legislature(Thing):
            equivalent_to = [ocd.Legislatura]
            label = "Legislatura@pt", "Legislature@en"
            #todo parliament legislature

        class ParliamentaryGroup(Thing):
            equivalent_to = [ocd.gruppoParlamentare]
            label = "Grupo Parlamentar@pt", "Parliamentary Group@en"

        class ElectoralCircle(Thing):
            label = "Círculo Eleitoral@pt", "Electoral Circle@en"
            pass

        class LegislativeSession(Thing):
            label = "Sessão Legislativa@pt", "Legislative Session@en"
            pass

        class MoPSituation(Thing):
            label = "Situação do deputado@pt", "Situation of the member of parliament@en"
            pass

        class MoPDuty(Thing):
            label = "Cargo do deputado@pt", "Duty of the member of parliament@en"
            pass

        class InterestRegistry(Thing):
            label = "Registo de interesses@pt", "Interest Registry@en"
            pass

        # ---------- OBJECT PROPERTIES ---------- #

        class isMemberOf(MoP >> ParliamentaryGroup):
            pass

        class electedIn(MoP >> ElectoralCircle):
            pass

        class servesDuring(MoP >> Legislature):
            pass

        class hasLegislativeSession(Legislature >> LegislativeSession):
            pass

        class inLegislature(ElectoralCircle >> Legislature):
            pass

        class inSituation(MoP >> MoPSituation):
            pass

        class hasDuty(MoP >> MoPDuty):
            pass

        class hasInterestRegistry(MoP >> InterestRegistry):
            pass

        # ---------- DATA PROPERTIES ---------- #

        class bid(DataProperty, FunctionalProperty):
            domain = [MoP]
            range = [int]
            label = "ID do deputado no website do parlamento@pt", "Member of Parliament ID based on the parlamento.pt website@en"
        
        foaf.accountName.domain = [MoP] # == username
        dct.identifier.domain = [MoP, ParliamentaryGroup, ElectoralCircle, MoPDuty] 

        class parliamentaryName(DataProperty, FunctionalProperty):
            domain = [MoP]
            range = [str]
            label = "Nome abreviado do deputado como usado no parlamento@pt", "Abbreviated name of the member of parliament, as used in the parliament@en"

        #class mopUsername(DataProperty, FunctionalProperty):
        #    domain = [MoP]
        #    range = [str]
        #    label = "Nome de Utilizador do deputado@pt", "Member of Parliament username@en"

        #class parliamentaryGroupName(DataProperty, FunctionalProperty):
        #    domain = [ParliamentaryGroup]
        #    range = [str]
        #    label = "Nome do grupo parlamentar@pt", "Parliamentary group name@en"

        rdfs.label.domain = [ParliamentaryGroup, MoPSituation, MoPDuty, ElectoralCircle]
        schema.startDate.domain = [Legislature, LegislativeSession, ParliamentaryGroup, MoPSituation, MoPDuty]
        schema.endDate.domain = [Legislature, LegislativeSession, ParliamentaryGroup, MoPSituation, MoPDuty]
        
        schema.position.domain = [Legislature, LegislativeSession]

        """
        
        class parliamentaryGroupAcronym(DataProperty, FunctionalProperty):
            domain = [ParliamentaryGroup]
            range = [str]
            label = "Sigla do grupo parlamentar@pt", "Parliamentary group acronym@en"
        
        class electoralCircleName(DataProperty, FunctionalProperty):
            domain = [ElectoralCircle]
            range = [str]
            label = "Nome do círculo eleitoral@pt", "Electoral circle name@en"
        
        class electoralCircleCode(DataProperty, FunctionalProperty):
            domain = [ElectoralCircle]
            range = [str]
            label = "Código do círculo eleitoral@pt", "Electoral circle code@en"

        class legislatureTerm(DataProperty, FunctionalProperty):
            domain = [Legislature]
            range = [int]
            label = "Número da legislatura@pt", "Legislature term@en"

        class legislativeSessionTerm(DataProperty, FunctionalProperty):
            domain = [LegislativeSession]
            range = [int]
            label = "Número da sessão legislativa@pt", "Term from the legislative session@en"

        class parliamentDuty(DataProperty, FunctionalProperty):
            domain:

        """

        

    return onto