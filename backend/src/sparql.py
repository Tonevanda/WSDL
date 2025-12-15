from rdflib import *
import json
import sys
import os

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

    results = []
    for row in g.query(query):
        results.append({
            "party": str(row.party),
            "total": int(row.total),
            "description": f"{row.party} has {row.total} MPs with a Sociology Habilitation"
        })
    return results
    
def query_academic_titles_leg(g: Graph):
     # Qual a quantidade de academic titles por legislatura
    query = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?legDesc (COUNT(?title) as ?total)
    WHERE {
        ?mop a :MoP ;
            :academicTitle ?title ;
            :servedDuring ?ctx .
        
        ?ctx :legislature ?leg .
        ?leg rdfs:label ?legDesc .
        FILTER(LANG(?legDesc) = 'pt')
    }
    GROUP BY ?leg
    ORDER BY DESC(?total)
    """
    
    results = []
    for row in g.query(query):
        results.append({
            "legislature": str(row.legDesc),
            "total": int(row.total),
            "description": f"{row.legDesc} has a total of {row.total} academic titles"
        })
    return results

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
           (COUNT(?title) as ?totalTitles)
           (COUNT(?duty) as ?totalDuties)
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
            ?mop :academicTitle ?title .
        }
        
        OPTIONAL {
            ?context :duty ?duty .
        }
    }
    GROUP BY ?circleName ?electorate ?area
    ORDER BY DESC(?electorate)
    """
   
    results = []
    for row in g.query(query_area):
        area = f"{int(row.area):,} km²" if row.area else "N/A"
        results.append({
            "circleName": str(row.circleName),
            "voters": int(row.electorate),
            "area": area,
            "permanentMPs": int(row.totalMoPs),
            "academicTitles": int(row.totalTitles),
            "duties": int(row.totalDuties),
            "parties": str(row.parties)
        })
    return results

def query_party_efetivo_direito_leg(g: Graph):
    # Por partido quantos deputados efetivos tem habilitacao "direito" por legislatura
    query = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX schema: <https://schema.org/>

    SELECT ?legDesc ?party (COUNT(DISTINCT ?mop) as ?total)
    WHERE {
        ?hab a :Habilitation ;
            rdfs:label ?habName .
        FILTER(REGEX(?habName, "direito", "i"))

        ?hab ^:habilitation ?mop .
        ?mop :servedDuring ?ctx .
        
        ?ctx :legislature ?leg ;
             :membership ?mem ;
             :situation ?sit .
        
        ?leg rdfs:label ?legDesc .
        FILTER(LANG(?legDesc) = 'pt')
        
        ?sit :situationType :Efetivo ;
            schema:startDate ?start .

        FILTER NOT EXISTS {
            ?ctx :situation ?otherSit .
            ?otherSit schema:startDate ?otherStart .
            FILTER(?otherStart > ?start)
        }
        
        ?mem :group ?group .
        ?group skos:altLabel ?party .
    }
    GROUP BY ?legDesc ?party
    ORDER BY ?legDesc DESC(?total)
    """

    results = {}
    for row in g.query(query):
        if row.legDesc not in results:
            results[row.legDesc] = []
        results[row.legDesc].append({
            "party": str(row.party),
            "total": int(row.total)
        })
    
    return results

def query_mp_change_metadata(g: Graph):
    # MPs who changed situation status - started Efetivo but ended differently
    query = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX schema: <https://schema.org/>
    SELECT ?name ?job ?party ?legDesc ?sitLabel
    WHERE{
        ?mop a ?MoP ;
            schema:name ?name ;
            :servedDuring ?ctx .
        OPTIONAL {
            ?mop schema:jobTitle ?job .
        }
        
        ?ctx :legislature ?leg ;
            :membership ?mem ;
            :situation ?sit .
        
        ?leg rdfs:label ?legDesc .
        FILTER(LANG(?legDesc) = 'pt')
        
        ?sit :situationType :Efetivo ;
            schema:startDate ?start .
        
        # There is no earlier situation than this Efetivo one
        FILTER NOT EXISTS {
            ?ctx :situation ?otherSit1 .
            ?otherSit1 schema:startDate ?otherStart1 .
            FILTER(?otherStart1 < ?start)
        }
        
        # The latest (most recent) situation must NOT be Efetivo
        ?ctx :situation ?latestSit .
        ?latestSit :situationType ?latestSitType ;
            schema:startDate ?latestStart .
        
        FILTER NOT EXISTS {
            ?ctx :situation ?evenLaterSit .
            ?evenLaterSit schema:startDate ?evenLaterStart .
            FILTER(?evenLaterStart > ?latestStart)
        }
        
        FILTER(?latestSitType != :Efetivo)
        
        ?latestSitType skos:prefLabel ?sitLabel .
        
        ?mem :group ?group .
        ?group skos:altLabel ?party .
    }
    ORDER BY ?legDesc ?party
    """

    results = {}
    for row in g.query(query):
        if row.legDesc not in results:
            results[row.legDesc] = {}
        if row.party not in results[row.legDesc]:
            results[row.legDesc][row.party] = []
        
        job = row.job if row.job else "N/A"
        results[row.legDesc][row.party].append({
            'name': str(row.name),
            'job': str(job),
            'change': f"Efetivo -> {row.sitLabel}"
        })
    
    return results
    
def query_ratio(g: Graph):
    query = """
    PREFIX : <http://www.semanticweb.org/tiago/ontologies/2025/11/poliontology/>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?party 
           (COUNT(?mopMale) as ?totalMale)
           (COUNT(?mopFemale) as ?totalFemale)
           (IF(COUNT(?mopFemale) > 0, COUNT(?mopMale) /COUNT(?mopFemale), COUNT(?mopMale)) as ?ratio)
    WHERE {
        ?mop a :MoP ;
            :servedDuring ?ctx .
        
        ?ctx :membership ?mem .
        ?mem :group ?group .
        ?group skos:altLabel ?party .
        
        OPTIONAL {
            ?mop schema:gender ?m .
            FILTER(REGEX(?m, "M", "i"))
            BIND(?mop as ?mopMale)
        }
        
        OPTIONAL {
            ?mop schema:gender ?f .
            FILTER(REGEX(?f, "F", "i"))
            BIND(?mop as ?mopFemale)
        }
    }
    GROUP BY ?party
    ORDER BY ASC(?ratio)
    """
    
    results = []
    
    for row in g.query(query):
        total_male = int(row.totalMale)
        total_female = int(row.totalFemale)
        total = total_male + total_female
        
        if total_female > 0:
            ratio = f"{total_male}:{total_female} ({total_male/total_female:.2f}:1)"
            ratio_numeric = round(total_male/total_female, 2)
        else:
            ratio = f"{total_male}:0"
            ratio_numeric = total_male
        
        results.append({
            "party": str(row.party),
            "men": total_male,
            "women": total_female,
            "total": total,
            "ratio": ratio,
            "ratioNumeric": ratio_numeric
        })
    
    return results

def query_runner(g: Graph, query_number: int):
    """
    Run a specific query based on the query_number (1-6).
    Returns a dictionary with query metadata and results.
    """
    queries = {
        1: {
            "title": "How many MP's with a Sociology Habilitation has each Parliamentary Group had?",
            "function": query_sociologia_party
        },
        2: {
            "title": "How many Academic Titles are in each Legislature?",
            "function": query_academic_titles_leg
        },
        3: {
            "title": "Relevant information retrieval about Electoral Circles with >1M electorate (according to WikiData), during the XVII Legislature",
            "function": query_leg_electorate_area
        },
        4: {
            "title": "Per Legislature, how many MPs per Parliamentary Group, whose most recent situation was as Permanent, have a Law Habilitation",
            "function": query_party_efetivo_direito_leg
        },
        5: {
            "title": "Per Legislature, which MPs from which Parliamentary Group, started as Permanent but aren't permanent as the latest situation and what jobs do they have?",
            "function": query_mp_change_metadata
        },
        6: {
            "title": "Overall Ratio Man vs Woman per Parliamentary Group",
            "function": query_ratio
        }
    }
    
    if query_number not in queries:
        return {
            "error": f"Invalid query number. Please provide a number between 1 and 6.",
            "query_number": query_number
        }
    
    query_info = queries[query_number]
    results = query_info["function"](g)
    
    return {
        "query_number": query_number,
        "title": query_info["title"],
        "results": results
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python sparql.py <query_number>")
        print("Query numbers: 1-6")
        sys.exit(1)
    
    try:
        query_number = int(sys.argv[1])
    except ValueError:
        print("Error: Query number must be an integer between 1 and 6")
        sys.exit(1)
    
    g = Graph()
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build path to the resources directory (one level up, then into resources)
    ttl_path = os.path.join(os.path.dirname(script_dir), 'resources', 'poliontology_full.ttl')
    g.parse(ttl_path, format="turtle")
    
    result = query_runner(g, query_number)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()


