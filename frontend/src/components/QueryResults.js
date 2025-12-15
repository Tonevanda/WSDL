import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './QueryResults.css';

const API_BASE_URL = 'http://localhost:8000/api/queries';

function QueryResults() {
  const { queryId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    
    axios.get(`${API_BASE_URL}/run/${queryId}/`)
      .then(response => {
        setData(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.response?.data?.error || 'Failed to execute query');
        setLoading(false);
      });
  }, [queryId]);

  const renderResults = () => {
    if (!data || !data.results) return null;

    const results = data.results;

    // Query 1: Sociology by party
    if (queryId === '1') {
      return (
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Parliamentary Group</th>
                <th>MPs with Sociology Habilitation</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.party}</td>
                  <td>{row.total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    // Query 2: Academic titles per legislature
    if (queryId === '2') {
      return (
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Legislature</th>
                <th>Total Academic Titles</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.legislature}</td>
                  <td>{row.total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    // Query 3: Electoral circles info
    if (queryId === '3') {
      return (
        <div className="results-cards">
          {results.map((row, idx) => (
            <div key={idx} className="result-card">
              <h3>{row.circleName}</h3>
              <div className="card-content">
                <p><strong>Voters:</strong> {row.voters.toLocaleString()}</p>
                <p><strong>Area:</strong> {row.area}</p>
                <p><strong>Permanent MPs:</strong> {row.permanentMPs}</p>
                <p><strong>Academic Titles:</strong> {row.academicTitles}</p>
                <p><strong>Duties:</strong> {row.duties}</p>
                <p><strong>Parliamentary Groups:</strong> {row.parties}</p>
              </div>
            </div>
          ))}
        </div>
      );
    }

    // Query 4: Law habilitation by party and legislature
    if (queryId === '4') {
      return (
        <div className="results-nested">
          {Object.entries(results).map(([legislature, parties]) => (
            <div key={legislature} className="legislature-section">
              <h3>{legislature}</h3>
              <table>
                <thead>
                  <tr>
                    <th>Parliamentary Group</th>
                    <th>MPs with Law Habilitation</th>
                  </tr>
                </thead>
                <tbody>
                  {parties.map((party, idx) => (
                    <tr key={idx}>
                      <td>{party.party}</td>
                      <td>{party.total}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      );
    }

    // Query 5: MPs who changed situation
    if (queryId === '5') {
      return (
        <div className="results-nested">
          {Object.entries(results).map(([legislature, parties]) => (
            <div key={legislature} className="legislature-section">
              <h3>{legislature}</h3>
              {Object.entries(parties).map(([party, mps]) => (
                <div key={party} className="party-section">
                  <h4>{party}</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Job</th>
                        <th>Status Change</th>
                      </tr>
                    </thead>
                    <tbody>
                      {mps.map((mp, idx) => (
                        <tr key={idx}>
                          <td>{mp.name}</td>
                          <td>{mp.job}</td>
                          <td>{mp.change}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          ))}
        </div>
      );
    }

    // Query 6: Gender ratio
    if (queryId === '6') {
      return (
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Parliamentary Group</th>
                <th>Men</th>
                <th>Women</th>
                <th>Total</th>
                <th>Ratio (M:F)</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.party}</td>
                  <td>{row.men}</td>
                  <td>{row.women}</td>
                  <td>{row.total}</td>
                  <td>{row.ratio}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    return <pre>{JSON.stringify(results, null, 2)}</pre>;
  };

  return (
    <div className="results-container">
      <button className="back-button" onClick={() => navigate('/')}>
        ← Back to Queries
      </button>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Running query {queryId}...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && data && (
        <div className="results-content">
          <h2>Query {queryId}: {data.title}</h2>
          {renderResults()}
        </div>
      )}
    </div>
  );
}

export default QueryResults;
