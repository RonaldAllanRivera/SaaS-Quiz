'use client';

import { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useGoogleLogin } from '@react-oauth/google';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();
  const router = useRouter();

  const handleLoginError = (error: any) => {
    let errorMessage = 'An unknown error occurred.';
    if (axios.isAxiosError(error) && error.response) {
        // If the backend sends a specific error message, use it.
        errorMessage = JSON.stringify(error.response.data);
    } else if (error instanceof Error) {
        // Otherwise, use the error's message property.
        errorMessage = error.message;
    }
    setError(`Google login failed: ${errorMessage}`);
    console.error('Login Failed:', error);
  };

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      try {
        const googleAccessToken = tokenResponse.access_token;
        const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/auth/google/`;
        
        const response = await axios.post(apiUrl, {
          access_token: googleAccessToken,
        });

        if (response.data.key) { // dj-rest-auth returns a 'key' for token auth
          login(response.data.key);
          router.push('/'); // Redirect to homepage
        } else {
          handleLoginError(new Error('Login response did not contain a key.'));
        }
      } catch (error) {
        handleLoginError(error);
      }
    },
    onError: handleLoginError,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
            const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api-token-auth/`;
      const response = await axios.post(apiUrl, {
        username,
        password,
      });

      if (response.data.token) {
        login(response.data.token);
        router.push('/'); // Redirect to homepage on successful login
      } else {
        setError('Login failed. Please check your credentials.');
      }
    } catch (err) {
      setError('Login failed. Please check your credentials or try again later.');
      console.error(err);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-gray-900">Welcome Back</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="username" className="text-sm font-medium text-gray-700">
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label htmlFor="password"className="text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div>
            <button
              type="submit"
              className="w-full px-4 py-2 font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign In
            </button>
          </div>
        </form>

        <div className="relative my-4">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or continue with</span>
          </div>
        </div>

        <div className="space-y-4">
          <button
            onClick={() => handleGoogleLogin()}
            type="button"
            className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
          >
            <svg className="w-5 h-5 mr-2" viewBox="0 0 48 48">
              <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039L38.804 12.8C34.661 8.969 29.698 6 24 6C12.955 6 4 14.955 4 26s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z" />
              <path fill="#FF3D00" d="M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039L38.804 12.8C34.661 8.969 29.698 6 24 6C16.318 6 9.656 10.083 6.306 14.691z" />
              <path fill="#4CAF50" d="M24 46c5.698 0 10.661-2.969 14.804-7.2l-6.571-4.819C29.938 36.405 27.165 38 24 38c-5.223 0-9.651-3.444-11.127-8.169l-6.571 4.819C9.656 39.917 16.318 46 24 46z" />
              <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303c-.792 2.237-2.231 4.16-4.082 5.571l6.571 4.819C40.049 34.661 44 28.698 44 20c0-1.341-.138-2.65-.389-3.917z" />
            </svg>
            Sign in with Google
          </button>

          <button
            type="button"
            disabled
            className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 opacity-50 cursor-not-allowed"
          >
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M20 10c0-5.523-4.477-10-10-10S0 4.477 0 10c0 4.991 3.657 9.128 8.438 9.878V12.875H5.938v-2.875h2.5V7.65C8.438 5.1 10.031 3.5 12.438 3.5c1.113 0 2.063.082 2.344.118v2.5l-1.475.001c-1.238 0-1.475.588-1.475 1.45v1.8h2.781l-.363 2.875h-2.418V19.878C16.343 19.128 20 14.991 20 10z" clipRule="evenodd" />
            </svg>
            Sign in with Facebook
          </button>
        </div>

        <p className="mt-4 text-sm text-center text-gray-600">
          Don't have an account?{' '}
          <Link href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}
