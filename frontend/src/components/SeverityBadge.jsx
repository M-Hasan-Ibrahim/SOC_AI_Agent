export default function SeverityBadge({ severity }) {
  const colors = {
    high: 'bg-red-100 text-red-800 border-red-200',
    medium: 'bg-orange-100 text-orange-800 border-orange-200',
    low: 'bg-green-100 text-green-800 border-green-200',
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${colors[severity] || colors.medium}`}>
      {severity || 'Unknown'}
    </span>
  );
}
