import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import QueryResults from './components/QueryResults';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results/:queryId" element={<QueryResults />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
