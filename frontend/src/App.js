import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardHome from './components/DashboardHome';
import BankDashboard from './components/BankDashboard';
import CommandsList from './components/CommandsList';
import UpdatesPage from './components/UpdatesPage';
import NotFound from './components/NotFound';
import { ToastProvider } from './context/ToastContext';
import './App.css';

function App() {
  return (
    <ToastProvider>
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Layout>
          <Routes>
            <Route path="/" element={<DashboardHome />} />
            <Route path="/bank" element={<BankDashboard />} />
            <Route path="/commands" element={<CommandsList />} />
            <Route path="/updates" element={<UpdatesPage />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Router>
    </ToastProvider>
  );
}

export default App;