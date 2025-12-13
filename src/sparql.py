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
        print(f"{row.party} tem {row.total} deputados Sociólogos")
    
def query_academic_titles_leg(g: Graph):
     # Qual a quantidade de academic titles por legislatura
    query = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?legDesc (COUNT(?title) as ?total)
    WHERE {
        ?mop a :MoP ;
            :hasAcademicTitle ?title ;
            :servedDuring ?ctx .
        
        ?ctx :legislature ?leg .
        ?leg rdfs:label ?legDesc .
        FILTER(LANG(?legDesc) = 'pt')
    }
    GROUP BY ?leg
    ORDER BY DESC(?total)
    """
    
    for row in g.query(query):
        print(f"{row.legDesc} tem {row.total} títulos académicos")

def query(g: Graph):
    
    query_area = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX schema: <https://schema.org/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    """
   
    for row in g.query(query_area):
        print(f"{row.mopName} - {row.circleName} - {row.label}")

def main():
    g = Graph()
    g.parse("./resources/test.ttl", format="turtle")
    query_academic_titles_leg(g)

if __name__ == "__main__":
    main()


