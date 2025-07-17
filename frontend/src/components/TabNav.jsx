import { Activity, AlertTriangle, CheckCircle } from 'lucide-react';

export default function TabNav({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'logs', name: 'Logs', icon: Activity },
    { id: 'alerts', name: 'Alerts', icon: AlertTriangle },
    { id: 'closed', name: 'Closed Alerts', icon: CheckCircle },
  ];
  return (
    <nav className="bg-white border-b border-gray-200 px-6">
      <div className="flex space-x-8">
        {tabs.map(({ id, name, icon: Icon }) => (
          <button
            key={id}
            onClick={() => onTabChange(id)}
            className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <Icon className="h-4 w-4" />
            {name}
          </button>
        ))}
      </div>
    </nav>
  );
}
