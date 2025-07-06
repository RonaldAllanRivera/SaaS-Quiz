'use client';

import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';

export default function Home() {
  const { isAuthenticated, logout, loading, userEmail } = useAuth();

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50">
        <p className="text-lg text-gray-600">Loading...</p>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">QuizNest 🐣</h1>
        <p className="mt-2 text-lg text-gray-600">AI-Powered Quiz Playground for Kids</p>
        
        <div className="mt-8">
          {isAuthenticated ? (
            <div className="text-center">
              <p className="text-xl text-gray-800">Welcome back {userEmail || 'User'}!</p>
              <button
                onClick={logout}
                className="mt-4 px-6 py-2 font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="px-6 py-3 font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Parent Login
            </Link>
          )}
        </div>
      </div>
    </main>
  );
}
