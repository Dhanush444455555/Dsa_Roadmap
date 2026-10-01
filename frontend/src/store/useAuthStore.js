import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import apiClient from '../services/api';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      setLoading: (val) => set({ isLoading: val }),
      setError: (err) => set({ error: err }),
      clearError: () => set({ error: null }),

      login: async ({ name, email, date_of_birth, rememberMe }) => {
        set({ isLoading: true, error: null });
        try {
          const res = await apiClient.post('/api/auth/login', {
            name: name.trim(),
            email: email.trim().toLowerCase(),
            date_of_birth,
          });
          const { access_token, user } = res.data;
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
          set({
            token: access_token,
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          if (rememberMe) {
            localStorage.setItem('dsa_token', access_token);
          }
          return { success: true, user };
        } catch (err) {
          const message = err.response?.data?.detail || 'Authentication failed. Please check your details.';
          set({ isLoading: false, error: message });
          return { success: false, error: message };
        }
      },

      register: async ({ name, email, date_of_birth }) => {
        set({ isLoading: true, error: null });
        try {
          const res = await apiClient.post('/api/auth/register', {
            name: name.trim(),
            email: email.trim().toLowerCase(),
            date_of_birth,
          });
          const { access_token, user } = res.data;
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
          set({
            token: access_token,
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          return { success: true, user };
        } catch (err) {
          const message = err.response?.data?.detail || 'Registration failed. Please try again.';
          set({ isLoading: false, error: message });
          return { success: false, error: message };
        }
      },

      logout: () => {
        localStorage.removeItem('dsa_token');
        delete apiClient.defaults.headers.common['Authorization'];
        set({ user: null, token: null, isAuthenticated: false, error: null });
      },

      // Rehydrate token on app load
      initAuth: () => {
        const stored = get().token || localStorage.getItem('dsa_token');
        if (stored) {
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${stored}`;
          set({ token: stored, isAuthenticated: true });
        }
      },
    }),
    {
      name: 'dsa-auth-store',
      partialize: (state) => ({ token: state.token, user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);

