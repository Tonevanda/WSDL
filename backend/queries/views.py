from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import subprocess
import json
import os

@api_view(['GET'])
def run_query(request, query_number):
    """
    Run a SPARQL query by calling sparql.py with the query number.
    """
    if query_number not in range(1, 7):
        return Response(
            {"error": "Invalid query number. Must be between 1 and 6."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get the path to sparql.py
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sparql_path = os.path.join(base_dir, 'src', 'sparql.py')
        
        # Get the project root (one level up from backend)
        project_root = os.path.dirname(base_dir)
        
        # Run the sparql.py script with the query number using uv
        result = subprocess.run(
            ['uv', 'run', 'python', sparql_path, str(query_number)],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return Response(
                {
                    "error": "Query execution failed",
                    "details": result.stderr
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Parse the JSON output from sparql.py
        try:
            data = json.loads(result.stdout)
            return Response(data, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response(
                {
                    "error": "Failed to parse query results",
                    "details": result.stdout
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except subprocess.TimeoutExpired:
        return Response(
            {"error": "Query execution timed out"},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except Exception as e:
        return Response(
            {
                "error": "An unexpected error occurred",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def list_queries(request):
    """
    List all available queries.
    """
    queries = [
        {
            "id": 1,
            "title": "How many MP's with a Sociology Habilitation has each Parliamentary Group had?"
        },
        {
            "id": 2,
            "title": "How many Academic Titles are in each Legislature?"
        },
        {
            "id": 3,
            "title": "Relevant information retrieval about Electoral Circles with >1M electorate (according to WikiData), during the XVII Legislature"
        },
        {
            "id": 4,
            "title": "Per Legislature, how many MPs per Parliamentary Group, whose most recent situation was as Permanent, have a Law Habilitation"
        },
        {
            "id": 5,
            "title": "Per Legislature, which MPs from which Parliamentary Group, started as Permanent but aren't permanent as the latest situation and what jobs do they have?"
        },
        {
            "id": 6,
            "title": "Overall Ratio Man vs Woman per Parliamentary Group"
        }
    ]
    
    return Response({"queries": queries}, status=status.HTTP_200_OK)
