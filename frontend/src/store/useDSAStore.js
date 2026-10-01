import { create } from 'zustand';

export const useDSAStore = create((set, get) => ({
  // Upload & Problem Import State
  importedProblems: [],
  uploadMeta: null,
  isImporting: false,
  
  // Roadmap Configuration
  userLevel: 'Average', // Beginner, Average, Advanced
  durationMonths: 6,    // 3, 6, 9, 12
  targetProblemCount: 150, // 20, 50, 100, 150, 200
  roadmapTitle: 'My Personalized DSA Roadmap',
  useBuiltIn: false,
  
  // Active Roadmap & Progress
  activeRoadmap: null,
  progressData: null,
  todayData: null,
  isLoadingRoadmap: false,
  
  // Actions
  setImportedProblems: (problems, meta = null) => set({ importedProblems: problems, uploadMeta: meta }),
  setUserLevel: (level) => set({ userLevel: level }),
  setDurationMonths: (months) => set({ durationMonths: months }),
  setTargetProblemCount: (count) => set({ targetProblemCount: count }),
  setRoadmapTitle: (title) => set({ roadmapTitle: title }),
  setUseBuiltIn: (val) => set({ useBuiltIn: val }),
  setActiveRoadmap: (roadmap) => set({ activeRoadmap: roadmap }),
  setProgressData: (data) => set({ progressData: data }),
  setTodayData: (data) => set({ todayData: data }),
  setLoadingRoadmap: (val) => set({ isLoadingRoadmap: val }),

  // Update item status in local roadmap state for instant UI responsiveness
  updateLocalItemStatus: (itemId, newStatus) => {
    const roadmap = get().activeRoadmap;
    if (!roadmap || !roadmap.weeks) return;

    const updatedWeeks = roadmap.weeks.map((week) => ({
      ...week,
      days: week.days.map((day) => ({
        ...day,
        problems: day.problems.map((prob) => {
          if (prob.roadmap_item_id === itemId || prob.id === itemId) {
            return { ...prob, status: newStatus };
          }
          return prob;
        }),
      })),
    }));

    set({ activeRoadmap: { ...roadmap, weeks: updatedWeeks } });
  },
}));
