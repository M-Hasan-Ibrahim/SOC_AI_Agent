import { formatTimestamp, formatIPAddress } from '../utils';
import TypeBadge from './TypeBadge';

export default function LogBlock({ log }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="font-bold text-gray-800">{formatIPAddress(log.source_address)}</span>
          <span className="text-gray-400">→</span>
          <span className="font-bold text-gray-800">{formatIPAddress(log.destination_address)}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-500">{formatTimestamp(log.timestamp)}</span>
          <TypeBadge type={log.type} />
        </div>
      </div>
    </div>
  );
}
