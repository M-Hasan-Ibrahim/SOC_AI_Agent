export default function IsolationBadge({ isolated }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
      isolated ? 'bg-red-100 text-red-800 border-red-200' : 'bg-green-100 text-green-800 border-green-200'
    }`}>
      {isolated ? 'Isolated' : 'Not Isolated'}
    </span>
  );
}
