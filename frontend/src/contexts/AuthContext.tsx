'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

// Define the shape of the context data
interface AuthContextType {
  token: string | null;
  userEmail: string | null;
  isAuthenticated: boolean;
  login: (token: string, email?: string) => void;
  logout: () => void;
  loading: boolean;
}

// Create the context with a default value
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Create a provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Try to load token and email from localStorage on initial render
    const storedToken = localStorage.getItem('authToken');
    const storedEmail = localStorage.getItem('userEmail');
    
    if (storedToken) {
      setToken(storedToken);
      setUserEmail(storedEmail);
      axios.defaults.headers.common['Authorization'] = `Token ${storedToken}`;
    }
    setLoading(false);
  }, []);

  const login = (newToken: string, email?: string) => {
    setToken(newToken);
    if (email) {
      setUserEmail(email);
      localStorage.setItem('userEmail', email);
    }
    localStorage.setItem('authToken', newToken);
    axios.defaults.headers.common['Authorization'] = `Token ${newToken}`;
  };

  const logout = () => {
    setToken(null);
    setUserEmail(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    token,
    userEmail,
    isAuthenticated: !!token,
    login,
    logout,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};


