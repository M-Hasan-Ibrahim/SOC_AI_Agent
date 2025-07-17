import React, { useState, useEffect } from 'react';
import { Loader2, RefreshCw } from 'lucide-react';
import { api } from '../api';
import LogBlock from '../components/LogBlock';

export default function LogsTab() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const data = await api.get('/logs');
      setLogs(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch logs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={fetchLogs}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-800">Logs</h2>
        <button
          onClick={fetchLogs}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
        >
          <RefreshCw className="h-4 w-4" />
          Refresh
        </button>
      </div>
      {logs.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No logs available</div>
      ) : (
        logs.map((log, index) => (
          <LogBlock key={index} log={log} />
        ))
      )}
    </div>
  );
}
