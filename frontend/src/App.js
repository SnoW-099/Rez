import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardHome from './components/DashboardHome';
import BankDashboard from './components/BankDashboard';
import CommandsList from './components/CommandsList';
import UpdatesPage from './components/UpdatesPage';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardHome />} />
          <Route path="/bank" element={<BankDashboard />} />
          <Route path="/commands" element={<CommandsList />} />
          <Route path="/updates" element={<UpdatesPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;