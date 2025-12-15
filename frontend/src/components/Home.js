import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Database, Loader2, AlertCircle } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api/queries';

function Home() {
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API_BASE_URL}/list/`)
      .then(response => {
        setQueries(response.data.queries);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load queries. Make sure the backend server is running.');
        setLoading(false);
      });
  }, []);

  const handleQueryClick = (queryId) => {
    navigate(`/results/${queryId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600">Loading queries...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <div className="flex items-center gap-2 text-red-600 mb-2">
              <AlertCircle className="h-5 w-5" />
              <CardTitle>Error</CardTitle>
            </div>
            <CardDescription className="text-red-600">{error}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Database className="h-10 w-10 text-gray-700" />
            <h1 className="text-4xl font-bold text-gray-900">WSDL Query Interface</h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Select a SPARQL query to explore Portuguese parliamentary data
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {queries.map((query) => (
            <Card 
              key={query.id}
              className="cursor-pointer transition-all hover:shadow-lg hover:-translate-y-1"
              onClick={() => handleQueryClick(query.id)}
            >
              <CardHeader>
                <div className="flex items-start justify-between mb-2">
                  <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Query {query.id}
                  </span>
                </div>
                <CardDescription className="text-gray-700 text-sm leading-relaxed">
                  {query.title}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;
