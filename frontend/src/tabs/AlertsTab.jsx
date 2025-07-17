import React, { useState, useEffect } from 'react';
import { Loader2, RefreshCw } from 'lucide-react';
import { api } from '../api';
import AlertRow from '../components/AlertRow';

export default function AlertsTab({ onDataChange }) {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analyzingAll, setAnalyzingAll] = useState(false);
  const [analyzingIds, setAnalyzingIds] = useState(new Set());
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [error, setError] = useState(null);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const data = await api.get('/alerts');
      setAlerts(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch alerts');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async (alertId) => {
    try {
      setAnalyzingIds(prev => new Set([...prev, alertId]));
      await api.post(`/alerts/${alertId}/analyze`);
      await fetchAlerts();
      onDataChange && onDataChange();
    } catch (err) {
      setError(`Failed to analyze alert ${alertId}`);
    } finally {
      setAnalyzingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(alertId);
        return newSet;
      });
    }
  };

  const handleAnalyzeAll = async () => {
    try {
      setAnalyzingAll(true);
      await api.post('/alerts/analyze_all');
      await fetchAlerts();
      onDataChange && onDataChange();
    } catch (err) {
      setError('Failed to analyze all alerts');
    } finally {
      setAnalyzingAll(false);
    }
  };

  const handleExpand = (alertId) => {
    setExpandedIds(prev => {
      const newSet = new Set(prev);
      if (newSet.has(alertId)) {
        newSet.delete(alertId);
      } else {
        newSet.add(alertId);
      }
      return newSet;
    });
  };

  useEffect(() => {
    fetchAlerts();
    // eslint-disable-next-line
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-800">Open Alerts</h2>
        <div className="flex items-center gap-2">
          <button
            onClick={handleAnalyzeAll}
            disabled={analyzingAll || alerts.length === 0}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {analyzingAll ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
            Analyze All
          </button>
          <button
            onClick={fetchAlerts}
            className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
        </div>
      </div>
      {alerts.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No open alerts</div>
      ) : (
        alerts.map((alert) => (
          <AlertRow
            key={alert.id}
            alert={alert}
            onAnalyze={handleAnalyze}
            onExpand={handleExpand}
            expanded={expandedIds.has(alert.id)}
            loading={analyzingIds.has(alert.id)}
          />
        ))
      )}
      {error && (
        <div className="text-red-600 text-center mt-4">{error}</div>
      )}
    </div>
  );
}
