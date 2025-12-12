from rdflib import *

def queries2(g: Graph):
    # Now with the most recent Efetivo filter (fixed)
    query_area = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
PREFIX schema: <https://schema.org/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?mopName ?circleName ?startDate
WHERE {

    # Situation anchor
    ?situation a :Situation ;
               :situationType :Efetivo ;
               schema:startDate ?startDate ;
               ^:situation ?context .

    # Legislature
    ?context :legislature :XVII ;
             :electoralCircle ?circle .

    # Membership of same context
    ?membership ^:membership ?context ;
                :group :PCP .

    # MoP linked to same context
    ?mop ^:servedDuring ?context ;
         schema:name ?mopName .

    # Circle label
    ?circle rdfs:label ?circleName .
    FILTER(LANG(?circleName) = "pt")

    # Keep only latest effective situation
    FILTER NOT EXISTS {
        ?context :situation ?laterSit .
        ?laterSit schema:startDate ?laterDate .
        FILTER(?laterDate > ?startDate)
    }
}
LIMIT 100

    """
    
    print("\n=== 100 MoP with Efetivo as most recent situation ===")
    count = 0
    for row in g.query(query_area):
        print(f"{row.mopName} - {row.circleName} - (desde {row.startDate})")
        count += 1
    
    print(f"\nTotal: {count} members")


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
queries2(g)