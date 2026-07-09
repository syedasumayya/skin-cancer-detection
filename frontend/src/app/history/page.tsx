"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import api from '@/lib/api';
import { HistoryItem } from '@/types';

export default function HistoryPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    } else if (user) {
      const fetchHistory = async () => {
        try {
          const res = await api.get<HistoryItem[]>('/api/history');
          setHistory(res.data);
        } catch (err) {
          console.error("Failed to fetch history");
        } finally {
          setIsLoading(false);
        }
      };

      fetchHistory();
    }
  }, [user, authLoading, router]);

  if (authLoading || isLoading) return <div className="flex justify-center items-center h-[80vh]"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;
  if (!user) return null;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Scan History</h1>
        <p className="text-gray-500 mt-1">Your previous skin lesion analyses.</p>
      </div>

      {history.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center shadow-sm border border-gray-100">
          <p className="text-gray-400 text-lg">No scans yet.</p>
          <button onClick={() => router.push('/dashboard')} className="mt-4 text-blue-600 font-medium hover:underline">Go to Analyze</button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {history.map((item) => (
            <div key={item.id} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-bold text-gray-900">{item.prediction}</h3>
                <span className={`px-2 py-1 text-xs font-bold rounded ${item.risk_level === 'High' ? 'bg-red-100 text-red-700' : item.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>
                  {item.risk_level}
                </span>
              </div>
              <div className="text-2xl font-bold text-blue-600 mb-4">{item.confidence.toFixed(1)}%</div>
              <p className="text-xs text-gray-400">{new Date(item.analyzed_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}