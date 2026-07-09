// src/components/Navbar.tsx
"use client";

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { usePathname, useRouter } from 'next/navigation';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link href="/dashboard" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">AI</div>
            <span className="font-bold text-gray-900 text-xl tracking-tight">SkinAI</span>
          </Link>

          {user && (
            <div className="hidden md:flex items-center space-x-8">
              <Link href="/dashboard" className={`${pathname === '/dashboard' ? 'text-blue-600 font-medium' : 'text-gray-500 hover:text-gray-900'} transition`}>
                Analyze
              </Link>
              <Link href="/history" className={`${pathname === '/history' ? 'text-blue-600 font-medium' : 'text-gray-500 hover:text-gray-900'} transition`}>
                History
              </Link>
            </div>
          )}

          {user && (
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500 hidden sm:block">Hi, {user.name.split(' ')[0]}</span>
              <button
                onClick={handleLogout}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}