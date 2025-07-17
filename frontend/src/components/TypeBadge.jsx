export default function TypeBadge({ type }) {
  const colors = {
    firewall: 'bg-blue-100 text-blue-800 border-blue-200',
    sysmon: 'bg-green-100 text-green-800 border-green-200',
    default: 'bg-gray-100 text-gray-800 border-gray-200',
  };
  const colorClass = colors[type] || colors.default;
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${colorClass}`}>
      {type || 'Unknown'}
    </span>
  );
}
