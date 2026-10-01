import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const dsaApi = {
  // Upload and parsing
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  parseText: async (text) => {
    const response = await apiClient.post('/parse-document', { text });
    return response.data;
  },

  getBuiltInProblems: async () => {
    const response = await apiClient.get('/built-in-problems');
    return response.data;
  },

  getProblems: async (params = {}) => {
    const response = await apiClient.get('/problems', { params });
    return response.data;
  },

  // Roadmap generation and retrieval
  generateRoadmap: async (config) => {
    const response = await apiClient.post('/generate-roadmap', config);
    return response.data;
  },

  getCurrentRoadmap: async () => {
    const response = await apiClient.get('/roadmap/active/current');
    return response.data;
  },

  getRoadmapById: async (id) => {
    const response = await apiClient.get(`/roadmap/${id}`);
    return response.data;
  },

  // Problem and Roadmap item updates
  updateProblemStatus: async (itemId, status, notes = '') => {
    const response = await apiClient.patch(`/roadmap/item/${itemId}/status`, { status, notes });
    return response.data;
  },

  // Daily study & progress
  getTodayProblems: async () => {
    const response = await apiClient.get('/today');
    return response.data;
  },

  getProgress: async () => {
    const response = await apiClient.get('/progress');
    return response.data;
  },

  getRecommendations: async () => {
    const response = await apiClient.get('/recommendations');
    return response.data;
  },

  // Spaced revision
  getRevisions: async (status = 'All') => {
    const response = await apiClient.get('/revision', { params: { status } });
    return response.data;
  },

  updateRevisionStatus: async (revId, status) => {
    const response = await apiClient.patch(`/revision/${revId}/status`, { status });
    return response.data;
  },

  // Google Drive & Master Formulas
  getDriveLinks: async () => {
    const response = await apiClient.get('/drive-links');
    return response.data;
  },

  addDriveLink: async (payload) => {
    const response = await apiClient.post('/drive-links', payload);
    return response.data;
  },

  getFormulaDoc: async () => {
    const response = await apiClient.get('/formula-doc');
    return response.data;
  },

  getDownloadFormulaDocUrl: () => {
    return `${API_BASE_URL}/download-formula-doc`;
  },

  // Helper to generate LeetCode URL
  getLeetCodeUrl: (leetcodeNumber, slug, title) => {
    if (slug && slug.length > 2) {
      return `https://leetcode.com/problems/${slug}/`;
    }
    const query = encodeURIComponent(`${leetcodeNumber ? leetcodeNumber + ' ' : ''}${title}`);
    return `https://leetcode.com/problemset/all/?search=${query}`;
  },
};

export default apiClient;
