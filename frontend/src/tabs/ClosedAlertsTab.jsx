import React, { useState, useEffect } from 'react';
import { Loader2, RefreshCw } from 'lucide-react';
import { api } from '../api';
import ClosedAlertRow from '../components/ClosedAlertRow';

export default function ClosedAlertsTab() {
  const [closedAlerts, setClosedAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [error, setError] = useState(null);

  const fetchClosedAlerts = async () => {
    try {
      setLoading(true);
      const data = await api.get('/closed_alerts');
      setClosedAlerts(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch closed alerts');
    } finally {
      setLoading(false);
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
    fetchClosedAlerts();
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
        <h2 className="text-xl font-semibold text-gray-800">Closed Alerts</h2>
        <button
          onClick={fetchClosedAlerts}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
        >
          <RefreshCw className="h-4 w-4" />
          Refresh
        </button>
      </div>
      {closedAlerts.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No closed alerts</div>
      ) : (
        closedAlerts.map((alert) => (
          <ClosedAlertRow
            key={alert.alert_id}
            alert={alert}
            onExpand={handleExpand}
            expanded={expandedIds.has(alert.alert_id)}
          />
        ))
      )}
      {error && (
        <div className="text-red-600 text-center mt-4">{error}</div>
      )}
    </div>
  );
}
