import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Home.css';

const API_BASE_URL = 'http://localhost:8000/api/queries';

function Home() {
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the list of available queries
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
      <div className="home-container">
        <h1>WSDL Query Interface</h1>
        <p>Loading queries...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home-container">
        <h1>WSDL Query Interface</h1>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="home-container">
      <h1>WSDL Query Interface</h1>
      <p className="subtitle">Select a query to run:</p>
      
      <div className="queries-grid">
        {queries.map((query) => (
          <div 
            key={query.id} 
            className="query-card"
            onClick={() => handleQueryClick(query.id)}
          >
            <div className="query-number">Query {query.id}</div>
            <div className="query-title">{query.title}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
