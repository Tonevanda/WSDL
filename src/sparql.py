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
        print(f"{row.party} has {row.total} MPs with a Sociology Habilitation")
    
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
    
    for row in g.query(query):
        print(f"{row.legDesc} has a total of {row.total} academic titles")

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
   
    for row in g.query(query_area):
        area = f"{int(row.area):,} km²" if row.area else "N/A"
        print(f"\n{row.circleName}")
        print(f"  Voters: {int(row.electorate):,}")
        print(f"  Area: {area}")
        print(f"  Permanent MPs: {row.totalMoPs}")
        print(f"  Academic Titles: {row.totalTitles}")
        print(f"  Duties: {row.totalDuties}")
        print(f"  Parliamentary Groups: {row.parties}")

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
        results[row.legDesc].append((row.party, row.total))
    
    for leg, parties in results.items():
        print(f"\n{leg}:")
        for party, total in parties:
            print(f"  {party} - {total} MPs with a Law habilitation")

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
            'name': row.name,
            'job': job,
            'change': f"Efetivo -> {row.sitLabel}"
        })
    
    for leg, parties in results.items():
        print(f"\n{leg}:")
        for party, mps in parties.items():
            print(f"  {party}:")
            for mp in mps:
                print(f"    {mp['name']} - {mp['job']} - {mp['change']}")
    
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
    
    print(f"{'Parliamentary Group':<30} {'Men':<10} {'Women':<10} {'Total':<10} {'Ratio (M:F)'}")
    print("=" * 80)
    
    for row in g.query(query):
        total_male = int(row.totalMale)
        total_female = int(row.totalFemale)
        total = total_male + total_female
        
        if total_female > 0:
            ratio = f"{total_male}:{total_female} ({total_male/total_female:.2f}:1)"
        else:
            ratio = f"{total_male}:0"
        
        print(f"{row.party:<30} {total_male:<10} {total_female:<10} {total:<10} {ratio}")

def query_runner(g: Graph):
    print("=== 1. How many MP's with a Sociology Habilitation has each Parliamentary Group had? ===")
    query_sociologia_party(g)
    print("\n=== 2. How many Academic Titles are in each Legislature? ===")
    query_academic_titles_leg(g)
    print("\n=== 3. Relevant information retrieval about Electoral Circles with >1M electorate (according to WikiData), during the XVII Legislature ===")
    query_leg_electorate_area(g)
    print("\n=== 4. Per Legislature, how many MPs per Parliamentary Group, whose most recent situation was as Permanent, have a Law Habilitation ===")
    query_party_efetivo_direito_leg(g)
    print("\n=== 5. Per Legislature, which MPs from which Parliamentary Group, started as Permanent but aren't permanent as the latest situation and what jobs do they have? ===")
    query_mp_change_metadata(g)
    print("\n=== 6. Overall Ratio Man vs Woman per Parliamentary Group ===")
    query_ratio(g)

def main():
    g = Graph()
    g.parse("./resources/poliontology_full.ttl", format="turtle")
    #query_ratio(g)
    query_runner(g)

if __name__ == "__main__":
    main()


