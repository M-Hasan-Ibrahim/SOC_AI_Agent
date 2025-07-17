import { useEffect } from 'react';
export default function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);
  const bgColor = type === 'error'
    ? 'bg-red-100 border-red-400 text-red-700'
    : 'bg-green-100 border-green-400 text-green-700';
  return (
    <div className={`fixed top-4 right-4 p-4 rounded-lg border ${bgColor} z-50`}>
      {message}
    </div>
  );
}
