import { create } from 'zustand';

// Thin shared UI store — auth state lives in authStore.ts
interface UIState {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
}

export const useStore = create<UIState>((set) => ({
  sidebarOpen: false,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));
