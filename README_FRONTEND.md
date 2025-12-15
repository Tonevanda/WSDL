# WSDL Frontend & Backend

This project consists of a Django backend and React frontend for querying SPARQL data.

## Project Structure

```
WSDL/
├── backend/
│   ├── src/                    # Python source code including sparql.py
│   ├── resources/              # RDF data files
│   ├── wsdl_backend/           # Django project
│   ├── queries/                # Django app for API endpoints
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   └── App.js
│   └── package.json
└── README.md
```

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies (if using uv):
```bash
cd .. && uv add django djangorestframework django-cors-headers
```

3. Run migrations:
```bash
uv run python manage.py migrate
```

4. Start the Django development server:
```bash
uv run python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### API Endpoints

- `GET /api/queries/list/` - Get list of all available queries
- `GET /api/queries/run/<query_number>/` - Run a specific query (1-6)

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Start both the backend (port 8000) and frontend (port 3000) servers
2. Open your browser to `http://localhost:3000`
3. Click on any of the 6 query buttons to execute SPARQL queries
4. View the results on the results page

## Queries

1. How many MP's with a Sociology Habilitation has each Parliamentary Group had?
2. How many Academic Titles are in each Legislature?
3. Electoral Circles information with >1M electorate (XVII Legislature)
4. MPs per Parliamentary Group with Law Habilitation (by Legislature)
5. MPs who changed from Permanent status (by Legislature and Party)
6. Overall Gender Ratio per Parliamentary Group
