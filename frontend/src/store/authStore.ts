import { create } from 'zustand';
import { User, UserSettings } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  updateSettings: (settings: Partial<UserSettings>) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => {
  const savedToken = localStorage.getItem('dsa_token');
  const savedUser = localStorage.getItem('dsa_user');

  return {
    user: savedUser ? JSON.parse(savedUser) : null,
    token: savedToken,
    isAuthenticated: !!savedToken,

    setAuth: (user: User, token: string) => {
      localStorage.setItem('dsa_token', token);
      localStorage.setItem('dsa_user', JSON.stringify(user));
      set({ user, token, isAuthenticated: true });
    },

    updateSettings: (newSettings: Partial<UserSettings>) => {
      set((state) => {
        if (!state.user) return state;
        const updatedUser = {
          ...state.user,
          settings: {
            ...(state.user.settings || {
              timezone: 'UTC',
              reminder_time: '09:00',
              paused: false,
              duration_months: 6,
              level: 'Average',
              daily_count: 1,
              source_type: 'default',
            }),
            ...newSettings,
          },
        };
        localStorage.setItem('dsa_user', JSON.stringify(updatedUser));
        return { user: updatedUser };
      });
    },

    logout: () => {
      localStorage.removeItem('dsa_token');
      localStorage.removeItem('dsa_user');
      set({ user: null, token: null, isAuthenticated: false });
    },
  };
});
