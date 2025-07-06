'use client';

import { useContext } from 'react';
import { AuthContext } from '@/contexts/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Extend the AuthContextType to include userEmail
declare module '@/contexts/AuthContext' {
  interface AuthContextType {
    userEmail: string | null;
  }
}
