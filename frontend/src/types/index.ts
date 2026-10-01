export interface User {
  id: number;
  email: string;
  name: string;
  settings?: UserSettings;
}

export interface UserSettings {
  timezone: string;
  reminder_time: string;
  paused: boolean;
  duration_months: number;
  level: string;
  daily_count: number;
  source_type: string;
}

export interface Problem {
  id: number;
  number: number;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  topic: string;
  pattern?: string;
  similar_to?: string;
  url: string;
  display_header?: string;
  display_hint?: string;
}

export interface RoadmapItem {
  id: number;
  day_index: number;
  is_revision: boolean;
  status: 'pending' | 'done' | 'hard' | 'easy' | 'skipped';
  assigned_at: string;
  completed_at?: string;
  unlock_at?: string;
  tip?: string;
  problem: Problem;
}

export interface TodayView {
  current_day: number;
  total_days: number;
  items: RoadmapItem[];
  can_advance: boolean;
  next_unlock_at?: string;
  revision_count: number;
  all_done_today: boolean;
  server_time: string;
}

export interface Roadmap {
  id: number;
  duration_months: number;
  level: string;
  daily_count: number;
  status: string;
  current_day_index: number;
  total_days: number;
  completed_count: number;
  total_count: number;
  items: RoadmapItem[];
}

export interface CheatSheetContent {
  topic: string;
  when_to_use: string[];
  core_idea: string;
  code_templates: {
    python: string;
    cpp: string;
    java: string;
  };
  formulas_and_identities: string[];
  complexity_table: {
    operation: string;
    time: string;
    space: string;
  }[];
  common_mistakes: string[];
  pattern_to_problem_map: {
    number: number;
    title: string;
  }[];
  quick_revision: string[];
}

export interface CheatSheetSummary {
  id: number;
  topic: string;
  when_to_use: string[];
  core_idea: string;
  formulas_count: number;
  common_mistakes_count: number;
  quick_revision_points: string[];
}

export interface NotificationItem {
  id: number;
  title: string;
  message: string;
  type: string;
  is_read: boolean;
  created_at: string;
}
