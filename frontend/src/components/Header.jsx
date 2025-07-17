import { Shield } from 'lucide-react';
export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center gap-3">
        <Shield className="h-8 w-8 text-blue-600" />
        <h1 className="text-2xl font-bold text-gray-800">SOC_AI_Agent</h1>
        <h6>By Mohamad Hassan Ibrahim & Reem Kanaan</h6>
      </div>
    </header>
  );
}
