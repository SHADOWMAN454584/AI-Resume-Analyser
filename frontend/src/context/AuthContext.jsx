import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authAPI } from '../api/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('resumeai_token'));
  const [loading, setLoading] = useState(true);

  const isAuthenticated = !!token && !!user;

  // Load profile on mount if token exists
  useEffect(() => {
    const loadUser = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await authAPI.getProfile();
        setUser(res.data.user || res.data);
      } catch (err) {
        console.error('Failed to load profile:', err);
        localStorage.removeItem('resumeai_token');
        localStorage.removeItem('resumeai_user');
        setToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, [token]);

  const login = useCallback(async (email, password) => {
    const res = await authAPI.login({ email, password });
    const { access_token, user: userData } = res.data;
    localStorage.setItem('resumeai_token', access_token);
    setToken(access_token);
    setUser(userData || null);
    if (!userData) {
      try {
        const profileRes = await authAPI.getProfile();
        setUser(profileRes.data.user || profileRes.data);
      } catch { /* profile will load via effect */ }
    }
    return res.data;
  }, []);

  const register = useCallback(async (username, email, password) => {
    const res = await authAPI.register({ username, email, password });
    const { access_token, user: userData } = res.data;
    if (access_token) {
      localStorage.setItem('resumeai_token', access_token);
      setToken(access_token);
      setUser(userData || null);
    }
    return res.data;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('resumeai_token');
    localStorage.removeItem('resumeai_user');
    setToken(null);
    setUser(null);
  }, []);

  const value = {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
