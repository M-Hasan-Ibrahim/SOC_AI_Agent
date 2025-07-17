import React from "react";
import { ChevronDown, ChevronUp, CheckCircle, XCircle } from "lucide-react";
import SeverityBadge from "./SeverityBadge";
import IsolationBadge from "./IsolationBadge";

export default function ClosedAlertRow({ alert, onExpand, expanded }) {
  // Handle artifacts_and_iocs (may be JSON/string/array)
  let artifacts = [];
  if (alert.artifacts_and_iocs) {
    if (Array.isArray(alert.artifacts_and_iocs)) {
      artifacts = alert.artifacts_and_iocs;
    } else {
      try {
        // try parsing JSON
        artifacts = JSON.parse(alert.artifacts_and_iocs);
      } catch {
        artifacts = typeof alert.artifacts_and_iocs === "string"
          ? [alert.artifacts_and_iocs]
          : [];
      }
    }
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="font-mono text-sm text-gray-600">
            #{alert.alert_id}
          </span>
          <IsolationBadge isolated={alert.isolation === "yes" || alert.isolation === true} />
          <div className="flex items-center gap-1">
            {alert.true_positive ? (
              <CheckCircle className="h-4 w-4 text-green-500" />
            ) : (
              <XCircle className="h-4 w-4 text-red-500" />
            )}
            <span className="text-sm text-gray-600">
              {alert.true_positive ? "True Positive" : "False Positive"}
            </span>
          </div>
          <span className="text-sm text-gray-600">{alert.attack_type}</span>
          <SeverityBadge severity={alert.severity} />
          <span className="text-sm text-gray-500">
            {artifacts.length ? `${artifacts.length} IOCs` : "0 IOCs"}
          </span>
        </div>
        <button
          onClick={() => onExpand(alert.alert_id)}
          className="text-gray-500 hover:text-gray-700"
        >
          {expanded ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </button>
      </div>
      {expanded && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-800 mb-2">Summary</h4>
              <p className="text-sm text-gray-600">{alert.summary}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-800 mb-2">Reasoning</h4>
              <p className="text-sm text-gray-600">{alert.reasoning}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-800 mb-2">Recommendations</h4>
              <p className="text-sm text-gray-600">{alert.recommendations}</p>
            </div>
            {artifacts.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">IOCs/Artifacts</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {artifacts.map((artifact, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-50 p-2 rounded text-sm font-mono"
                    >
                      {artifact}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
