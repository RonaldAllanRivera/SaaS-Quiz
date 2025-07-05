'use client';

import { AuthProvider } from '@/contexts/AuthContext';
import { GoogleOAuthProvider } from '@react-oauth/google';
import React from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const googleClientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  return (
    <AuthProvider>
      {googleClientId ? (
        <GoogleOAuthProvider clientId={googleClientId}>
          {children}
        </GoogleOAuthProvider>
      ) : (
        <>
          {/* Google Login is disabled because NEXT_PUBLIC_GOOGLE_CLIENT_ID is not set. */}
          {children}
        </>
      )}
    </AuthProvider>
  );
}
