"use client";

import { useState, useRef, useEffect, ChangeEvent, DragEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import api from '@/lib/api';
import { AnalysisResult } from '@/types';

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const handleFileSelect = (selectedFile: File) => {
    if (!selectedFile.type.startsWith('image/')) return;
    setFile(selectedFile);
    setResult(null);
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result as string);
    reader.readAsDataURL(selectedFile);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files[0]) handleFileSelect(e.dataTransfer.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post<AnalysisResult>('/api/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (_error) {
      setResult({
        success: false,
        is_valid_image: false,
        error_message: 'Failed to analyze image. Please try again.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading) return <div className="flex justify-center items-center h-[80vh]"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;
  if (!user) return null;

  // Calculate ALL CSS classes safely OUTSIDE of the JSX to avoid ESLint errors
  let dragBoxClass = "border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer transition-colors h-64 ";
  
  if (isDragging) {
    dragBoxClass += "border-blue-500 bg-blue-50";
  } else {
    dragBoxClass += "border-gray-300 hover:bg-gray-50";
  }

  let riskBoxClass = "p-4 rounded-xl border ";
  let riskBadgeClass = "px-3 py-1 rounded-full text-sm font-bold ";

  if (result && result.success) {
    if (result.risk_level === 'High') {
      riskBoxClass += "bg-red-50 border-red-200";
      riskBadgeClass += "bg-red-200 text-red-800";
    } else if (result.risk_level === 'Medium') {
      riskBoxClass += "bg-yellow-50 border-yellow-200";
      riskBadgeClass += "bg-yellow-200 text-yellow-800";
    } else {
      riskBoxClass += "bg-green-50 border-green-200";
      riskBadgeClass += "bg-green-200 text-green-800";
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Skin Lesion Analysis</h1>
        <p className="text-gray-500 mt-1">Upload a clear image of the skin lesion for AI analysis.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* LEFT: Upload Section */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold mb-4">Upload Image</h2>
          
          <div
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={dragBoxClass}
          >
            {preview ? (
              <img src={preview} alt="Preview" className="max-h-full max-w-full object-contain rounded-lg" />
            ) : (
              <div className="text-center text-gray-400">
                <svg className="mx-auto h-12 w-12 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                <p className="font-medium">Drag & Drop an image here</p>
                <p className="text-sm mt-1">or click to browse (JPG, PNG)</p>
              </div>
            )}
            <input type="file" ref={fileInputRef} onChange={(e: ChangeEvent<HTMLInputElement>) => e.target.files?.[0] && handleFileSelect(e.target.files[0])} className="hidden" accept="image/*" />
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!file || isLoading}
            className="mt-4 w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Analyzing...
              </>
            ) : (
              "Analyze Lesion"
            )}
          </button>
        </div>

        {/* RIGHT: Results Section */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold mb-4">Analysis Results</h2>
          
          {!result && (
            <div className="h-full flex items-center justify-center text-gray-400 text-center">
              <p>Upload an image and click <br/><span className="font-medium text-gray-600">Analyze Lesion</span> to see results</p>
            </div>
          )}

          {result && !result.success && (
            <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl">
              <h3 className="font-semibold text-red-800 mb-1">Invalid Image</h3>
              <p className="text-sm">{result.error_message}</p>
            </div>
          )}

          {result && result.success && (
            <div className="space-y-6">
              {/* Main Prediction */}
              <div className={riskBoxClass}>
                <p className="text-sm font-medium text-gray-500">Primary Prediction</p>
                <h3 className="text-2xl font-bold mt-1">{result.prediction}</h3>
                <div className="flex items-center gap-3 mt-2">
                  <span className="text-3xl font-bold text-gray-900">{result.confidence?.toFixed(1)}%</span>
                  <span className={riskBadgeClass}>
                    {result.risk_level} Risk
                  </span>
                </div>
              </div>

              {/* Confidence Bars */}
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-3">All Probabilities</h4>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {result.all_predictions?.map((pred) => (
                    <div key={pred.class_name} className="flex items-center gap-3">
                      <span className="text-xs text-gray-600 w-36 truncate">{pred.class_name}</span>
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${pred.confidence}%` }}></div>
                      </div>
                      <span className="text-xs font-medium text-gray-700 w-10 text-right">{pred.confidence.toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">Recommendations</h4>
                <ul className="space-y-2">
                  {result.recommendations?.map((rec, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                      <span className="text-blue-500 mt-0.5">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
              
              <p className="text-xs text-gray-400 border-t border-gray-100 pt-4">*AI simulation mode. Results are for demonstration purposes only.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}