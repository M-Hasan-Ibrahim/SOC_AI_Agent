import React from "react";
import { ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import SeverityBadge from "./SeverityBadge";
import { formatTimestamp, formatIPAddress } from "../utils";

export default function AlertRow({
  alert,
  onAnalyze,
  onExpand,
  expanded,
  loading,
}) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="font-mono text-sm text-gray-600">#{alert.id}</span>
          <span className="text-sm text-gray-500">
            {formatTimestamp(alert.timestamp)}
          </span>
          <div className="flex items-center gap-2">
            <span className="font-medium text-gray-800">
              {formatIPAddress(alert.source_ip)}
            </span>
            <span className="text-gray-400">→</span>
            <span className="font-medium text-gray-800">
              {formatIPAddress(alert.destination_ip)}
            </span>
          </div>
          <span className="text-sm text-gray-600">{alert.alert_type}</span>
          <SeverityBadge severity={alert.severity} />
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onAnalyze(alert.id)}
            disabled={loading}
            className="bg-blue-600 text-white px-3 py-1 rounded-md text-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
          >
            {loading ? <Loader2 className="h-3 w-3 animate-spin" /> : null}
            Analyze
          </button>
          <button
            onClick={() => onExpand(alert.id)}
            className="text-gray-500 hover:text-gray-700"
          >
            {expanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </button>
        </div>
      </div>
      {expanded && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(alert).map(([key, value]) => (
              <div key={key} className="flex flex-col">
                <span className="text-sm font-medium text-gray-500 capitalize">
                  {key.replace("_", " ")}
                </span>
                <span className="text-sm text-gray-800">{String(value)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
