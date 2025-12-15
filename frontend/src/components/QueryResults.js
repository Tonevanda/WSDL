import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { ArrowLeft, Loader2, AlertCircle } from 'lucide-react';

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
        <Card>
          <CardContent className="pt-6">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Parliamentary Group</TableHead>
                  <TableHead>MPs with Sociology Habilitation</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((row, idx) => (
                  <TableRow key={idx}>
                    <TableCell className="font-medium">{row.party}</TableCell>
                    <TableCell>{row.total}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      );
    }

    // Query 2: Academic titles per legislature
    if (queryId === '2') {
      return (
        <Card>
          <CardContent className="pt-6">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Legislature</TableHead>
                  <TableHead>Total Academic Titles</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((row, idx) => (
                  <TableRow key={idx}>
                    <TableCell className="font-medium">{row.legislature}</TableCell>
                    <TableCell>{row.total}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      );
    }

    // Query 3: Electoral circles info
    if (queryId === '3') {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {results.map((row, idx) => (
            <Card key={idx}>
              <CardHeader>
                <CardTitle className="text-xl">{row.circleName}</CardTitle>
              </CardHeader>
              <CardContent>
                <dl className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <dt className="font-medium text-gray-600">Voters:</dt>
                    <dd className="text-gray-900">{row.voters.toLocaleString()}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium text-gray-600">Area:</dt>
                    <dd className="text-gray-900">{row.area}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium text-gray-600">Permanent MPs:</dt>
                    <dd className="text-gray-900">{row.permanentMPs}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium text-gray-600">Academic Titles:</dt>
                    <dd className="text-gray-900">{row.academicTitles}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium text-gray-600">Duties:</dt>
                    <dd className="text-gray-900">{row.duties}</dd>
                  </div>
                  <div className="pt-2 border-t">
                    <dt className="font-medium text-gray-600 mb-1">Parliamentary Groups:</dt>
                    <dd className="text-gray-900 text-xs">{row.parties}</dd>
                  </div>
                </dl>
              </CardContent>
            </Card>
          ))}
        </div>
      );
    }

    // Query 4: Law habilitation by party and legislature
    if (queryId === '4') {
      return (
        <div className="space-y-6">
          {Object.entries(results).map(([legislature, parties]) => (
            <Card key={legislature}>
              <CardHeader>
                <CardTitle>{legislature}</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Parliamentary Group</TableHead>
                      <TableHead>MPs with Law Habilitation</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {parties.map((party, idx) => (
                      <TableRow key={idx}>
                        <TableCell className="font-medium">{party.party}</TableCell>
                        <TableCell>{party.total}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          ))}
        </div>
      );
    }

    // Query 5: MPs who changed situation
    if (queryId === '5') {
      return (
        <div className="space-y-6">
          {Object.entries(results).map(([legislature, parties]) => (
            <Card key={legislature}>
              <CardHeader>
                <CardTitle>{legislature}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {Object.entries(parties).map(([party, mps]) => (
                  <div key={party}>
                    <h4 className="font-semibold text-lg mb-3 text-gray-700">{party}</h4>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Name</TableHead>
                          <TableHead>Job</TableHead>
                          <TableHead>Status Change</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {mps.map((mp, idx) => (
                          <TableRow key={idx}>
                            <TableCell className="font-medium">{mp.name}</TableCell>
                            <TableCell>{mp.job}</TableCell>
                            <TableCell>{mp.change}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ))}
              </CardContent>
            </Card>
          ))}
        </div>
      );
    }

    // Query 6: Gender ratio
    if (queryId === '6') {
      return (
        <Card>
          <CardContent className="pt-6">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Parliamentary Group</TableHead>
                  <TableHead>Men</TableHead>
                  <TableHead>Women</TableHead>
                  <TableHead>Total</TableHead>
                  <TableHead>Ratio (M:F)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((row, idx) => (
                  <TableRow key={idx}>
                    <TableCell className="font-medium">{row.party}</TableCell>
                    <TableCell>{row.men}</TableCell>
                    <TableCell>{row.women}</TableCell>
                    <TableCell>{row.total}</TableCell>
                    <TableCell>{row.ratio}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      );
    }

    return <pre className="bg-gray-100 p-4 rounded-lg overflow-auto">{JSON.stringify(results, null, 2)}</pre>;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Button 
          variant="outline" 
          onClick={() => navigate('/')}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Queries
        </Button>

        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="h-12 w-12 animate-spin text-gray-400 mb-4" />
            <p className="text-gray-600">Running query {queryId}...</p>
          </div>
        )}

        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardHeader>
              <div className="flex items-center gap-2 text-red-700">
                <AlertCircle className="h-5 w-5" />
                <CardTitle>Error</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-red-700">{error}</p>
            </CardContent>
          </Card>
        )}

        {!loading && !error && data && (
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              Query {queryId}: {data.title}
            </h2>
            {renderResults()}
          </div>
        )}
      </div>
    </div>
  );
}

export default QueryResults;
