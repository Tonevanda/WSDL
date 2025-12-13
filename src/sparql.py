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

def query_leg_electorate_area(g: Graph):
    # Regiões com mais eleitores e a respetiva área com estatísticas dos deputados
    query_area = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX schema: <https://schema.org/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?circleName ?electorate ?area 
           (COUNT(DISTINCT ?mop) as ?totalMoPs)
           (COUNT(DISTINCT ?title) as ?totalTitles)
           (COUNT(DISTINCT ?duty) as ?totalDuties)
           (GROUP_CONCAT(DISTINCT ?party; separator=", ") as ?parties)
    WHERE {
        ?circle a :ElectoralCircle ;
                rdfs:label ?circleName ;
                :legislatures :XVII ;
                owl:sameAs ?wd .
        
        SERVICE <https://query.wikidata.org/sparql> {
            ?wd wdt:P1831 ?electorate .
            FILTER(?electorate > 1000000)

            OPTIONAL {
                ?wd wdt:P131 ?region .
                ?region wdt:P2046 ?area .
            }
        }
        
        ?circle ^:electoralCircle ?context .
        ?context :legislature :XVII ;
                 :situation ?sit ;
                 :membership ?membership ;
                 ^:servedDuring ?mop .
        
        ?sit :situationType :Efetivo .

        ?membership :group ?group .
        ?group skos:altLabel ?party .
        
        OPTIONAL {
            ?mop :hasAcademicTitle ?title .
        }
        
        OPTIONAL {
            ?context :duty ?duty .
        }
    }
    GROUP BY ?circleName ?electorate ?area
    ORDER BY DESC(?electorate)
    """
   
    for row in g.query(query_area):
        area = f"{int(row.area):,} km²" if row.area else "N/A"
        print(f"\n{row.circleName}")
        print(f"  Eleitores: {int(row.electorate):,}")
        print(f"  Área: {area}")
        print(f"  Deputados: {row.totalMoPs}")
        print(f"  Títulos Académicos: {row.totalTitles}")
        print(f"  Cargos: {row.totalDuties}")
        print(f"  Partidos: {row.parties}")

def query_uni_teach_electorate(g: Graph):
    # Professores universitários em círculos eleitorais com mais de 1 milhão de eleitores
    query_area = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX schema: <https://schema.org/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?circleName ?electorate #?mopName ?circleName ?jobTitle ?electorate
    WHERE {
        # First, get electoral circles with > 1M electorate from Wikidata
        ?circle a :ElectoralCircle ;
                rdfs:label ?circleName ;
                :legislatures :XVII ;
                owl:sameAs ?wd .
        
        SERVICE <https://query.wikidata.org/sparql> {
            ?wd wdt:P1831 ?electorate .
            FILTER(?electorate > 1000000)
        }
        
        #?circle ^:electoralCircle ?ctx .
        #?ctx ^:servedDuring ?mop .
        #
        #?mop schema:name ?mopName ;
        #    :jobTitle ?jobTitle .
        #
        #FILTER(REGEX(?jobTitle, "universitári", "i"))
    }
    ORDER BY DESC(?electorate) # ?mopName
    """

def query_runner(g: Graph):
    print("=== 1. Quais os partidos com mais deputados sociólogos? ===")
    query_sociologia_party(g)
    print("=== 2. Qual a quantidade de academic titles por legislatura? ===")
    query_academic_titles_leg(g)

def main():
    g = Graph()
    g.parse("./resources/test.ttl", format="turtle")
    query_leg_electorate_area(g)

if __name__ == "__main__":
    main()


