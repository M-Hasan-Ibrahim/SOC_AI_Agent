import React, { useState } from 'react';
import Header from './components/Header';
import TabNav from './components/TabNav';
import Toast from './components/Toast';
import LogsTab from './tabs/LogsTab';
import AlertsTab from './tabs/AlertsTab';
import ClosedAlertsTab from './tabs/ClosedAlertsTab';
import './index.css';

export default function App() {
  

  const [activeTab, setActiveTab] = useState('logs');
  const [toast, setToast] = useState(null);
  const [dataVersion, setDataVersion] = useState(0);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  const handleDataChange = () => {
    setDataVersion(prev => prev + 1);
  };

  return (
    
    <div className="min-h-screen bg-gray-50">
      <Header />
      <TabNav activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="p-6">
        <div className="max-w-7xl mx-auto">
          {activeTab === 'logs' && <LogsTab key={`logs-${dataVersion}`} />}
          {activeTab === 'alerts' && (
            <AlertsTab key={`alerts-${dataVersion}`} onDataChange={handleDataChange} />
          )}
          {activeTab === 'closed' && (
            <ClosedAlertsTab key={`closed-${dataVersion}`} />
          )}
        </div>
      </main>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}
