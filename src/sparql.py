from rdflib import *

def query_sociologia_party(g: Graph):
    # Quais os partidos com mais deputados sociólogos
    query = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?party (COUNT(DISTINCT ?mop) as ?total)
    WHERE {

            ?hab a :Habilitation ;
                rdfs:label ?habName .
            FILTER(REGEX(?habName, "sociologia", "i"))

            ?hab ^:habilitation ?mop .

            ?mop :servedDuring ?ctx .
            ?ctx :membership ?mem .
            ?mem :group ?group .
            ?group skos:altLabel ?party .
        
    }
    GROUP BY ?party
    ORDER BY DESC(?total)
    """

    for row in g.query(query):
        print(f"{row.party} - {row.total} deputados Sociólogos")
    


def queries(g: Graph):
    
    query_area = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX schema: <https://schema.org/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?mopName ?circleName ?label
    WHERE {
        ?mop a :MoP ;
            schema:name ?mopName ;
            :servedDuring ?context .

        ?context :electoralCircle ?circle ;
            :membership ?membership ;
            :situation ?situation ;
            :legislature ?leg .

        ?leg rdfs:label ?label .
        FILTER(LANG(?label) = "pt")

        ?membership :group :PCP .

        ?situation :situationType ?sitType ;
                   schema:startDate ?startDate .
        
        ?sitType skos:prefLabel ?situationType .
        FILTER(LANG(?situationType) = "pt")
        
        ?circle rdfs:label ?circleName .
        FILTER(LANG(?circleName) = "pt")

        {
            SELECT ?context (MAX(?date) AS ?maxDate)
            WHERE {
                ?context :situation ?s .
                ?s schema:startDate ?date .
            }
            GROUP BY ?context
        }
        FILTER(?startDate = ?maxDate && ?situationType = "Efetivo")
            
        
    }
    ORDER BY ?mopName
    """
   
    for row in g.query(query_area):
        print(f"{row.mopName} - {row.circleName} - {row.label}")

g = Graph()
g.parse("./resources/test.ttl", format="turtle")
query_sociologia_party(g)